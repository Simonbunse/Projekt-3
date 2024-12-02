import csv

# Set to store unique combinations
unique_combinations = set()

# Open and read the CSV file
file_path = r'C:\Users\simon\OneDrive\IT-Teknolog\projekt3\data\Car_Parking_Sensor_Data_123.csv'
with open(file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV
    for row in csv_reader:
        between_street1 = row['BetweenStreet1'].strip()
        between_street2 = row['BetweenStreet2'].strip()
        
        # Create a tuple of the combination (in a sorted manner to avoid duplicates in reverse order)
        combination = tuple(sorted([between_street1, between_street2]))
        
        # Add to set to ensure uniqueness
        unique_combinations.add(combination)

# Print each unique combination
for combo in unique_combinations:
    print(f"{combo[0]} - {combo[1]}")
