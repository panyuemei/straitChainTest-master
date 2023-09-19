import asyncio
import datetime
import json
from core.web3.main import Web3
from settings import settings

w3 = Web3(Web3.AsyncHTTPProvider(settings.chain_url, request_kwargs=settings.request_kwargs))
scs = w3.async_scs

ca = None
storage = []
process_start_at = datetime.datetime.now().timestamp()


def average(data: list[int | float], r=2):
    if len(data) == 0:
        return 0
    return round(sum(data) / len(data), r)


async def mint(contract_address, send_time_list: list = None):
    start = datetime.datetime.now().timestamp()
    if send_time_list is None:
        send_time_list = [start, ]
    else:
        send_time_list.append(start)
    try:
        result = await scs.mint(1,
                                contract_address,
                                nft_name='武夷山藏品-单个',
                                c_id='',
                                nft_uri='http://nps.shang-chain.com:30023/profile/tmp/ahjdfhf.json',
                                copy_right='熵链科技版权',
                                issuer='熵链科技发行',
                                operator='熵链科技运营',
                                remark='武夷山世界遗产',
                                collect_sn='collect_sn',
                                use_alone=True)
        received_time = datetime.datetime.now().timestamp()
        storage_data = {
            'send_times': send_time_list,
            'received_time': received_time,
            'response': dict(result)
        }
        storage.append(storage_data)

    except Exception as e:
        print(e)
        return await mint(contract_address, send_time_list)
    return result


async def main(count: int):
    # 部署合约
    global ca
    tx_hash = await scs.deploy_contract_get_hash(count)

    # 获取合约地址
    contract_address = None
    while contract_address is None:
        contract_address = await scs.contract_address_by_hash(tx_hash)
        if contract_address is None:
            await asyncio.sleep(1)
    ca = contract_address
    print(f'合约地址：{contract_address}')

    # 铸造
    tasks = []
    for _ in range(count):
        task = asyncio.create_task(mint(contract_address))
        tasks.append(task)
    gather_result = await asyncio.gather(*tasks)
    success = list(filter(lambda x: x is not None, gather_result))
    print(f'铸造成功统计（共{len(success)}个）：')
    print(success)


if __name__ == '__main__':
    c = 1000
    asyncio.run(main(c))
    print(storage)

    with open(f'./cache/result-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-{ca}.json', 'w') as f:
        content = {
            'count': c,
            'contract_address': ca,
            'storage': storage
        }
        f.write(json.dumps(content, indent=2, ensure_ascii=False))
