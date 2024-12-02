from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb+srv://simonhastrupjensen:TvrLm9gVK7ahWEPt@cluster0.e3e1e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.Cluster0
collection = db.ParkDataAusTest


# Filter for the last 2 months (November and December), excluding all other months
filtered_data = list(collection.find({
    "$expr": {
        "$in": [
            {"$month": {"$dateFromString": {"dateString": "$dateTimeStart"}}},
            [11, 12]  # November (11) and December (12)
        ]
    }
}))

# Convert to DataFrame
df = pd.DataFrame(filtered_data)

# Save the filtered data locally as a CSV file
file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\filtered_test_data.csv"
df.to_csv(file_path, index=False)
print(f"Data saved locally to {file_path}")
