import sys
import logging
import asyncio
import time
from asyncua import Client, Node, ua
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')
var = []
data_dict = {}
data_send = True
client_mqtt = mqtt.Client("opc_Socket")
mqtt_url = '192.168.1.51'
topic = 'send_opc_tag'


class SubscriptionHandler:

    def event_notification(self, event):
        print(f"{event=}")


async def connection(url):

    try:

        client = Client(url)
        print(await client.connect_and_get_server_endpoints())

        return client


    except:
        print("error")

# async def mqtt_connection(url, port):
#     try:
#         client_mqtt = mqtt.Client("opc_client")
#         # client_mqtt.reinitialise(client_id="opc_client", clean_session=True, userdata=None)
#         # client_mqtt.on_connect = mqtt_c.on_connect
#         client_mqtt.on_connect(url, port)
#         print("MQTT Connected")
#         # client_mqtt.subscribe("opc_url")
#
#         return client_mqtt
#     except:
#         print("mqtt_connection lost !!!")
#
#
def mqtt_sub(mqtt_url, topic):
    try:
        print("HERE")
        print(f"{topic},{mqtt_url}")
        msg = subscribe.simple(topics=topic, hostname=mqtt_url)
        print(msg)
        msg = str(msg.payload.decode())
        return msg

    except:
        print("error")

def on_log(client, userdata, level, buff):  # mqtt logs function
    print(buff)


def on_connect(client, userdata, flags, rc):  # connect to mqtt broker function
    if rc == 0:
        client.connected_flag = True  # set flags
        print("Connected Info")
    else:
        print("Bad connection returned code = " + str(rc))
        client.loop_stop()

def on_subscribe(client, userdata, mid, granted_qos):  # subscribe to mqtt broker
    print("Subscribed", userdata)

def on_publish(client, userdata, mid):  # publish to mqtt broker
    print("In on_pub callback mid=" + str(mid))


def on_message(client, userdata, message):  # get message from mqtt broker
    print("New message received: ", str(message.payload.decode("utf-8")), "Topic : %s ", message.topic, "Retained : %s", message.retain)

def onMessage(client, userdata, msg):

    print(msg.topic + ": "+msg.payload.decode())
    return msg.payload.decode()


async def node_find(ns_node, client):
    root_id = client.get_root_node()
    children_of_root = await Node.get_children(root_id)
    for i in ns_node:
        var.append(client.get_node(str(i)))
    return var

async def sub_rule_create(var):

    for i in var:

        data_dict[i]= {
            await Node.read_value(i)
        }


    await asyncio.sleep(1)
    return data_dict

def connectToMqtt(client=None):  # connect to MQTT broker main function
    print("Connecting to MQTT broker")
    client_mqtt.on_log = on_log
    client_mqtt.on_connect = on_connect
    client_mqtt.on_publish = on_publish
    client_mqtt.on_subscribe = on_subscribe
    client_mqtt.connect("192.168.1.51", 1883, keepalive=600)
    rec = client_mqtt.publish(topic="ready_to_Recieve_opc_topic",qos=0,payload="")
    print("Published = "+ str(rec))
    ret = client_mqtt.subscribe(topic, qos=0)
    for i in ret:
        print(i)
    print("Subscribed return = " + str(ret))
    msg = client_mqtt.subscribe_callback()
    print(msg)

    client_mqtt.on_message = on_message


async def main():

    connectToMqtt()
    # client_mqtt.loop_forever()

    client_mqtt.loop_start()
    # client_mqtt.on_message = onMessage
    #
    # time.sleep(1)
    # client_mqtt.loop_stop()
    client = await connection()
    if client == "error":
        client_mqtt.publish(topic="OPC_ServersConnected", payload=str(msg), qos=0, retain=False, properties=None)
    else:
        client_mqtt.publish(topic="OPC_ServersConnected", payload=str(""), qos=0, retain=False, properties=None)
        print("mqtt_send_opc")
    async with client:
        ns = mqtt_sub(mqtt_url, topic="send_opc_tag")
        print(ns)


        while data_send:
            var_last = (await node_find(ns, client))
            sub_module = await sub_rule_create( var_last)
            client_mqtt.publish(topic="opc_data_receive", payload=str(sub_module), qos=0, retain=False, properties=None)
            print(sub_module)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARN)
    asyncio.run(main())