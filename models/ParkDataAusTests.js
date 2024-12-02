import { model, models, Schema } from "mongoose";

const lineItemSchema = new Schema({
  ArrivalTime: { type: String, required: true },
  DepartureTime: { type: String, required: true },
  VehiclePresent: { type: Boolean, required: true }
}, { _id: false });

const parkDataAusTestsSchema = new Schema({
  DeviceId: { type: String, required: true },
  dateTimeStart: { type: String, required: true },
  dateTimeEnd: { type: String, required: true },
  StreetName: { type: String, required: true },
  BetweenStreet1: { type: String, required: true },
  BetweenStreet2: { type: String, required: true },
  line_items: [lineItemSchema],
}, { timestamps: true });

export const ParkDataAusTests = models?.ParkDataAusTests || model('ParkDataAusTests', parkDataAusTestsSchema);
