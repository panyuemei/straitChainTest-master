from core.api_test.method import Interface
from core.api_test.module import Module
from core.api_test.urls import urls

GET = 'GET'
POST = 'POST'


class BaseStrait(Module):
    _market_page = Interface(
        POST,
        urls.market_page,
        data={'curPage': 1, 'limit': 4, 'appType': 'service'}
    )

    _market_recommend = Interface(
        POST,
        urls.market_recommend,
        data={'curPage': 1, 'limit': 3, 'appType': 'app'}
    )

    _login = Interface(
        POST,
        '/login/dev',
        data={'username': 'test200@qq.com', 'password': 'qwer1234'}
    )

    _login_by_address = Interface(
        POST,
        '/login/address',
        data={'address': '0x6d61dbfb32599cd94fee1c8fab1e80e2ee8623d7'}
    )

    _index = Interface(
        GET,
        '/'
    )


class AsyncStrait(BaseStrait):
    is_async = True


class Strait(BaseStrait):

    def market_page(self):
        return self._market_page()

    def market_recommend(self):
        return self._market_recommend()

    def login(self, username=..., password=...):
        return self._login(update={'username': username, 'password': password})

    def login_by_address(self, address=...):
        return self._login_by_address(update={'address': address})

    def index(self):
        return self._index()


if __name__ == '__main__':
    strait = Strait()
    # res = strait.login()
    res = strait.market_recommend()

    print(res.text)
