import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.api_test.module import Module

default_headers = {
    'Content-Type': 'application/json'
}


class Interface:
    def __init__(self, method, url, headers: dict = None, data: dict = None, params=None):
        self.method = method
        self.url: str = url
        self.headers = default_headers if headers is None else headers
        self.data = data
        self.params = params

    def __get__(self, instance: 'Module', owner):
        return instance.call(self)

    def __str__(self):
        return f'{self.method.upper()} {self.url} {self.data}'
