import mqtt from 'mqtt';
import axios from 'axios';

export function handleMessage(message, setParkingSpots) {
  try {
    console.log('raw message:', message);

    // Replace single quotes with double quotes for valid JSON format
    const jsonString = message.replace(/'/g, '"');

    // Parse the JSON string into an object
    const jsonObject = JSON.parse(jsonString);

    console.log('parsed object:', jsonObject);

    // Set parking spots from the parsed object
    setParkingSpots(jsonObject.spots || []);

    // Send the parking lot name and timestamp to the API
    axios.post('http://localhost:3000/api/parkdata', {
      parkingLotName: jsonObject.parkingLotName,
      timestamp: jsonObject.timestamp,
      spots: jsonObject.spots
    })
    .then(response => {
      console.log('Data sent to API successfully:', response.data);
    })
    .catch(error => {
      console.error('Error sending data to API:', error);
    });

  } catch (e) {
    console.error('Error parsing MQTT message:', e);
  }
}

export function connectToBroker(topic, setParkingSpots) {
  const user = process.env.NEXT_PUBLIC_MQTT_USER;
  const password = process.env.NEXT_PUBLIC_MQTT_PASS;

  const client = mqtt.connect('ws://79.171.148.142:9001', {
    username: user,
    password: password,
  });

  client.on('connect', () => {
    console.log('Connected to MQTT broker');
    client.subscribe(topic, (err) => {
      if (err) {
        console.error('Subscription error:', err);
      }
    });
  });

  client.on('error', (err) => {
    console.error('Connection error:', err);
  });

  client.on('message', (receivedTopic, message) => {
    if (receivedTopic === topic) {
      handleMessage(message.toString(), setParkingSpots);
    }
  });

  return function disconnect() {
    client.end();
  };
}
