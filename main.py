import sys
import logging
import asyncio
from asyncua import Client, Node, ua
import sub

sys.path.insert(0, "..")
all_dict = {}
i = 0
connection_start = True

async def main():

    try:
        client = Client("opc.tcp://ofathi:53530/OPCUA/SimulationServer")
        print(await client.connect_and_get_server_endpoints())
        client.session_timeout = 2000
    except:
        print("error")

    async with client:

        root_id = client.get_root_node()
        children_of_root = await Node.get_children(root_id)
        start = True




        var = client.get_node("ns=3;i=1001")
        # val = await Node.get_value(var)
        # print(val)
        handler = sub.SubscriptionHandler()


        subscription = await client.create_subscription(1000, handler)
        nodes = [
            var,
            # client.get_node(ua.ObjectIds.Server_ServerStatus_CurrentTime),
        ]
            # We subscribe to data changes for two nodes (variables).

        hello = await subscription.subscribe_data_change(nodes)
        # We let the subscription run for ten seconds
        # await subscription.create_monitored_items(var)
        # We delete the subscription (this un-subscribes from the data changes of the two variables).
        # This is optional since closing the connection will also delete all subscriptions.

        # After one second we exit the Client context manager - this will close the connection.
        await asyncio.sleep(1)
        node_id_to_value_dict = {}
        # for node in var:
        #     # identifier = await node.nodeid.Identifier
        #     browse_Name = await node.read_browse_name()
        #     nodeIdentifier = node.nodeid.Identifier
        #     nodeNamespace = node.nodeid.NamespaceIndex
        #     nodeNamespaceUri = node.nodeid.NamespaceUri
        #     nodeNodeIdType = node.nodeid.NodeIdType
        #     nodeServerIndex = node.nodeid.ServerIndex
        #     nodeParent = await Node.get_parent(node)
        #     print(browse_Name)
        #
        #     base_identifier = 'Identifier = ' + str(nodeIdentifier)
        #     base_namespace = 'Namespace = ' + str(nodeNamespace)
        #
        #     node_id_to_value_dict[node.nodeid] = nodeParent
        #
        # node_id_to_value_dict_str = ua_utils.val_to_string(node_id_to_value_dict)

        await asyncio.sleep(1)

if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARN)
    asyncio.run(main())