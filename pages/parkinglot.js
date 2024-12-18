// pages/parkinglot.js
import React, { useState, useEffect } from 'react';
import Parkinglot1 from '../components/parkinglot1';
import { connectToBroker } from '../lib/mqtt'; // Import the functions from mqtt.js
import Layout from '@/components/Layout';

const ParkinglotPage = () => {
  const [parkingSpots, setParkingSpots] = useState(null); // Start with null to indicate loading
  
  // Connect to MQTT when the component mounts
  useEffect(() => {
    const disconnect = connectToBroker('parking/updates', setParkingSpots);
    
    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, []);

  // Show loading state if parking spots are not yet received
  if (!parkingSpots) {
    return (
      <Layout>
        <div className="flex flex-col justify-center items-center">
          <h1>Loading parking lot availability...</h1>
        </div>
      </Layout>
    );
  }

  // Extract slot availability from parkingSpots array
  const [slot1 = false, slot2 = false, slot3 = false, slot4 = false, slot5 = false] = parkingSpots.map(spot => spot.isFree || false);

  return (
    <Layout>
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
    </Layout>
  );
};

export default ParkinglotPage;
