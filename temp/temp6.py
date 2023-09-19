# TODO: 动态添加异步方法
import asyncio
import time
from types import MethodType

from awaits.awaitable import awaitable


def async_desc(func):
    global is_async
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if is_async:
        return async_wrapper
    else:
        return wrapper


class Cat:

    # @async_desc
    def runner(self, speed):
        print(f'猫在以每秒{speed}米的速度奔跑')

    def __getattribute__(self, item):
        if is_async:
            return awaitable(object.__getattribute__(self, item))
            # tmp = object.__getattribute__(self, item)
            #
            # async def async_item(_, *args, **kwargs):
            #     return tmp(*args, **kwargs)
            #
            # object.__setattr__(self, item, MethodType(async_item, self))

        return object.__getattribute__(self, item)


async def run(self: 'Cat', speed):
    await asyncio.sleep(1)
    print('执行动态方法')
    return self.runner(speed * 10)
    # print(f'猫在以每秒{speed}米的速度异步奔跑')


if __name__ == '__main__':
    is_async = True
    cat = Cat()
    # cat.run(1)
    asyncio.run(cat.runner(1))
