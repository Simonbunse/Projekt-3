import csv
import requests
from collections import defaultdict
from datetime import datetime

# File path to the CSV
file_path = r'C:\Users\simon\OneDrive\IT-Teknolog\projekt3\data\Car_Parking_Sensor_Data_123.csv'

# URL for your API endpoint
api_url = "http://localhost:3000/api/streetsdata"

# Dictionary to group devices by between street combinations
streets_data = defaultdict(lambda: {"devices": set()})

# Temporary storage to track the latest vehiclePresent status per DeviceId
latest_vehicle_status = {}

# Read the CSV file and build data structure
with open(file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        street_name = row['StreetName'].strip()
        between_street1 = row['BetweenStreet1'].strip()
        between_street2 = row['BetweenStreet2'].strip()
        device_id = int(row['DeviceId'].strip())
        arrival_time = datetime.strptime(row['ArrivalTime'], "%m/%d/%Y %I:%M:%S %p")
        vehicle_present = row['VehiclePresent'].strip().lower() == 'true'

        # Create a unique key for each combination of streets
        between_streets_combined = f"{between_street1} - {between_street2}"
        
        # Populate the data, ensuring unique deviceIds
        if 'streetName' not in streets_data[between_streets_combined]:
            streets_data[between_streets_combined]['streetName'] = street_name
            streets_data[between_streets_combined]['betweenStreets'] = between_streets_combined  # corrected field name
        streets_data[between_streets_combined]['devices'].add(device_id)  # Use a set to ensure uniqueness

        # Update the latest_vehicle_status for the device
        if device_id not in latest_vehicle_status or arrival_time > latest_vehicle_status[device_id]['arrival_time']:
            latest_vehicle_status[device_id] = {
                "arrival_time": arrival_time,
                "vehicle_present": vehicle_present,
            }

# Convert sets to list of dictionaries and include vehiclePresent status
for key, data in streets_data.items():
    # Convert the set of deviceIds to a list of dictionaries
    data['devices'] = [
        {
            "deviceId": device_id,
            "vehiclePresent": latest_vehicle_status[device_id]['vehicle_present']
        }
        for device_id in data['devices']
    ]

    # Add the lastUpdated field to the data
    data['lastUpdated'] = datetime.now().isoformat()  # Current timestamp as the last updated time

    # Debugging: Print the data before sending it
    print(f"Sending data for {data['betweenStreets']}:\n", data)

    # Send data to the API
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        print(f"Successfully sent data for {data['betweenStreets']}")
    else:
        print(f"Failed to send data for {data['betweenStreets']}. Status Code: {response.status_code}, Response: {response.text}")
