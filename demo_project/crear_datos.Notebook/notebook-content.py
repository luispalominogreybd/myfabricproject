# Fabric notebook source
# Test connection with GitHub

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# CELL ********************

import time
import os
import uuid
import datetime
import random
import json

from azure.eventhub import EventHubProducerClient, EventData

# This script simulates the production of events for 10 devices.
devices = []
for x in range(0, 10):
    devices.append(str(uuid.uuid4()))

# Create a producer client to produce and publish events to the event hub.
producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://udemyeventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XKe+P5l24vfG5OpD7ugQ168p1JJDb/i5x+AEhNQ8nV4=", 
    eventhub_name="udemyeventhub"
    )

for y in range(0,20):    # For each device, produce 20 events. 
    event_data_batch = producer.create_batch() # Create a batch. You will add events to the batch later. 
    for dev in devices:
        # Create a dummy reading.
        reading = {'id': dev, 'timestamp': str(datetime.datetime.utcnow()), 'ratioventas': random.random(), 'manzanas': random.randint(20, 150), 'naranjas': random.randint(50, 80)}
        s = json.dumps(reading) # Convert the reading into a JSON string.
        event_data_batch.add(EventData(s)) # Add event data to the batch.
    producer.send_batch(event_data_batch) # Send the batch of events to the event hub.

# Close the producer.    
producer.cl

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
