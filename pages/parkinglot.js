import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Parkinglot1 from '../components/parkinglot1';

const socket = io();

const ParkinglotPage = () => {
  const [parkingSpots, setParkingSpots] = useState([]);

  useEffect(() => {
    socket.on('parkingSpotsUpdate', (data) => {
      console.log('Received IoT data:', data);
      const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
      setParkingSpots(parsedData);
    });


    return () => {
      socket.off('parkingSpotsUpdate');
    };
  }, []);

  const [slot1 = false, slot2 = false, slot3 = false, slot4 = false, slot5 = false] = parkingSpots.map(spot => spot.isFree || false);

  return (
    <div className="flex flex-col justify-center items-center">
      <h1>Parking Lot Availability</h1>
      <Parkinglot1 
        slot1={slot1} 
        slot2={slot2} 
        slot3={slot3} 
        slot4={slot4} 
        slot5={slot5} 
      />
    </div>
  );
};

export default ParkinglotPage;
