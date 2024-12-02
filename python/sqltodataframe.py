from pymongo import MongoClient
import pandas as pd
import os

# MongoDB connection
client = MongoClient("mongodb+srv://simonhastrupjensen:TvrLm9gVK7ahWEPt@cluster0.e3e1e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.Cluster0
collection = db.ParkDataAus

# Directory to save DataFrames
output_dir = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\Parquet"
os.makedirs(output_dir, exist_ok=True)

# Counter for parsed documents
document_count = 0

def process_and_save_document(document):
    global document_count

    # Extract `line_items` and other fields
    line_items_df = pd.DataFrame(document['line_items'])
    line_items_df['DeviceId'] = document['DeviceId']
    line_items_df['dateTimeStart'] = document['dateTimeStart']
    line_items_df['dateTimeEnd'] = document['dateTimeEnd']
    
    # Create a subdirectory for each device
    device_dir = os.path.join(output_dir, f"Device_{document['DeviceId']}")
    os.makedirs(device_dir, exist_ok=True)
    
    # Save the DataFrame to a Parquet file, named by date
    date_str = pd.to_datetime(document['dateTimeStart']).strftime('%Y-%m-%d')
    file_path = os.path.join(device_dir, f"{date_str}.parquet")
    line_items_df.to_parquet(file_path, index=False)
    
    # Increment document count and print status
    document_count += 1
    print(f"Document {document_count}: Saved DataFrame for Device {document['DeviceId']} on {date_str} to {file_path}")

# Fetch all documents from the collection and process each one
for document in collection.find({}):
    process_and_save_document(document)

print(f"All documents have been processed and saved. Total documents processed: {document_count}")
