import { transactionIDValidator } from '../../src/middleware/transaction_id_validator';
import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

describe('Transaction ID Validator Middleware', () => {
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let mockNext: jest.MockedFunction<NextFunction>;

  beforeEach(() => {
    mockRequest = {
      headers: {}
    };
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
    mockNext = jest.fn();
  });

  test('should pass with valid transaction ID', () => {
    const validTransactionId = uuidv4();
    mockRequest.headers = { 'x-transaction-id': validTransactionId };

    const middleware = transactionIDValidator();
    middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockRequest.transactionId).toBe(validTransactionId);
  });

  test('should fail if transaction ID is required but missing', () => {
    const middleware = transactionIDValidator();
    middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith(
      expect.objectContaining({
        error: 'Transaction ID is required'
      })
    );
    expect(mockNext).not.toHaveBeenCalled();
  });

  test('should fail with invalid transaction ID', () => {
    mockRequest.headers = { 'x-transaction-id': 'invalid-uuid' };

    const middleware = transactionIDValidator();
    middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith(
      expect.objectContaining({
        error: 'Invalid Transaction ID'
      })
    );
    expect(mockNext).not.toHaveBeenCalled();
  });

  test('should skip validation if not required and no ID provided', () => {
    const middleware = transactionIDValidator({ required: false });
    middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockRequest.transactionId).toBeUndefined();
  });

  test('should work with custom header name', () => {
    const validTransactionId = uuidv4();
    mockRequest.headers = { 'custom-transaction-id': validTransactionId };

    const middleware = transactionIDValidator({ 
      required: true, 
      headerName: 'custom-transaction-id' 
    });
    middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockRequest.transactionId).toBe(validTransactionId);
  });
});