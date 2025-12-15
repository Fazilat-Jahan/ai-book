import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logger():
    """
    Sets up a structured logger for the FastAPI application.
    Logs will be in JSON format to stdout.
    """
    logger = logging.getLogger('rag_chatbot_backend')
    logger.setLevel(logging.INFO)

    # Use sys.stdout for output, which is typical for containerized applications
    handler = logging.StreamHandler(sys.stdout)

    # Define a custom formatter to output logs in JSON format
    formatter = jsonlogger.JsonFormatter(
        '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
    )
    handler.setFormatter(formatter)

    # Clear existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)
    return logger

# Initialize logger for the application
logger = setup_logger()

# Example usage
if __name__ == "__main__":
    logger.info("This is an info message from the logger.")
    logger.warning("This is a warning message.", extra={"details": "something might be wrong"})
    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("An error occurred!", exc_info=True)
