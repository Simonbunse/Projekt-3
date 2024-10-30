import { mongooseConnect } from "@/lib/mongoose";
import { ParkDataAus } from "@/models/ParkDataAus";

export default async function handler(req, res) {
    await mongooseConnect();
  
    if (req.method !== 'POST' && req.method !== 'GET') {
      res.status(405).json({ message: 'Only POST and GET requests are allowed' });
      return;
    }
  
    if (req.method === 'POST') {
      const { DeviceId, data } = req.body;
  
      const arrivalDate = new Date(data[0].ArrivalTime + " GMT-0000"); // Treat as UTC
      let departureDate = new Date(data[1].DepartureTime + " GMT-0000"); // Treat as UTC
  
      // Check if the departure time is exactly midnight
      if (departureDate.getUTCHours() === 0 && departureDate.getUTCMinutes() === 0 && departureDate.getUTCSeconds() === 0) {
          // Subtract one second
          departureDate = new Date(departureDate.getTime() - 1000);
      }
  
      const formattedDate = arrivalDate.toISOString().split('T')[0]; // Get the YYYY-MM-DD format
      const dateTimeStart = `${formattedDate}T00:00:00`; // Start of the day in ISO format
      const dateTimeEnd = `${formattedDate}T23:59:59`; // End of the day in ISO format
  
      const existingParkData = await ParkDataAus.findOne({ dateTimeStart, DeviceId });
  
      if (existingParkData) {
        const lineItem = {
          ArrivalTime: arrivalDate.toISOString(),
          DepartureTime: departureDate.toISOString(),
          VehiclePresent: data[2]?.VehiclePresent,
        };
  
        await ParkDataAus.updateOne(
          { _id: existingParkData._id },
          { $push: { line_items: lineItem } }
        );
  
        res.status(200).json({ message: 'Data updated successfully', data: existingParkData });
      } else {
        const newParkData = new ParkDataAus({
          DeviceId,
          dateTimeStart, 
          dateTimeEnd,   
          line_items: [],
        });
  
        const lineItem = {
          ArrivalTime: arrivalDate.toISOString(),
          DepartureTime: departureDate.toISOString(), 
          VehiclePresent: data[2]?.VehiclePresent,
        };
  
        newParkData.line_items.unshift(lineItem);
  
        await newParkData.save();
  
        res.status(201).json({ message: 'Data added successfully', data: newParkData });
      }
    }
  }
