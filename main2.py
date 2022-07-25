import sys
import logging
import asyncio
import time

from asyncua import Client, Node, ua

import mqtt_c
from mqtt_c import mqtt
import paho.mqtt.subscribe as subscribe
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
        client_mqtt = mqtt.Client("opc_client")
        # client_mqtt.reinitialise(client_id="opc_client", clean_session=True, userdata=None)
        # client_mqtt.on_connect = mqtt_c.on_connect
        client_mqtt.connect(url, port)
        print(client_mqtt)
        print("MQTT Connected")
        # client_mqtt.subscribe("opc_url")

        return client_mqtt
    except:
        print("mqtt_connection lost !!!")

def onMessage(client, userdata, msg):

    print(msg.topic + ": "+msg.payload.decode())
    return msg.payload.decode()


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
    mqtt_url = "192.168.1.51"
    client_mqtt = await mqtt_connection(mqtt_url, 1883)
    msg = subscribe.simple(topics="opc_url", hostname=mqtt_url)
    opc_url = str(msg.payload.decode())
    print(type(opc_url))
    # client_mqtt.loop_start()
    # client_mqtt.on_message = onMessage
    #
    # time.sleep(1)
    # client_mqtt.loop_stop()
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