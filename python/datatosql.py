import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient("mongodb+srv://simonhastrupjensen:TvrLm9gVK7ahWEPt@cluster0.e3e1e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.Cluster0
collection = db.ParkDataAusTest

# Read CSV in chunks to avoid memory issues
chunks = pd.read_csv(r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\data\Car_Parking_Sensor_Data_123.csv", chunksize=10000)

# Helper function to process each chunk and reformat data
def process_chunk(chunk):
    # Convert Arrival and Departure times to datetime and add a new column for the day
    chunk["ArrivalTime"] = pd.to_datetime(chunk["ArrivalTime"], format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
    chunk["DepartureTime"] = pd.to_datetime(chunk["DepartureTime"], format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
    chunk["Day"] = chunk["ArrivalTime"].dt.date  # Extract the day for grouping

    # Group by DeviceId and Day to create daily documents
    grouped = chunk.groupby(["DeviceId", "Day"])

    # Process each group
    for (device_id, day), group in grouped:
        # Define dateTimeStart and dateTimeEnd for the document
        date_time_start = datetime.combine(day, datetime.min.time()).isoformat() + "Z"
        date_time_end = (datetime.combine(day, datetime.max.time()) - timedelta(seconds=1)).isoformat() + "Z"

        # Get unique values for the additional fields
        street_name = group["StreetName"].iloc[0]  # Assuming consistent value within the group
        between_street1 = group["BetweenStreet1"].iloc[0]  # Assuming consistent value within the group
        between_street2 = group["BetweenStreet2"].iloc[0]  # Assuming consistent value within the group

        # Prepare line items for each entry within the day
        line_items = [
            {
                "ArrivalTime": row["ArrivalTime"].isoformat(),
                "DepartureTime": row["DepartureTime"].isoformat(),
                "VehiclePresent": row["VehiclePresent"],
            }
            for _, row in group.iterrows()
        ]

        # Convert device_id to Python int
        device_id = int(device_id)

        # Check if there's already a document for this device on this day
        existing_doc = collection.find_one({"DeviceId": device_id, "dateTimeStart": date_time_start})

        if existing_doc:
            # Update existing document with additional line items
            collection.update_one(
                {"_id": existing_doc["_id"]},
                {"$push": {"line_items": {"$each": line_items}}}
            )
        else:
            # Create a new document for this device and day
            new_doc = {
                "DeviceId": device_id,
                "dateTimeStart": date_time_start,
                "dateTimeEnd": date_time_end,
                "StreetName": street_name,
                "BetweenStreet1": between_street1,
                "BetweenStreet2": between_street2,
                "line_items": line_items
            }
            collection.insert_one(new_doc)

# Iterate over each chunk and process it
for chunk in chunks:
    process_chunk(chunk)

print("Data successfully formatted and uploaded to MongoDB.")