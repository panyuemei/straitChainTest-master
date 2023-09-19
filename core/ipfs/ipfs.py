import os
from typing import TYPE_CHECKING

import aiohttp
import requests
from requests_toolbelt import MultipartEncoder

from core.exceptions import ResponseError
from core.logger import log, logger, async_logger

if TYPE_CHECKING:
    from core.web3.scs import BaseScs


class BaseIPFS:
    is_async = False

    def __init__(self, scs: "BaseScs"):
        self.scs = scs
        self.IPFS_upload_url = self.scs.settings.chain_url

    def params_processor(self, file_path, file_name, mode):
        params = {
            'appId': self.scs.settings.app_id,
            'address': self.scs.default_account,
        }
        sign_txn = self.scs.md5_sign(*list(params.values()))[-1]
        if file_name is None:
            file_name = os.path.split(file_path)[-1]
        params['file'] = (file_name, open(file_path, mode))
        params['sign'] = sign_txn
        payload = MultipartEncoder(params)
        headers = {**self.scs.settings.headers, **{'Content-Type': payload.content_type}}
        log.debug(payload.fields)
        return dict(
            url=self.scs.settings.IPFSUpload_url,
            data=payload,
            headers=headers
        )

    @staticmethod
    def response_processor(response):
        log.debug(response)
        if 'result' in response and response['result'] is not None:
            return response['result']
        else:
            raise ResponseError(f'IPFS上传接口错误response={response}')


class AsyncIPFS(BaseIPFS):
    is_async = True

    @async_logger('上传IPFS文件')
    async def upload(self, file_path, file_name=None, mode='rb'):
        async with aiohttp.ClientSession() as session:
            if file_name is None:
                file_name = os.path.split(file_path)[-1]
            data = aiohttp.FormData()
            data.add_field(file_name, open(file_path, mode))

            kwargs = self.params_processor(file_path, file_name, mode)
            async with session.post(url=kwargs['url'], data=data) as res:
                res = await res.json()
                print(res)
                return self.response_processor(res)


class IPFS(BaseIPFS):
    @logger('上传IPFS文件')
    def upload(self, file_path, file_name=None, mode='rb'):
        if file_name is None:
            file_name = os.path.split(file_path)[-1]
        res = requests.post(**self.params_processor(file_path, file_name, mode))
        log.debug(res.text)
        result = self.response_processor(res.json())
        return result
