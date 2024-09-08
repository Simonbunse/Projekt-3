import socketio
import random
import json
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to WebSocket server")

@sio.event
def disconnect():
    print("Disconnected from WebSocket server")

def send_data():
    while True:
        # Generate random parking spot data
        parking_spots = [
            {"id": 1, "isFree": random.choice([True, False])},
            {"id": 2, "isFree": random.choice([True, False])},
            {"id": 3, "isFree": random.choice([True, False])},
            {"id": 4, "isFree": random.choice([True, False])},
            {"id": 5, "isFree": random.choice([True, False])},
        ]
        
        # Convert to JSON and send
        data = json.dumps(parking_spots)
        sio.emit('iotData', data)
        print(f"Sent data: {data}")
        
        # Wait for a bit before sending the next update
        time.sleep(5)  # Adjust the delay as needed

# Connect to the WebSocket server
sio.connect('http://localhost:3000')
send_data()
