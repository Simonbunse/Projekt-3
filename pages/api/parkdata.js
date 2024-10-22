import { mongooseConnect } from "@/lib/mongoose";
import { ParkData } from "@/models/ParkData";

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ message: 'Only POST requests are allowed' });
    return;
  }

  const { parkingLotName, timestamp, spots } = req.body;

  await mongooseConnect();

  const dateTimeStart = new Date(timestamp + "Z");
  const oneHourLater = new Date(dateTimeStart.getTime() + 60 * 60 * 1000);  // for fallback

  // Find if a document already exists for the hour
  const existingParkData = await ParkData.findOne({
    parkingLotName,
    dateTimeStart: {
      $lte: dateTimeStart.toISOString(),
    },
    dateTimeEnd: {
      $gte: dateTimeStart.toISOString(),
    },
  });

  if (existingParkData) {
    const documentEnd = existingParkData.dateTimeEnd; // Use the document's end time for the hour

    // Create a new spot entry with the document's dateTimeEnd as the default end time
    const newSpotEntry = {
      spots: spots,
      timeline: {
        start: dateTimeStart.toISOString(),
        end: documentEnd,  // Set the default end time to the document's dateTimeEnd
      },
    };

    // Update the end time of the previous entry in the line_items
    const lastItem = existingParkData.line_items[existingParkData.line_items.length - 1];
    console.log("Last item in line_items:", lastItem);
    if (lastItem) {
      await ParkData.updateOne(
        { _id: existingParkData._id, "line_items.timeline.start": lastItem.timeline.start },
        { $set: { "line_items.$.timeline.end": dateTimeStart.toISOString() } }
      );
    }

    // Add the new entry with the current start time and document's end time
    try {
      await ParkData.updateOne(
        { _id: existingParkData._id, "line_items.timeline.start": lastItem.timeline.start },
        { $push: { line_items: newSpotEntry } }
      );
      
      res.status(200).json({ message: 'Updated successfully' });
    } catch (error) {
      console.error('Error updating ParkData:', error);
      res.status(500).json({ message: 'Error updating document', error });
    }

  } else {
    // Create a new document if none exists for the hour
    const newParkData = new ParkData({
      parkingLotName,
      dateTimeStart: dateTimeStart.toISOString(),
      dateTimeEnd: oneHourLater.toISOString(),  // New document, so we set dateTimeEnd to one hour later
      line_items: [{
        spots: spots,
        timeline: {
          start: dateTimeStart.toISOString(),
          end: oneHourLater.toISOString(),  // Set the end time to one hour later as a fallback for new document
        },
      }],
    });

    try {
      const savedParkData = await newParkData.save();
      res.status(201).json(savedParkData);
    } catch (error) {
      console.error('Error creating new document:', error);
      res.status(500).json({ message: 'Error creating new document', error });
    }
  }
}
