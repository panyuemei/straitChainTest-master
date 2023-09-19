import logging.handlers
import os
from functools import wraps
import typing
from settings import settings


class Logger:
    logger = None

    @classmethod
    def get_logger(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger()
            cls.logger.setLevel(settings.log_level)
            sh = logging.StreamHandler()
            log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/')
            if not os.path.exists(log_path):
                os.mkdir(log_path)
            th = logging.handlers.TimedRotatingFileHandler(
                os.path.join(log_path, 'nft_test.log'), when='MIDNIGHT', interval=1, backupCount=30, encoding='utf-8'
            )
            fmt = '%(levelname)s %(asctime)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
            formatter = logging.Formatter(fmt)
            sh.setFormatter(formatter)
            th.setFormatter(formatter)
            cls.logger.addHandler(sh)
            cls.logger.addHandler(th)
        return cls.logger


log = Logger().get_logger()

# 大佬提供的临时解决方案，使用泛型 T，（此方式会导致函数的二级属性提示消失，等待pycharm修复）
T = typing.TypeVar('T', bound=typing.Callable[..., typing.Any])


def logger(remark=None, level=logging.DEBUG):
    def logging_decorator(func: T) -> T:
        @wraps(func)
        def wrapped(*args, **kwargs):
            # pycharm的bug，使用此装饰器的函数用Ctrl + P查看参数提示总会显示上一行的(*args, **kwargs)，期待修复
            log.log(level, f'[{"" if remark is None else remark}>>>] - [{func.__name__}] args={args} kwargs={kwargs}')
            result = func(*args, **kwargs)
            log.log(level, f'[{"" if remark is None else remark}<<<] - [{func.__name__}] result={result}')
            return result
        return wrapped
    return logging_decorator


def async_logger(remark=None, level=logging.DEBUG):
    def logging_decorator(func: T) -> T:
        @wraps(func)
        async def wrapped(*args, **kwargs):
            log.log(level, f'[{"" if remark is None else remark}>>>] - [{func.__name__}] args={args} kwargs={kwargs}')
            result = await func(*args, **kwargs)
            log.log(level, f'[{"" if remark is None else remark}<<<] - [{func.__name__}] result={result}')
            return result
        return wrapped
    return logging_decorator


if __name__ == '__main__':
    ...
