import csv
from datetime import datetime

# Set file paths
input_file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\dataprojekt3\Car_Parking_Sensor_Data_Original.csv"
output_file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\dataprojekt3\Car_Parking_Sensor_Data_Sorted.csv"

# Function to parse the ArrivalTime string into a datetime object
def parse_arrival_time(arrival_time_str):
    return datetime.strptime(arrival_time_str, "%m/%d/%Y %I:%M:%S %p")

# Open the input file and create the output file
try:
    all_rows = []
    total_lines = 0
    
    with open(input_file_path, mode="r", encoding="utf-8-sig") as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Read the header row

        for row in reader:
            total_lines += 1
            if total_lines % 100000 == 0:  # Print every 100000 lines parsed
                print(f"{total_lines} lines parsed...")

            all_rows.append(row)  # Append all rows to the list

    # Sort the rows first by DeviceId and then by ArrivalTime
    all_rows.sort(key=lambda x: (x[headers.index("DeviceId")], parse_arrival_time(x[headers.index("ArrivalTime")])))

    # Write the sorted rows to the output file
    with open(output_file_path, mode="w", newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write the header to the new file
        writer.writerows(all_rows)  # Write the sorted rows

except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print(f"Sorted data has been written to {output_file_path}.")
