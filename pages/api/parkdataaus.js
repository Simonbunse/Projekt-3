// pages/api/parkdataaus.js
import { mongooseConnect } from "@/lib/mongoose";
import { ParkDataAusTests } from "@/models/ParkDataAusTests";

export default async function handler(req, res) {
  await mongooseConnect();

  if (req.method !== 'POST') {
    res.status(405).json({ message: 'Only POST requests are allowed' });
    return;
  }

  const { deviceId, timestamp, streetName, betweenStreet1, betweenStreet2, vehiclePresent } = req.body;

  if (!deviceId || !timestamp || !streetName || !betweenStreet1 || !betweenStreet2 || vehiclePresent === undefined) {
    res.status(400).json({ message: 'Missing required fields in request body' });
    return;
  }

  const dateStart = new Date(timestamp).toISOString().split('T')[0];
  const dateTimeStart = `${dateStart}T00:00:00Z`;
  const dateTimeEnd = `${dateStart}T23:59:59.999999Z`;

  const existingDocument = await ParkDataAusTests.findOne({ DeviceId: deviceId, dateTimeStart });

  if (existingDocument) {
    console.log('Document already exists');

    const lineItems = existingDocument.line_items;

    if (!lineItems || lineItems.length === 0) {
      res.status(500).json({ message: 'Existing document has no line items to reference' });
      return;
    }

    // Exclude the last placeholder object from timestamp validation
    const lastValidLineItem = lineItems[lineItems.length - 2] || lineItems[lineItems.length - 1];

    // Validate that the new timestamp is later than the previous DepartureTime
    if (new Date(timestamp) <= new Date(lastValidLineItem.DepartureTime)) {
      res.status(400).json({
        message: `Invalid timestamp: ${timestamp} is earlier than or equal to the previous DepartureTime: ${lastValidLineItem.DepartureTime}`
      });
      return;
    }

    try {
      // Update the placeholder last item with new DepartureTime
      const lastLineItem = lineItems[lineItems.length - 1];
      lastLineItem.DepartureTime = timestamp;
      lastLineItem.VehiclePresent = vehiclePresent;

      // Add a new placeholder line item for the end of the day
      const newLineItem = {
        ArrivalTime: timestamp,
        DepartureTime: dateTimeEnd,
        VehiclePresent: vehiclePresent
      };

      existingDocument.line_items.push(newLineItem);
      await existingDocument.save();

      res.status(200).json({ message: 'New line item added and placeholder updated', data: newLineItem });
    } catch (error) {
      console.error('Error updating document:', error);
      res.status(500).json({ message: 'Error updating document', error });
    }

    return;
  }

  // If no document exists, create a new one
  const initialLineItem = {
    ArrivalTime: dateTimeStart,
    DepartureTime: timestamp,
    VehiclePresent: vehiclePresent
  };

  const placeholderLineItem = {
    ArrivalTime: timestamp,
    DepartureTime: dateTimeEnd,
    VehiclePresent: vehiclePresent
  };

  const newDocument = {
    DeviceId: deviceId,
    dateTimeStart,
    dateTimeEnd,
    StreetName: streetName,
    BetweenStreet1: betweenStreet1,
    BetweenStreet2: betweenStreet2,
    line_items: [initialLineItem, placeholderLineItem]
  };

  try {
    const savedDocument = await ParkDataAusTests.create(newDocument);
    res.status(201).json({ message: 'Document created successfully with initial and placeholder line items', data: savedDocument });
  } catch (error) {
    console.error('Error saving document:', error);
    res.status(500).json({ message: 'Error saving document', error });
  }
}
