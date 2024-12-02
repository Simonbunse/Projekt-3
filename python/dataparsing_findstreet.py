import csv

# Set file path and target StreetId
file_path = r"C:\Users\simon\OneDrive\Desktop\On-street_Car_Parking_Sensor_Data_-_2019.csv"
target_street_id = "123"

# Initialize counters and a set to store unique DeviceIds with the target StreetId
device_ids_with_street_id = set()
total_lines = 0

# Open and read the CSV file
try:
    with open(file_path, mode="r", encoding="utf-8-sig") as file:  # Use utf-8-sig to handle BOM
        reader = csv.reader(file)
        headers = next(reader)  # Get the header row
        headers = [header.strip() for header in headers]  # Trim whitespace from headers

        # Create a dictionary to map headers to their indices
        header_index = {header: index for index, header in enumerate(headers)}

        for row in reader:
            # Update line counter
            total_lines += 1
            if total_lines % 100000 == 0:  # Print every 100000 lines parsed
                print(f"{total_lines} lines parsed...")

            # Check if the row's StreetId matches the target StreetId
            if row[header_index["StreetId"]] == target_street_id:
                device_ids_with_street_id.add(row[header_index["DeviceId"]])  # Use set to avoid duplicates

except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Count and print results
count = len(device_ids_with_street_id)
print(f"\nNumber of unique DeviceIds with StreetId {target_street_id}: {count}")
print("DeviceIds with the specified StreetId:")
for device_id in device_ids_with_street_id:
    print(device_id)
