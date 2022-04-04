#encoding=utf-8
import logging
import logging.handlers

logger = logging.getLogger(__name__)


def gen_log(name):
    filename = f'./{name}.log'
    logger.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(filename)s[line:%(lineno)d] : %(message)s")

    handler = logging.FileHandler(filename, mode='w')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(console)
    # logger.debug('This is a debug message.')
    # logger.info('This is an info message.')
    # logger.warning('This is a warning message.')
    # logger.error('This is an error message.')
    # logger.critical('This is a critical message.')
    # print(id(logger))

if __name__ == '__main__':
    gen_log('freebuy')
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')