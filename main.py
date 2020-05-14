from influxdb import InfluxDBClient
import paho.mqtt.client as paho
from datetime import datetime
from threading import Thread
import json
import requests

# Define broker and port to listen to
broker = "localhost"
port = 1883

#slackUrl = "https://hooks.slack.com/services/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"
#slackHeader = "Content-type: application/json"

def post_message(data):
    slackUrl = "https://hooks.slack.com/services/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"
    slackHeader = {"Content-type": "application/json"}
    data = {"text": data["message"]}
    slackPayload = json.dumps(data)
    x = requests.post(slackUrl, data=slackPayload, headers=slackHeader)

#function called when a message is recieved
def on_message(client, userdata, message):

    # Print data
    print("message recieved", str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("----------------------------------------------")
    # Start new thread - Insert data into db
    p = Thread(target=insert, args=(message.payload, message.topic,))
    p.start()
    p.join()

# Function to insert data into influxdb
def insert(data, measurement):

    # Get the measurement
    measurement = measurement.split("/")[1]

    if(measurement == "messages"):
        post_message(json.loads(data.decode("utf-8")))

    # Generate the json body to insert
    json_body = [
            {
            "measurement" : measurement,
            "tags": {
                },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                },
            }
        ]

    # Add the payload data to the insert json
    json_body[0]["fields"] = json.loads(data.decode("utf-8"))
    print(json_body)

    # Write data to the database
    dbClient.write_points(json_body)
        
# Connect to the database
dbClient = InfluxDBClient(host="localhost", port=8086, database="BinBotStats", username='binbot', password='b33pb00p!!')

# Create a mqtt client
client = paho.Client("Client1")

# Define which function to call when message is recived
client.on_message=on_message

# Connect to the database
client.connect(broker, port)

# Subscribe to all of the messages on the binBot base topic
client.subscribe("binBot/#")

# Loop forever
client.loop_forever()


