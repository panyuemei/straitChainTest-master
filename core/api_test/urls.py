from settings import settings


class Urls:

    """商店"""
    market_page = '/app/market/page'
    market_recommend = '/app/market/recommend/page'

    """登录"""
    login_common = '/login'
    login_dev = '/login/dev'
    login_by_address = '/login/address'

    def __getattribute__(self, item):
        return settings.host + object.__getattribute__(self, item)


urls = Urls()


if __name__ == '__main__':
    print(urls.login_dev)