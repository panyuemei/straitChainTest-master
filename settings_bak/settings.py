from eth_utils import to_hex
# from web3 import Web3

from core.web3.datatypes import Address

env = 'test'
# env = 'prod'
# env = 'pre-prod'

# chain_id = ''     # 老链
# chain_id = 'ScOcc02001'     # 老链
chain_id = 'ScOcc03001'     # polygon

jsonrpc = '2.0'
headers = {
    'Content-Type': 'application/json',
}
# log_level = 'INFO'
log_level = 'DEBUG'
chain_func_prefix = 'scs_'
gas = to_hex(210000)
gas_price = 563000000007
c_url = '/api/develop/straits/action'
i_url = '/api/develop/ipfsUpload'

match env:
    case 'test':
        # 测试配置
        host = 'http://192.168.80.15/strait-chain-client-test'
        # host = 'http://192.168.70.24:10825/webclient/'
        app_id = 'gPAEQ1U7'
        app_key = '25193d0a7e08c1638e0d336f223708693fa27253'
        master_address = Address('0x6d61dbfb32599cd94fee1c8fab1e80e2ee8623d7')  # test200@qq.com

        nft_service_id = '33BFWBCU'
        private_key = '0x30254413e44298281b625fa3702adc23c602635bb566709c412b4efb9ddb7a33'

        # master_address = Address('0x9b4F8a365aBE68cb065AfdB1a8835Da460114efb')  # test500@qq.com
        # private_key = '9dddbff5b27f40aff4dfb94f8ffe0262f5bf793cc147c6b1c6bf4bf0c25855f0'
    case 'pre-prod':
        # 测试配置
        host = 'https://baoye.www.shangchain.net/webclient'
        app_id = 'x7ztWQlk'
        app_key = '8b8c5a8055d93b6caef5d085ff3027343ed8cdd6'
        master_address = Address('0x63Da6c06fD55A9D1a3EfF0c27732768d6e8aF633')
        nft_service_id = 'L4gEKdhC'
        private_key = '5d2c79ec5ea305c8d0449a0cb5b6dda6f198393821ad142a1746944f8502eb4e'
    case 'prod':
        # 正式配置
        host = 'https://www.straitchain.com/webclient'
        app_id = 'Ps9WIoof'
        app_key = '9743abeda378ee68bc1efe4b2f218c94bad6543f'
        master_address = Address('0xf539959202351e89a355eb14a62e9def43ffd88f')
        nft_service_id = '4Dbz3ZeG'
        private_key = '12c7aea5ff0423fbaa9f0f23930aebf1594075bd00bf466564c3d2bffb22932b'
        # app_id = 'zDaX0Cm0'
        # app_key = '9dc7606f796bf2e775cf4e59b5af98a46cebfd21'
        # master_address = Address('0x9db8cac77964189b70e3128c2dc31e3034b529c1')
        # nft_service_id = 'bX1ynUK7'
        # private_key = '12c7aea5ff0423fbaa9f0f23930aebf1594075bd00bf466564c3d2bffb22932b'
    case _:
        raise Exception(f'env配置错误env={env!r}')

chain_url = host + c_url + (f'?chainCode={chain_id}' if chain_id else '')
IPFSUpload_url = host + i_url




