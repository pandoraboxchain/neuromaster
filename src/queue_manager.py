import logging
from threading import *
import logging
import traceback
from collections import namedtuple

from eth_connector import *
from processor import *

QueueManagerConfig = namedtuple('QueueManagerConfig', 'ipfs eth mwapi mnapi ver_ma ver_mi patch agent')

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class QueueManager:

    def __init__(self, config: QueueManagerConfig):
        self.config = config
        self.eth_connector = EthConnector(self.config.eth)

    def run(self):
        self.eth_connector.run()
