import { mongooseConnect } from "@/lib/mongoose";
import { ParkData } from "@/models/ParkData";

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ message: 'Only POST requests are allowed' });
    return;
  }

  const { parkingLotName, timestamp, spots } = req.body;

  await mongooseConnect();

  const dateTimeStart = new Date(timestamp + "Z"); // Appending 'Z' treats it as UTC
  const dateTimeEnd = new Date(dateTimeStart.getTime() + 60 * 60 * 1000);

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

    const newSpotEntry = {
      spots: spots,
    };

    try {
      await ParkData.updateOne(
        { _id: existingParkData._id },
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
      dateTimeEnd: dateTimeEnd.toISOString(),
      line_items: [{ spots: spots }],
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
