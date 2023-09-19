from typing import (  # noqa: F401
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from web3.exceptions import BadResponseFormat
from web3.middleware import request_parameter_normalizer, gas_price_strategy_middleware, name_to_address_middleware, \
    attrdict_middleware, validation_middleware, abi_middleware, buffered_gas_estimate_middleware, \
    async_gas_price_strategy_middleware, async_buffered_gas_estimate_middleware
from web3.providers.async_base import AsyncBaseProvider
from web3.types import (  # noqa: F401
    Middleware,
    MiddlewareOnion,
    RPCEndpoint,
    RPCResponse,
)
from web3.manager import RequestManager, apply_error_formatters, NULL_RESPONSES, apply_null_result_formatters

from core.web3.middleware.pythonic import pythonic_middleware, async_pythonic_middleware

if TYPE_CHECKING:
    from web3 import Web3  # noqa: F401


class RequestManager(RequestManager):

    def __init__(self, *args, **kwargs):
        self.raw_provider = args[1]
        super().__init__(*args, **kwargs)

    @staticmethod
    def formatted_response(
        response: RPCResponse,
        params: Any,
        error_formatters: Optional[Callable[..., Any]] = None,
        null_result_formatters: Optional[Callable[..., Any]] = None,
    ) -> Any:
        if "error" in response and response['error'] is not None:
            apply_error_formatters(error_formatters, response)
            raise ValueError(response["error"])
        # NULL_RESPONSES includes None, so return False here as the default
        # so we don't apply the null_result_formatters if there is no 'result' key
        elif response.get('result', False) in NULL_RESPONSES:
            # null_result_formatters raise either a BlockNotFound
            # or a TransactionNotFound error, depending on the method called
            apply_null_result_formatters(null_result_formatters, response, params)
            return response['result']
        elif response.get('result') is not None:
            return response['result']
        else:
            raise BadResponseFormat(
                "The response was in an unexpected format and unable to be parsed. "
                f"The raw response is: {response}"
            )

    # @staticmethod
    def default_middlewares(
            self,
            web3: 'Web3'
    ) -> List[Tuple[Middleware, str]]:
        """
        List the default middlewares for the request manager.
        Leaving ens unspecified will prevent the middleware from resolving names.
        """
        print(isinstance(self.raw_provider, AsyncBaseProvider))
        print(type(self.raw_provider))

        # return [
        #     (request_parameter_normalizer, 'request_param_normalizer'),  # Delete
        #     (gas_price_strategy_middleware, 'gas_price_strategy'),
        #     (name_to_address_middleware(web3), 'name_to_address'),  # Add Async
        #     (attrdict_middleware, 'attrdict'),  # Delete
        #     (pythonic_middleware, 'pythonic'),  # Delete
        #     (validation_middleware, 'validation'),
        #     (abi_middleware, 'abi'),  # Delete
        #     (buffered_gas_estimate_middleware, 'gas_estimate'),
        # ]
        return [
            (async_gas_price_strategy_middleware, 'gas_price_strategy'),
            (async_pythonic_middleware, 'pythonic'),  # Delete
            (async_buffered_gas_estimate_middleware, 'gas_estimate'),
        ]

    @staticmethod
    def default_async_middlewares(
            web3: 'Web3'
    ) -> List[Tuple[Middleware, str]]:
        """
        List the default middlewares for the request manager.
        Leaving ens unspecified will prevent the middleware from resolving names.
        """
        return [
            (async_gas_price_strategy_middleware, 'gas_price_strategy'),
            (async_pythonic_middleware, 'pythonic'),  # Delete
            (async_buffered_gas_estimate_middleware, 'gas_estimate'),
        ]
