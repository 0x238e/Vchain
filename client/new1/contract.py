#!/usr/bin/python3
import json
from cpc_fusion import Web3
from solc import compile_source
from cpc_fusion.contract import ConciseContract

def update(data,myaddr):
    data=json.dumps(data)
    # Solidity source code
    contract_source_code = '''
    pragma solidity ^0.4.24;

    contract Dumper {
        string public dumping;
        event test(address who,string a);
        function Dumper() public {
            dumping = '';
        }

        function setDumping(string _dumping) public {
            emit test(msg.sender,_dumping);
            dumping = _dumping;
        }

        function dump() view public returns (string) {
            return dumping;
        }
    }
    '''
    print(contract_source_code)

    compiled_sol = compile_source(contract_source_code)  # Compiled source code
    contract_interface = compiled_sol['<stdin>:Dumper']

    # web3.py instance
    w3 = Web3(Web3.HTTPProvider('http://3.1.81.79:8501'))

    # set pre-funded account as sender
    w3.cpc.defaultAccount = w3.cpc.accounts[0]

    # Instantiate and deploy contract
    Dumper = w3.cpc.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Submit the transaction that deploys the contract
    # your keypath
    # change the keypath to your keystore file
    keypath = "./UTC--2019-04-20T23-24-36.068766100Z--4ccd5762896ae5075808b2cd03599d487e1f33e0"
    # your password
    password = "123456"
    # your account address
    from_addr = w3.toChecksumAddress(myaddr)
    tx_hash = Dumper.constructor().raw_transact({
        # Increase or decrease gas according to contract conditions
        'gas': 819776,
        'from': from_addr,
        'value': 0
    }, keypath, password, 42)
    # tx_hash = Dumper.constructor().transact()

    # print('*********',w3.cpc.getTransactionReceipt(tx_hash_raw))
    print('*********', w3.cpc.getTransactionReceipt(tx_hash))

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.cpc.waitForTransactionReceipt(tx_hash)
    # tx_receipt1 = w3.cpc.waitForTransactionReceipt(tx_hash_raw)
    print(tx_receipt)
    # print(tx_receipt1)

    # Create the contract instance with the newly-deployed address
    dumper = w3.cpc.contract(
        address=tx_receipt.contractAddress,
        abi=contract_interface['abi'],
    )

    # Display the default dumping from the contract
    print('Default contract dumping: {}'.format(
        dumper.functions.dump().call()
    ))

    print('Setting the dumping ...')
    tx_hash = dumper.functions.setDumping(data).raw_transact({
        'gas': 300000,
        'from':from_addr,
        'value': 0,
    },keypath,password,42)

    # Wait for transaction to be mined...
    w3.cpc.waitForTransactionReceipt(tx_hash)

    # Display the new dumping value
    print('Updated contract dumping: {}'.format(
        dumper.functions.dump().call()
    ))

    # When issuing a lot of reads, try this more concise reader:
    reader = ConciseContract(dumper)
    assert reader.dump() == data
if __name__ == '__main__':
    update([1])
