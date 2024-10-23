// lib/mqtt.js
import mqtt from 'mqtt';

export function handleMessage(message, setParkingSpots) {
  try {
    const formattedMessage = message.replace(/([{,])([a-zA-Z0-9_]+)(:)/g, '$1"$2"$3');
    const data = JSON.parse(formattedMessage);
    setParkingSpots(data.spots || []);
  } catch (e) {
    console.error('Error parsing MQTT message:', e);
  }
}

export function connectToBroker(topic, setParkingSpots) {
  const user = process.env.MQTT_USER;
  const password = process.env.MQTT_PASS;

  const client = mqtt.connect('mqtt://79.171.148.142:9001', {
    username: user,
    password: password,
  });

  client.on('connect', () => {
    console.log('Connected to MQTT broker'); // Log successful connection
    client.subscribe(topic, (err) => {
      if (err) {
        console.error('Subscription error:', err);
      }
    });
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
