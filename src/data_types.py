from collections import namedtuple

Version = namedtuple('Version', 'major minor patch agent')

NeurocontractDetails = namedtuple('NeurocontractDetails', 'arch weights data count addr')
