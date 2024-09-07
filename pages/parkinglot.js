import React, { useState, useEffect } from 'react';
import Parkinglot1 from '@/components/parkinglot1';  // Correct component name

const initialSpotsData = [
  { id: 1, isFree: true },
  { id: 2, isFree: false },
  { id: 3, isFree: true },
  { id: 4, isFree: false },
  { id: 5, isFree: true },
];

const ParkinglotPage = () => {
  const [parkingSpots, setParkingSpots] = useState(initialSpotsData);

  useEffect(() => {
    const interval = setInterval(() => {
      setParkingSpots((prevSpots) =>
        prevSpots.map((spot) => ({
          ...spot,
          isFree: Math.random() > 0.5,  // Simulate real-time availability changes
        }))
      );
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  // Map parkingSpots to individual slot values
  const [slot1, slot2, slot3, slot4, slot5] = parkingSpots.map(spot => spot.isFree);

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
