import requests


class Request:
    def __init__(self):
        self.session = requests.session()

    @property
    def request(self):
        return self.session.request


if __name__ == '__main__':
    req = Request()
    res = req.request('GET', 'http://www.baidu.com')
    print(res.text)
