from typing import Callable, Any
from web3 import Web3
from web3._utils.method_formatters import (
    PYTHONIC_REQUEST_FORMATTERS,
)
from web3.middleware.formatting import (
    construct_formatting_middleware, async_construct_formatting_middleware,
)
from web3.types import RPCEndpoint, AsyncMiddleware
from core.web3.method_formatters import PYTHONIC_RESULT_FORMATTERS

# 自定义封装scs pythonic_middleware
formatting_middleware = dict(
    request_formatters=PYTHONIC_REQUEST_FORMATTERS,
    result_formatters=PYTHONIC_RESULT_FORMATTERS,
)


# --- sync -- #
pythonic_middleware = construct_formatting_middleware(**formatting_middleware)


# --- async -- #
async def async_pythonic_middleware(make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3") -> AsyncMiddleware:
    middleware = await async_construct_formatting_middleware(**formatting_middleware)
    return await middleware(make_request, web3)
