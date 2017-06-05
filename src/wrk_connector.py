import time
from concurrent import futures
from collections import namedtuple
from data_types import *

from neuromwapi.messages import *
from neuromwapi.services import *


MWAPIConfig = namedtuple('MWAPIConfig', 'host port max_conns')

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class WrkConnector:
    """Provides methods that implement functionality for masternode worker endpoint (MWAPI)"""

    def __init__(self, config: MWAPIConfig):
        self.config = config
        channel = grpc.insecure_channel('%s:%d' % (self.config.host, self.config.port))
        self.stub = WorkerStub(channel)

    def worker_ping(self, ver: Version) -> VersionInfo:
        print('Pinging worker...')
        resp = self.stub.ping(VersionInfo(major=ver.major, minor=ver.minor, patch=ver.patch, agent=ver.agent))
        print('Got version %d.%d.%d; worker is powered by %s' % (resp.major, resp.minor, resp.patch, resp.agent))
        return resp

    def worker_cognite_batch(self, details: NeurocontractDetails, key: str, msg: str) -> CognitionResponse:
        print('Sending batch of work for cognition...')
        req = CognitionRequest(arch_address=details.arch,
                               model_address=details.weights,
                               data_address=details.data,
                               samples_count=details.count,
                               pub_key=key,
                               signed_message=msg,
                               contract_address=details.addr)
        resp = self.stub.cognite_batch(req)
        if resp.accepted:
            print('Batch accepted, task id %s, estimated time %d' %
                  (resp.task_info.task_id, resp.task_info.time_estimate))
        else:
            print('Batch rejection, reason #%d: %s' %
                  (resp.decline_info.reason, resp.decline_info.message))
        return resp
