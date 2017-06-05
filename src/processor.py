import logging
from threading import *
from collections import namedtuple
from data_types import *
from wrk_connector import *
from ipfs_connector import *


ProcessorConfig = namedtuple('ProcessorConfig', 'eth ipfs mwapi version')

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Processor(Thread):

    def __init__(self, config: ProcessorConfig):
        super().__init__()
        self.config = config
        self.wrk_connector = WrkConnector(self.config.mwapi)

    def run(self):
        super().run()
        self.wrk_connector.worker_ping(self.config.version)

    def process_new_contract(self, details: NeurocontractDetails):
        self.wrk_connector.worker_cognite_batch(details, key='', msg='')
