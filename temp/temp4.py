import asyncio
import time

from settings import settings
from core.web3.main import Web3


contract_address = Web3.toChecksumAddress('0x935b0cf837a576a9519462c34d97ead815091e40')
to_address = Web3.toChecksumAddress('0x98a309d087ba9408ea48ae778eda961b9c534ed8')

# contract_address = Web3.toChecksumAddress('0x8d3a69b26c5ad79f0b50d8bdaed96f2a02234762')
# to_address = Web3.toChecksumAddress('0x53d9986bffa75d47c4f8d8e527b55c715a367ff8')


def sync_test(attr, *args, **kwargs):
    contract = Web3(Web3.HTTPProvider(settings.chain_url)).scs.contract(contract_address)
    result = getattr(contract, attr)(*args, **kwargs)
    print(result)


def async_test(attr, *args, **kwargs):
    async def task():
        contract = Web3(Web3.AsyncHTTPProvider(settings.chain_url)).async_scs.contract(contract_address)
        result = await getattr(contract, attr)(*args, **kwargs)
        print(result)
        return result
    asyncio.run(task())


def run():
    print(f'{"-" * 20}开始同步测试{"-" * 20}')
    sync_test(func_name, *params)
    print(f'{"-" * 20}结束同步测试{"-" * 20}')

    print('*' * 100)
    time.sleep(5)

    print(f'{"-" * 20}开始异步测试{"-" * 20}')
    async_test(func_name, *params)
    print(f'{"-" * 20}结束异步测试{"-" * 20}')


if __name__ == '__main__':
    func_name = 'get_owner'
    params = [2]
    run()

