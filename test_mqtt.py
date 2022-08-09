import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('192.168.1.51', 1883)

def on_connect(client, userdata, flags, rc):
    print("Connected to a broker!")
    client.publish("ready_to_Recieve_opc_topic", "")
    client.subscribe("OPC_Servers_Try_Connection")

def on_message(client, userdata, message):
    print(message.payload.decode())

while True:
    client.on_connect = on_connect

    client.on_message = on_message
    client.loop_forever()