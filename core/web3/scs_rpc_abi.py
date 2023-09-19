from web3.types import RPCEndpoint


address = 'address'
uint256 = 'uint256'
uint64 = 'uint64'
string = 'string'


class RPC:
    # scs
    scs_gasPrice = RPCEndpoint('scs_gasPrice')
    scs_protocolVersion = RPCEndpoint('scs_protocolVersion')
    scs_getBalance = RPCEndpoint('scs_getBalance')
    scs_getTransactionCount = RPCEndpoint('scs_getTransactionCount')
    scs_deploy_contract = RPCEndpoint('scs_deploy_contract')
    scs_contractAddressByHash = RPCEndpoint('scs_contractAddressByHash')
    scs_nft_mint = RPCEndpoint('scs_nft_mint')
    scs_nft_mint_alone = RPCEndpoint('scs_nft_mint_alone')
    scs_1155_nft_mint = RPCEndpoint('scs_1155_nft_mint')
    scs_nft_list = RPCEndpoint('scs_nft_list')
    scs_getTokenByHash = RPCEndpoint('scs_getTokenByHash')
    scs_sendTransaction = RPCEndpoint('scs_sendTransaction')
    scs_sendRawTransaction = RPCEndpoint('scs_sendRawTransaction')
    scs_call = RPCEndpoint('scs_call')
    scs_getBlockTransactionCountByHash = RPCEndpoint('scs_getBlockTransactionCountByHash')
    scs_getBlockTransactionCountByNumber = RPCEndpoint('scs_getBlockTransactionCountByNumber')
    scs_getCode = RPCEndpoint('scs_getCode')
    scs_estimateGas = RPCEndpoint('scs_estimateGas')
    scs_getBlockByHash = RPCEndpoint('scs_getBlockByHash')
    scs_getBlockByNumber = RPCEndpoint('scs_getBlockByNumber')
    scs_getTransactionReceipt = RPCEndpoint('scs_getTransactionReceipt')
    scs_getTransactionByHash = RPCEndpoint('scs_getTransactionByHash')
    scs_blockNumber = RPCEndpoint('scs_blockNumber')
    scs_get_evidence_contract_address = RPCEndpoint('scs_get_evidence_contract_address')
    scs_existing_evidence = RPCEndpoint('scs_existing_evidence')
    scs_digital_collection_mint = RPCEndpoint('scs_digital_collection_mint')
    scs_digital_collection_list = RPCEndpoint('scs_digital_collection_list')
    scs_digital_collection_transaction = RPCEndpoint('scs_digital_collection_transaction')
    scs_pangu_evidence = RPCEndpoint('scs_pangu_evidence')
    scs_real_name_auth = RPCEndpoint('scs_real_name_auth')
    scs_get_unionId_mint_count = RPCEndpoint('scs_get_unionId_mint_count')

    # scs nft contract
    ownerOf = RPCEndpoint('ownerOf')
    transferFrom = RPCEndpoint('transferFrom')
    tokenURI = RPCEndpoint('tokenURI')
    totalSupply = RPCEndpoint('totalSupply')

    # scs evidence contract
    evidence = RPCEndpoint('evidence')

    # 4907
    setUser = RPCEndpoint('setUser')
    userOf = RPCEndpoint('userOf')
    userExpires = RPCEndpoint('userExpires')

    # 1155
    safeTransferFrom = RPCEndpoint('safeTransferFrom')
    balanceOf = RPCEndpoint('balanceOf')
    balanceOfBatch = RPCEndpoint('balanceOfBatch')
    verificationNft = RPCEndpoint('verificationNft')


RPC_ABIS = {
    # 'scs_deploy_contract': ['address', 'uint'],
    # 'ownerOf': []
}

RPC_SCS_ABIS = {
    # scs nft contract
    'ownerOf': [uint256],
    'transferFrom': [address, address, uint256],
    'tokenURI': [uint256],
    'evidence': [string, string],
    'setUser': [uint256, address, uint64],
    'userOf': [uint256],
    'userExpires': [uint256],

    'safeTransferFrom': [address, address, uint256, uint256, 'bytes'],
    'balanceOf': [address, uint256],
    'balanceOfBatch': ['address[]', 'uint256[]']
}
