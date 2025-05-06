import { Request, Response, NextFunction } from 'express';
import { v4 as uuidValidate } from 'uuid';

/**
 * Interface for TransactionID configuration
 */
interface TransactionIDConfig {
  required?: boolean;
  headerName?: string;
}

/**
 * Middleware for validating transaction ID
 * @param config Configuration options for transaction ID validation
 * @returns Express middleware function
 */
export const transactionIDValidator = (config: TransactionIDConfig = {}) => {
  const {
    required = true,
    headerName = 'x-transaction-id'
  } = config;

  return (req: Request, res: Response, next: NextFunction) => {
    const transactionId = req.headers[headerName] as string | undefined;

    // Check if transaction ID is required but missing
    if (required && !transactionId) {
      return res.status(400).json({
        error: 'Transaction ID is required',
        details: `Please provide a valid transaction ID in the '${headerName}' header`
      });
    }

    // If transaction ID is provided, validate its format
    if (transactionId) {
      // Validate UUID format
      if (!uuidValidate(transactionId)) {
        return res.status(400).json({
          error: 'Invalid Transaction ID',
          details: 'Transaction ID must be a valid UUID v4'
        });
      }
    }

    // Attach transaction ID to request for further use
    req.transactionId = transactionId;

    next();
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