import json
from os import path
from collections import namedtuple
from web3 import Web3, HTTPProvider
from data_types import *

EthConfig = namedtuple('EthConfig', 'server port contract abi')


DEFAULT_CONTRACT_ADDR = ''


class EthDelegate:
    def on_neurocontract_created(self, details: NeurocontractDetails):
        pass


class EthConnector:

    def __init__(self, config: EthConfig, delegate: EthDelegate):
        self.config = config
        self.delegate = delegate

        print('Connecting to Ethereum node on %s:%d...' % (self.config.server, self.config.port))
        self.web3 = Web3(HTTPProvider(endpoint_uri="%s:%d" % (self.config.server, self.config.port)))
        print('Ethereum node connected successfully')

        print('Loading ABIs...')
        abi = self.read_abi("Neurochain")
        self.neurocontract_abi = self.read_abi("Neurocontract")
        self.kernel_abi = self.read_abi("KernelContract")
        self.dataset_abi = self.read_abi("DatasetContract")
        print('ABIs loaded successfully')

        print('Getting root contract %s...' % self.config.contract)
        self.root_contract = self.web3.eth.contract(address=self.config.contract, abi=abi)
        self.event_filter = self.root_contract.on('NewNeurocontract')
        print('Root contract instantiated')

    def run(self):
        self.event_filter.start()
        self.event_filter.watch(self.on_neurocontract_created)
        self.event_filter.join()

    def read_abi(self, file: str) -> str:
        here = path.abspath(path.dirname(__file__))
        file = "%s.json" % file
        with open(path.join(here, self.config.abi, file), encoding='utf-8') as f:
            artifact = json.load(f)
        return artifact['abi']

    def get_neurocontract_details(self, addr) -> NeurocontractDetails:
        neurocontract = self.web3.eth.contract(address=addr, abi=self.neurocontract_abi)
        kernel_contract = self.web3.eth.contract(address=neurocontract.call().kernelContract(), abi=self.kernel_abi)
        dataset_contract = self.web3.eth.contract(address=neurocontract.call().datasetContract(), abi=self.kernel_abi)
        arch = kernel_contract.call().ipfsAddress()
        return NeurocontractDetails(
            arch=kernel_contract.call().ipfsAddress(),
            weights=kernel_contract.call().ipfsWeights(),
            data=dataset_contract.call().ipfsAddress(),
            count=7, #dataset_contract.call().sampleCount(),
            addr=addr
        )

    def on_neurocontract_created(self, event: dict):
        address = event['args']['contractAddress']
        print('Got new neurocontract %s' % address)
        self.delegate.on_neurocontract_created(self.get_neurocontract_details(address))
