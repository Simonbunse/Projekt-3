import { model, models, Schema } from "mongoose";

const parkDataAusSchema = new Schema({
  line_items: Object,
  DeviceId: { type: String, required: true },
  dateTimeStart: { type: String, required: true },
  dateTimeEnd: { type: String, required: true }
}, { timestamps: true });

export const ParkDataAus = models?.ParkDataAus || model('ParkDataAus', parkDataAusSchema);
