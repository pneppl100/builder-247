import { Request, Response, NextFunction } from 'express';
import { v4 as uuidValidate, version as uuidVersion } from 'uuid';
import { performance } from 'perf_hooks';
import winston from 'winston';

// Configure logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'transaction-errors.log' })
  ]
});

/**
 * Transaction Uniqueness Service Interface
 */
interface TransactionUniquenessService {
  /**
   * Check if a transaction ID is unique
   * @param transactionId The transaction ID to check
   * @returns Promise resolving to boolean indicating uniqueness
   */
  isUnique(transactionId: string): Promise<boolean>;
}

/**
 * Configuration for Transaction ID Validation
 */
interface TransactionIDConfig {
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
        logger.warn('Transaction ID required but missing', {
          route: req.path,
          method: req.method
        });
        return res.status(400).json({
          error: 'Transaction ID is required',
          details: `Please provide a valid transaction ID in the '${headerName}' header`
        });
      }

      // If transaction ID is provided, validate its format
      if (transactionId) {
        // Validate UUID format
        if (!uuidValidate(transactionId) || uuidVersion(transactionId) !== 4) {
          logger.warn('Invalid transaction ID format', {
            transactionId,
            route: req.path,
            method: req.method
          });
          return res.status(400).json({
            error: 'Invalid Transaction ID',
            details: 'Transaction ID must be a valid UUID v4'
          });
        }

        // Check transaction uniqueness if service is provided
        if (uniquenessService) {
          const isUnique = await uniquenessService.isUnique(transactionId);
          if (!isUnique) {
            logger.warn('Duplicate transaction ID', {
              transactionId,
              route: req.path,
              method: req.method
            });
            return res.status(409).json({
              error: 'Duplicate Transaction ID',
              details: 'This transaction has already been processed'
            });
          }
        }
      }

      // Check middleware latency
      const endTime = performance.now();
      const duration = endTime - startTime;
      if (duration > maxLatency) {
        logger.warn('Transaction ID validation exceeded max latency', {
          duration,
          maxLatency
        });
      }

      // Attach transaction ID to request for further use
      req.transactionId = transactionId;

      next();
    } catch (error) {
      logger.error('Transaction ID validation error', {
        error: error instanceof Error ? error.message : String(error),
        route: req.path,
        method: req.method
      });
      res.status(500).json({
        error: 'Internal Server Error',
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
  }
}