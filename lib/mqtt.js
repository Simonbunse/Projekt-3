// lib/mqtt.js
import mqtt from 'mqtt';

// Function to handle incoming MQTT messages
export function handleMessage(message, setParkingSpots) {
    // Try parsing the message as is
    try {
      // Replace unquoted keys with quoted keys to form valid JSON
      const formattedMessage = message.replace(/([{,])([a-zA-Z0-9_]+)(:)/g, '$1"$2"$3');
      const data = JSON.parse(formattedMessage);
      setParkingSpots(data.spots || []);
    } catch (e) {
      console.error('Error parsing MQTT message:', e);
    }
  }

// Function to connect to the MQTT broker and handle messages
export function connectToBroker(topic, setParkingSpots) {
  const client = mqtt.connect('mqtt://79.171.148.142:9001'); // WebSocket over SSL

  client.on('connect', () => {
    console.log('Connected to MQTT broker');
    client.subscribe(topic, (err) => {
      if (err) {
        console.error('Subscription error:', err);
      }
    });
  });

  client.on('message', (receivedTopic, message) => {
    if (receivedTopic === topic) {
      handleMessage(message.toString(), setParkingSpots); // Call the message handler
    }
  });

  // Cleanup function to disconnect the client
  return function disconnect() {
    client.end();
  };
}
