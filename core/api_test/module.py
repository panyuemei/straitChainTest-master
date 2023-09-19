import json
from typing import TYPE_CHECKING
import requests
from requests import Session

if TYPE_CHECKING:
    from core.api_test.method import Interface


def get_call(module: 'Module', interface: 'Interface'):
    def caller(data=None, update: dict = None, headers: dict = None):
        if data is not None:
            interface.data = data

        if update is not None:
            for k, v in update.items():
                if v is not Ellipsis:
                    interface.data[k] = v

        if headers is not None:
            interface.headers.update(headers)
        return module.requests(interface)
    return caller


class Module:
    is_async = False

    def __init__(self, base_url=None, ):
        self.base_url = base_url
        self.session: Session = ...

    def call(self, interface: 'Interface'):
        return get_call(self, interface)

    def set_session(self):
        self.session = requests.session()

    def requests(self, interface: 'Interface', *args, **kwargs):
        if self.session is Ellipsis:
            self.set_session()

        # if self.base_url is not None:
        #     if not (interface.url.startswith('http://') or interface.url.startswith('https://')):
        #         interface.url = self.base_url + interface.url

        response = self.session.request(
            interface.method,
            url=interface.url,
            data=json.dumps(interface.data),
            headers=interface.headers, *args, **kwargs)
        return response

