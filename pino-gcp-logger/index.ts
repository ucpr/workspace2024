import pino, { type Level, type LoggerOptions } from 'pino';

// https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#LogSeverity
const gcpLogSeverity: Record<string, string> = {
  trace: 'DEBUG',
  debug: 'DEBUG',
  info: 'INFO',
  warn: 'WARNING',
  error: 'ERROR',
  fatal: 'CRITICAL',
}

export interface ServiceContext {
  serviceName?: string;
  version?: string;
  mixin?: (mergeObject: object, level: number) => object;
}

function gcpLogger(
  options?: LoggerOptions,
  context: ServiceContext = {},
): LoggerOptions {
  const { serviceName, version, mixin } = context;

  const base =
    serviceName && version
      ? { serviceContext: { service: serviceName, version } }
      : {};

  return {
    base,
    level: "info",
    mixin: (mergeObject: object, _: number) => {
      return {
        jsonPayload: {
          ...mergeObject,
        },
      };
    },
    formatters: {
      level: (label: string) => {
        const pinoLevel = label as Level;
        const severity = gcpLogSeverity[pinoLevel] ?? "INFO";
        return { severity };
      },
    },
    serializers: {
      err: pino.stdSerializers.err,
      error: pino.stdSerializers.err,
    },
    timestamp: pino.stdTimeFunctions.isoTime,
    messageKey: 'message',
    ...options,
  }
}

export class Logger {
  logger: pino.Logger;

  constructor(serviceName: string, version: string) {
    this.logger = pino(gcpLogger({}, {
      serviceName: serviceName,
      version: version,
    }));
  }

  debug(message: String, obj?: Record<string, string>) {
    this.logger.debug({ message: message, ...obj });
  }

  info(message: String, obj?: Object) {
    this.logger.info({ message: message, ...obj });
  }

  warn(message: String, obj?: Object) {
    this.logger.warn({ message: message, ...obj });
  }

  error(message: String, obj?: Object) {
    this.logger.error({ message: message, ...obj });
  }

  critical(message: String, obj?: Object) {
    this.logger.fatal({ message: message, ...obj });
  }
}

let logger = new Logger('my-service', 'v1');
logger.info('Hello world', { a: 'b' });
logger.debug('Hello world', { a: 'b' });
