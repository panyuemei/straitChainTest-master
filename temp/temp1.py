import time

count = 0

def test():
    global count
    time.sleep(1)
    try:
        print('try')
        raise
    except Exception:
        count += 1
        print('except')
        if count < 10:
            return test()
        # return None
    else:
        print('else')


test()

