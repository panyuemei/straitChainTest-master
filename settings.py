import os
import sys
from core.utils.make_setting import Settings

BASE_DIR = os.path.split(os.path.abspath(__file__))[0]


# env = 'prod'
# username = 'operation@straitchain.com'
# username = '1669971502@qq.com'

env = 'test'
username = 'test200@qq.com'
# username = 'test500@qq.com'

address = None
chain_name = None


# settings = Settings(BASE_DIR, env, username, address, chain_name)
if sys.argv[1:]:
    params = sys.argv[1:]
else:
    params = [env, username, address, chain_name]
# settings = Settings(BASE_DIR, *params, use_urn_name='gateway_urn')
settings = Settings(BASE_DIR, *params)
test_settings = Settings(BASE_DIR, 'test', 'test200@qq.com')
