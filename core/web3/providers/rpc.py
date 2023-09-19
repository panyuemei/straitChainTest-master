from typing import Any
from web3 import HTTPProvider as SourceHTTPProvider
from web3._utils.request import make_post_request
from web3.types import RPCEndpoint, RPCResponse


class HTTPProvider(SourceHTTPProvider):
    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        self.logger.debug(f'>>> Method: {method}, params: {params}')
        request_data = self.encode_rpc_request(method, params)
        # noinspection PyArgumentList
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug(f'<<< Method: {method}, Response: {response}')
        return response
