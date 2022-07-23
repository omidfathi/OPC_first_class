import sys
sys.path.insert(0, "..")
import os
# os.environ['PYOPCUA_NO_TYPO_CHECK'] = 'True'
import asyncio
import logging
from asyncua import Client, Node, ua
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


class SubscriptionHandler:
    dataa = []
    async def datachange_notification(self, node: Node, val, data):

        # _logger.info('datachange_notification %r %s', node, val)
        print(node)
        print(val)
        dataa = data
        print(dataa)
