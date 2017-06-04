import logging
import json
from os import path
from collections import namedtuple
from web3 import Web3, HTTPProvider


EthConfig = namedtuple('EthConfig', 'server port contract abi')

DEFAULT_CONTRACT_ADDR = ''


def read_abi(file: str) -> str:
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, file), encoding='utf-8') as f:
        abi = json.load(f)
    return abi


def on_neurocontract_created(address: str):
    print('Got new neurocontract %s' % address)


class EthConnector:

    def __init__(self, config: EthConfig):
        self.config = config
        print('Connecting to Ethereum node on %s:%d...' % (self.config.server, self.config.port))
        self.web3 = Web3(HTTPProvider(endpoint_uri="%s:%d" % (self.config.server, self.config.port)))
        print('Ethereum node connected successfully')
        print('Getting root contract %s...' % self.config.contract)
        abi = read_abi(self.config.abi)
        self.root_contract = self.web3.eth.contract(address=self.config.contract, abi=abi)
        self.event_filter = self.root_contract.on('NewNeurocontract')
        print('Root contract ABI instantiated')

    def run(self):
        self.event_filter.start()
        self.event_filter.join()
        self.event_filter.watch(on_neurocontract_created)

