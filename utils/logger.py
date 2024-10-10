import logging
import os

class Logger:
    def __init__(self, name=__name__, log_to_file=False, log_file_name="app.log"):
        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Set up formatter
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        # Check if logging to a file or stdout
        if log_to_file:
            # Create file handler
            file_handler = logging.FileHandler(log_file_name)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        else:
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
