error = {
    10002: '参数异常',
    10006: '业务操作异常',
    10007: '铸造等待中',
    20001: '系统级别异常',
    20006: '签名验签异常',
    30003: '调用合约返回失败',
    30004: '接口开放限制'
}


class ResponseParseError(BaseException):
    def __init__(self, msg=None):
        self.msg = str(msg)

    def __str__(self):
        return f'返回体解析错误{"：" + self.msg}'


class ResponseError(BaseException):
    def __init__(self, msg=None):
        self.msg = str(msg)

    def __str__(self):
        return f'业务异常{"：" + self.msg}'
