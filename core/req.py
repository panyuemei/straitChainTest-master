import hashlib
import json
import time
from json import JSONDecodeError
import requests
from requests import Response
from settings import settings
from core.logger import log
from exceptions import ResponseParseError, ResponseError


def process_response(response: Response, is_raise=True, is_warning_error=True, is_return_all=False, ):
    def return_body(res_data):
        # log.debug(res_data)
        if is_return_all:
            return res_data
        else:
            return res_data['result'] if 'result' in res_data else None

    try:
        res = response.json()
        if 'error' in res and res['error'] is not None:
            if is_raise:
                raise ResponseError(res)
            else:
                if is_warning_error:
                    log.warning(res)
                else:
                    log.debug(res)
                return return_body(res)
        else:
            log.debug(res)
            return return_body(res)

    except JSONDecodeError:
        raise ResponseParseError(response.text)


def req_nft(method: str,
            params=None,
            req_method='POST',
            req_url=settings.chain_url,
            req_headers=settings.headers,
            app_key=settings.app_key,
            req_body_id=None,
            need_md5=False,
            is_raise=True,
            is_warning_error=True,
            is_return_all=False,
            timeout=20
            ):
    """
    请求封装
    :param method: 接口方法
    :param params: 接口参数：dict
    :param req_method: 请求方法
    :param req_url: 请求链接
    :param req_headers: 请求头
    :param app_key: appKey
    :param req_body_id: 请求标识 返回一致（标识同一个请求）
    :param need_md5: 是否需要md5加密
    :param is_raise: 异常是否抛出错误
    :param is_warning_error: 不抛出错误时，是否需要打印错误
    :param is_return_all: 是否返回全部数据
    :param timeout: 接口请求超时时间
    :return:
    """
    data = {
        'jsonrpc': settings.jsonrpc,
        'method': method,
        'params': params_handler(params if params is not None else {}, need_md5, app_key),
        'id': round(time.time() * 1000) if req_body_id is None else req_body_id
    }
    log.debug(data)
    res = requests.request(req_method, req_url, data=json.dumps(data), headers=req_headers, timeout=timeout)
    return process_response(res, is_raise=is_raise, is_warning_error=is_warning_error, is_return_all=is_return_all)


def get_params_list(params):
    """
    当传入dict时，按顺序取value组成列表
    当传入list或tuple时，直接返回
    其余，将值组合为列表的index=0
    :param params:
    :return:
    """
    if isinstance(params, dict):
        params_list = list(map(lambda x: '' if x is None else x, [val for idx, val in params.items()]))
    elif not (isinstance(params, list) or isinstance(params, tuple)):
        params_list = [params]
    else:
        params_list = params
    return params_list


def params_handler(params, need_md5=False, app_key=None):
    params = get_params_list(params)
    if need_md5:
        if app_key is None:
            raise ValueError('需要md5加密时，app_key不可为空')
        params = [str(param) for param in params]
        params_str = '&'.join(params + [app_key])
        params_md5 = hashlib.md5(params_str.encode('utf-8')).hexdigest()
        params.append(params_md5)
    return params


if __name__ == '__main__':
    ...
