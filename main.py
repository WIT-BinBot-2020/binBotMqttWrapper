import paho.mqtt.client as paho

broker = "localhost"
port = 1883

def on_message(client, userdata, message):
    print("message recieved", str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("----------------------------------------------")
client = paho.Client("Client1")
client.on_message=on_message
client.connect(broker, port)
client.subscribe("binBot/#")
client.loop_forever()


