import os
import random
import subprocess
import time
from settings import BASE_DIR

count = 10

success = 0

while True:
    env = 'test'
    if random.randint(1, 10) > 5:
        username = 'test500@qq.com'
    else:
        username = 'test200@qq.com'
    res = subprocess.run(['python', os.path.join(BASE_DIR, 'apps/nft/nft.py'), 'test', username, "", ""])
    if res.returncode == 0:
        success += 1
        print('*' * 500)
        print(f'已执行成功{success}次，剩余{count - success}次')
        if success >= count:
            break
        time.sleep(3)
    else:
        print('-' * 500)
        print(f'执行失败，剩余{count - success}次，重试。。。')
