class Test:
    def __init__(self):
        print('开启')

    def run(self):
        print('执行')

    def __del__(self):
        print('关闭')


ttt = Test()
