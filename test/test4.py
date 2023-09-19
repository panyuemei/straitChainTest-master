import json
import requests

url = 'http://192.168.80.15/strait-chain-client-test/api/develop/straits/action?chainCode=ScOcc03001'
headers = {
    'Content-Type': 'application/json'
}
data = {
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'scs_nft_list',
    'params': ['0x9b4F8a365aBE68cb065AfdB1a8835Da460114efb']
}

res = requests.post(url, data=json.dumps(data), headers=headers).json()
result = res['result']
print(result)
