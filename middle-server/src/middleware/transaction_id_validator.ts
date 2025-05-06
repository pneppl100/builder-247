import { Request, Response, NextFunction } from 'express';
import { validate as uuidValidate, version as uuidVersion } from 'uuid';
import { performance } from 'perf_hooks';

/**
 * Transaction Validation Result
 */
export interface TransactionValidationResult {
  isValid: boolean;
  error?: string;
  details?: string;
}

/**
 * Transaction Uniqueness Service Interface
 */
export interface TransactionUniquenessService {
  /**
   * Validate transaction ID uniqueness
   * @param transactionId The transaction ID to validate
   * @returns Promise resolving to validation result
   */
  validateTransaction(transactionId: string): Promise<TransactionValidationResult>;
}

/**
 * Configuration for Transaction ID Validation
 */
export interface TransactionIDConfig {
  required?: boolean;
  headerName?: string;
  uniquenessService?: TransactionUniquenessService;
  maxLatency?: number;
}

/**
 * Middleware for transaction ID validation
 * @param config Configuration options for transaction ID validation
 * @returns Express middleware function
 */
export const transactionIDValidator = (config: TransactionIDConfig = {}) => {
  const {
    required = true,
    headerName = 'x-transaction-id',
    uniquenessService = null,
    maxLatency = 100 // 100ms max latency
  } = config;

  return async (req: Request, res: Response, next: NextFunction) => {
    const startTime = performance.now();
    const transactionId = req.headers[headerName] as string | undefined;

    try {
      // Check if transaction ID is required but missing
      if (required && !transactionId) {
        return res.status(400).json({
          isValid: false,
          error: 'Transaction ID Required',
          details: `Please provide a valid transaction ID in the '${headerName}' header`
        });
      }

      // If transaction ID is provided, validate its format
      if (transactionId) {
        // Validate UUID format
        if (!uuidValidate(transactionId) || uuidVersion(transactionId) !== 4) {
          return res.status(400).json({
            isValid: false,
            error: 'Invalid Transaction ID',
            details: 'Transaction ID must be a valid UUID v4'
          });
        }

        // Check transaction uniqueness if service is provided
        if (uniquenessService) {
          const validationResult = await uniquenessService.validateTransaction(transactionId);
          
          if (!validationResult.isValid) {
            return res.status(409).json({
              isValid: false,
              error: validationResult.error || 'Duplicate Transaction',
              details: validationResult.details || 'This transaction has already been processed'
            });
          }
        }
      }

      // Check middleware latency
      const endTime = performance.now();
      const duration = endTime - startTime;
      if (duration > maxLatency) {
        // Log warning about excessive latency
        console.warn(`Transaction ID validation exceeded max latency: ${duration}ms`);
      }

      // Attach transaction ID to request for further use
      req.transactionId = transactionId;

      // Return successful validation result
      res.locals.transactionValidation = {
        isValid: true
      };

      next();
    } catch (error) {
      // Handle unexpected errors
      console.error('Transaction ID validation error:', error);
      return res.status(500).json({
        isValid: false,
        error: 'Internal Validation Error',
        details: 'Failed to validate transaction ID'
      });
    }
  };
};

// Extend Request interface to include optional transactionId
declare global {
  namespace Express {
    interface Request {
      transactionId?: string;
    }
    interface Response {
      locals: {
        transactionValidation?: TransactionValidationResult;
      } & LocalsObject;
    }
  }
}