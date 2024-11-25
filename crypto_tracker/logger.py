import logging
import logging.handlers
import os


class Logger:

    def __init__(self, logging_service="crypto_tracker"):
        # Logger setup
        self.Logger = logging.getLogger(f"{logging_service}_logger")
        self.Logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if not self.Logger.hasHandlers():
            self.Logger.propagate = False
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s")

            # Ensure log directory exists
            os.makedirs("logs", exist_ok=True)

            # File handler
            fh = logging.FileHandler(f"logs/{logging_service}.log")
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self.Logger.addHandler(fh)

            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            self.Logger.addHandler(ch)

    def close(self):
        for handler in self.Logger.handlers[:]:
            handler.close()
            self.Logger.removeHandler(handler)

    def log(self, message, level="info"):
        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)

    def info(self, message):
        self.log(message, "info")

    def warning(self, message):
        self.log(message, "warning")

    def error(self, message):
        self.log(message, "error")

    def debug(self, message):
        self.log(message, "debug")
