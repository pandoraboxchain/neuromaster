from collections import namedtuple

from eth_connector import *
from processor import *

QueueManagerConfig = namedtuple('QueueManagerConfig', 'ipfs eth mwapi mnapi version')


class QueueManager(EthDelegate):

    def __init__(self, config: QueueManagerConfig):
        self.config = config
        self.eth_connector = EthConnector(self.config.eth, self)
        self.processors = []

    def run(self):
        self.eth_connector.run()

    def on_neurocontract_created(self, details: NeurocontractDetails):
        processor = Processor(ProcessorConfig(
            eth=self.config.eth,
            ipfs=self.config.ipfs,
            mwapi=self.config.mwapi,
            version=self.config.version
        ))
        self.processors.append(processor)
        processor.run()
        processor.process_new_contract(details)
