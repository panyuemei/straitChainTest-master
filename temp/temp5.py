from functools import wraps
from types import MethodType
from typing import Callable
from core.logger import log


def logger(func, *args, **kwargs):
    print(f'开始执行函数{func} args={args} kwargs={kwargs}')
    result = func(*args, **kwargs)
    print(f'结束执行函数{func} result={result}')
    return result


class Test:

    def test1(self, *args, **kwargs):
        return 'aaaaaaa'

    def test2(self, *args, **kwargs):
        return

    def test3(self, *args, **kwargs):
        return

    def __getattribute__(self, item):
        ret = super().__getattribute__(item)

        if type(ret) is MethodType:
            def res(*args, **kwargs):
                no_log = kwargs.get('no_log', False)
                if not no_log:
                    log.info(f'开始执行函数[{ret.__name__}] args={args} kwargs={kwargs}')
                result = ret(*args, **kwargs)
                if not no_log:
                    log.info(f'结束执行函数[{ret.__name__}] result={result}')
                return result

            return res
        else:
            return ret


t = Test()
t.test1()
t.test2()
t.test3()

