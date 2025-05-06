import { transactionIDValidator, TransactionValidationResult, TransactionUniquenessService } from '../../src/middleware/transaction_id_validator';
import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

// Mock Uniqueness Service
class MockUniquenessService implements TransactionUniquenessService {
  private usedIds: Set<string> = new Set();

  async validateTransaction(id: string): Promise<TransactionValidationResult> {
    if (this.usedIds.has(id)) {
      return {
        isValid: false,
        error: 'Duplicate Transaction',
        details: 'Transaction ID has been used before'
      };
    }
    this.usedIds.add(id);
    return { isValid: true };
  }
}

describe('Transaction ID Validator Middleware', () => {
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let mockNext: jest.MockedFunction<NextFunction>;
  let mockUniquenessService: MockUniquenessService;

  beforeEach(() => {
    mockRequest = {
      headers: {},
      path: '/test-route',
      method: 'POST'
    };
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn(),
      locals: {}
    };
    mockNext = jest.fn();
    mockUniquenessService = new MockUniquenessService();
  });

  test('should pass with valid transaction ID', async () => {
    const validTransactionId = uuidv4();
    mockRequest.headers = { 'x-transaction-id': validTransactionId };

    const middleware = transactionIDValidator({
      uniquenessService: mockUniquenessService
    });
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockRequest.transactionId).toBe(validTransactionId);
    expect(mockResponse.locals.transactionValidation).toEqual({ isValid: true });
  });

  test('should fail if transaction ID is required but missing', async () => {
    const middleware = transactionIDValidator();
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith(
      expect.objectContaining({
        isValid: false,
        error: 'Transaction ID Required'
      })
    );
    expect(mockNext).not.toHaveBeenCalled();
  });

  test('should fail with invalid transaction ID', async () => {
    mockRequest.headers = { 'x-transaction-id': 'invalid-uuid' };

    const middleware = transactionIDValidator();
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith(
      expect.objectContaining({
        isValid: false,
        error: 'Invalid Transaction ID'
      })
    );
    expect(mockNext).not.toHaveBeenCalled();
  });

  test('should fail with duplicate transaction ID', async () => {
    const duplicateTransactionId = uuidv4();
    mockRequest.headers = { 'x-transaction-id': duplicateTransactionId };

    const middleware = transactionIDValidator({
      uniquenessService: mockUniquenessService
    });
    
    // First call should pass
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);
    expect(mockNext).toHaveBeenCalled();

    // Reset mocks
    mockNext.mockClear();
    mockResponse.status = jest.fn().mockReturnThis();
    mockResponse.json = jest.fn();

    // Second call should fail
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);
    expect(mockResponse.status).toHaveBeenCalledWith(409);
    expect(mockResponse.json).toHaveBeenCalledWith(
      expect.objectContaining({
        isValid: false,
        error: 'Duplicate Transaction'
      })
    );
    expect(mockNext).not.toHaveBeenCalled();
  });

  test('should skip validation if not required and no ID provided', async () => {
    const middleware = transactionIDValidator({ required: false });
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockRequest.transactionId).toBeUndefined();
  });

  test('should work with custom header name', async () => {
    const validTransactionId = uuidv4();
    mockRequest.headers = { 'custom-transaction-id': validTransactionId };

    const middleware = transactionIDValidator({ 
      required: true, 
      headerName: 'custom-transaction-id',
      uniquenessService: mockUniquenessService
    });
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockRequest.transactionId).toBe(validTransactionId);
  });

  test('should handle uniqueness service errors gracefully', async () => {
    // Simulate a service that always throws an error
    const brokenService = {
      validateTransaction: jest.fn().mockRejectedValue(new Error('Service error'))
    };

    mockRequest.headers = { 'x-transaction-id': uuidv4() };

    const middleware = transactionIDValidator({
      uniquenessService: brokenService as any
    });
    await middleware(mockRequest as Request, mockResponse as Response, mockNext);

    expect(mockResponse.status).toHaveBeenCalledWith(500);
    expect(mockResponse.json).toHaveBeenCalledWith(
      expect.objectContaining({
        isValid: false,
        error: 'Internal Validation Error'
      })
    );
    expect(mockNext).not.toHaveBeenCalled();
  });
});