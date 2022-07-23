import sys
import logging
import asyncio
import time

from asyncua import Client, Node, ua

import mqtt_c
from mqtt_c import mqtt

var = []
data_dict = {}
async def connection(url):

    try:

        client = Client(url)
        print(await client.connect_and_get_server_endpoints())
        client.session_timeout = 2000
        return client


    except:
        print("error")

async def mqtt_connection(url, port):
    try:
        client_mqtt = mqtt.Client()
        client_mqtt.reinitialise(client_id="opc_client", clean_session=True, userdata=None)
        client_mqtt.on_connect = mqtt_c.on_connect
        client_mqtt.connect(url, port, 60)
        print("Mqtt Connected !!!")
        return client_mqtt
    except:
        print("mqtt_connection lost !!!")

async def node_find(ns_node, client):
    root_id = client.get_root_node()
    children_of_root = await Node.get_children(root_id)
    for i in ns_node:
        var.append(client.get_node(str(i)))
    return var

async def sub_rule_create(client, var):

    for i in var:
        data_dict[await Node.read_browse_name(i)]={
            await Node.read_value(i),


        }



    await asyncio.sleep(1)
    return data_dict

async def main():

    client_mqtt = await mqtt_connection("192.168.1.51", 1883)
    time.sleep(3)
    opc_url = str(client_mqtt.subscribe(topic="opc_url", qos=0, options=None, properties=None))
    print(opc_url)
    client = await connection(opc_url)

    async with client:
        ns = ["ns=3;i=1001", "ns=3;i=1002", "ns=3;i=1003", "ns=3;i=1004"]

        var_last = (await node_find(ns, client))
        print(var_last)
        while True:
            sub_module = await sub_rule_create(client, var_last)
            client_mqtt.publish(topic="opc_data_receive", payload=str(sub_module), qos=0, retain=False, properties=None)
            print(sub_module)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARN)
    asyncio.run(main())