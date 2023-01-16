import logging
import os

def get_logger(level, log_file=None):
    # if not os.path.exists(log_file):
    #     with open(log_file, 'w') as f:
    #         f.write('')
    head = '[%(asctime)-15s][%(levelname)s]%(message)s'
    if level == 'info':
        logging.basicConfig(level=logging.INFO, format=head)
    elif level == 'debug':
        logging.basicConfig(level=logging.DEBUG, format=head)
    logger = logging.getLogger()
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(head))
        logger.addHandler(file_handler)
    return logger

