
import logging
import os

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #don't add multiple handlers if the logger already has handlers
    if not logger.handlers:
        #console handler - shows in terminal

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        #file handler - writes to a file
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/test_logs.log", mode='w')
        file_handler.setLevel(logging.DEBUG)

        #formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        #add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger