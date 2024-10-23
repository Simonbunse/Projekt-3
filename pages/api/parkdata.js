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
  const oneHourLater = new Date(dateTimeStart.getTime() + 60 * 60 * 1000);
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
    const documentEnd = existingParkData.dateTimeEnd;
    const newSpotEntry = {
      spots: spots,
      timeline: {
        start: dateTimeStart.toISOString(),
        end: documentEnd,
      },
    };
    const lastItem = existingParkData.line_items[existingParkData.line_items.length - 1];
    if (lastItem) {
      await ParkData.updateOne(
        { _id: existingParkData._id, "line_items.timeline.start": lastItem.timeline.start },
        { $set: { "line_items.$.timeline.end": dateTimeStart.toISOString() } }
      );
    }

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
    const newParkData = new ParkData({
      parkingLotName,
      dateTimeStart: dateTimeStart.toISOString(),
      dateTimeEnd: oneHourLater.toISOString(),
      line_items: [{
        spots: spots,
        timeline: {
          start: dateTimeStart.toISOString(),
          end: oneHourLater.toISOString(),
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
