import logging


class MLOGGER(logging.Formatter):
    # ANSI escape codes for coloring the console output
    BLUE = "\033[94m"
    RESET = "\033[0m"

    FORMATS = {
        logging.DEBUG: BLUE + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.INFO: BLUE + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.WARNING: BLUE + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.ERROR: BLUE + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
        logging.CRITICAL: BLUE + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logg = logging.getLogger('my_logger')
logg.setLevel(logging.DEBUG)  # Set the minimum logging level

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('mitm.log')

# Set the logging level for handlers
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
console_handler.setFormatter(MLOGGER())
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add handlers to the logger
logg.addHandler(console_handler)
logg.addHandler(file_handler)