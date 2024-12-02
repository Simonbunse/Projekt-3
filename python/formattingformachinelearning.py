import csv
from datetime import datetime, timedelta

# File paths
input_file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\filtered_training_data.csv"
output_file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\filtered_training_data_10minuteinterval.csv"

# Function to split intervals into perfect 10-minute segments
def generate_10_minute_intervals(start_date, end_date):
    current = start_date.replace(minute=0, second=0, microsecond=0)
    while current < end_date:
        yield current, current + timedelta(minutes=10)
        current += timedelta(minutes=10)

# Function to calculate occupancy for an interval
def calculate_occupancy(interval_start, interval_end, original_intervals):
    occupied_time = 0
    total_interval_time = (interval_end - interval_start).total_seconds()
    
    for item in original_intervals:
        # Ensure both arrival_time and departure_time are naive
        arrival_time = max(interval_start, datetime.fromisoformat(item["ArrivalTime"]).replace(tzinfo=None))
        departure_time = min(interval_end, datetime.fromisoformat(item["DepartureTime"]).replace(tzinfo=None))
        
        if arrival_time < departure_time:  # Overlapping interval
            if item["VehiclePresent"]:
                occupied_time += (departure_time - arrival_time).total_seconds()
    
    # Decide if the spot is occupied for the majority of the time
    return occupied_time > total_interval_time / 2

# Open the input file and process each line
line_counter = 0  # Initialize the counter
with open(input_file_path, "r") as infile, open(output_file_path, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ["deviceId", "month", "dayOfMonth", "IntervalOfDay", "dayOfWeek", "streetName", "betweenStreets", "vehiclePresent"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        line_counter += 1  # Increment the counter for each line processed
        
        device_id = row["DeviceId"]
        street_name = row["StreetName"].replace(" ", "").upper()
        between_streets = f"{row['BetweenStreet1']} - {row['BetweenStreet2']}"
        line_items = eval(row["line_items"])  # Parse line_items as a list of dictionaries
        
        # Extract start and end times for the day
        day_start = datetime.fromisoformat(row["dateTimeStart"]).replace(tzinfo=None)
        day_end = datetime.fromisoformat(row["dateTimeEnd"]).replace(tzinfo=None)
        
        # Generate 10-minute intervals for the day
        for interval_start, interval_end in generate_10_minute_intervals(day_start, day_end):
            vehicle_present = calculate_occupancy(interval_start, interval_end, line_items)
            
            # Calculate features
            day_of_week = interval_start.strftime("%A")
            month = interval_start.strftime("%B")
            day_of_month = interval_start.day
            hour_of_day = interval_start.hour
            minute_of_hour = interval_start.minute
            
            # Calculate the interval number (from the start of the day)
            interval_of_day = hour_of_day * 6 + minute_of_hour // 10  # 6 intervals per hour, each 10 minutes
            
            # Write the interval row
            writer.writerow({
                "deviceId": device_id,
                "month": month,
                "dayOfMonth": day_of_month,
                "IntervalOfDay": interval_of_day,
                "dayOfWeek": day_of_week,
                "streetName": street_name,
                "betweenStreets": between_streets,
                "vehiclePresent": vehicle_present
            })
        
        # Print progress every 100 lines processed
        if line_counter % 100 == 0:
            print(f"Processed {line_counter} lines...")

# Final print statement when done
print(f"Reformatted data with perfect 10-minute intervals saved to {output_file_path}.")
