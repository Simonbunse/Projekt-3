import mqtt from 'mqtt';
import axios from 'axios';

export function handleMessage(message, setParkingSpots) {
  try {
    console.log('raw message:', message);

    // Replace single quotes with double quotes for valid JSON format
    const jsonString = message.replace(/'/g, '"');
    console.log('JSON string after replacement:', jsonString);

    // Parse the JSON string into an object
    const jsonObject = JSON.parse(jsonString);
    console.log('parsed object:', jsonObject);

    // Set parking spots from the parsed object
    setParkingSpots(jsonObject.spots || []);
    console.log('Updated parking spots:', jsonObject.spots);

    // Send the parking lot name and timestamp to the API
    axios.post('http://localhost:3001/api/parkdata', {
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
  const mqttip = process.env.NEXT_PUBLIC_MQTT_IP;

  console.log('Connecting to MQTT broker...');
  console.log('MQTT URI:', mqttip);
  console.log('Username:', user);

  const client = mqtt.connect(mqttip, {
    username: user,
    password: password,
  });

  client.on('connect', () => {
    console.log('Connected to MQTT broker');
    client.subscribe(topic, (err) => {
      if (err) {
        console.error('Subscription error:', err);
      } else {
        console.log(`Subscribed to topic: ${topic}`);
      }
    });
  });

  client.on('error', (err) => {
    console.error('Connection error:', err);
  });

  client.on('message', (receivedTopic, message) => {
    console.log(`Message received on topic: ${receivedTopic}`);
    console.log('Raw message content:', message.toString());
    
    if (receivedTopic === topic) {
      handleMessage(message.toString(), setParkingSpots);
    } else {
      console.log(`Ignored message from topic: ${receivedTopic}`);
    }
  });

  return function disconnect() {
    console.log('Disconnecting from MQTT broker...');
    client.end();
  };
}
