import csv
from datetime import datetime

# Set file paths
input_file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\dataprojekt3\Car_Parking_Sensor_Data_Original.csv"
output_file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\dataprojekt3\Car_Parking_Sensor_Data_123.csv"

# Unique DeviceIds with the target StreetId
device_ids_with_street_id = {
    "23704", "17264", "23161", "17737", "24846", "24191", "17784", "24560", "26342", 
    "17254", "27461", "17272", "26495", "23703", "17779", "24202", "18745", "18740", 
    "18798", "27173", "24531", "17290", "17298", "17313", "17299", "28059", "27312", 
    "17740", "18742", "18735", "25713", "17291", "17735", "17764", "26201", "18728", 
    "26492", "17739", "26878", "26200", "17274", "27462", "27406", "17756", "17275", 
    "17294", "17743", "17746", "17766", "17767", "17749", "18734", "23661", "26340", 
    "17755", "17304", "26204", "17734", "17733", "17300", "25710", "25921", "28196", 
    "17252", "17765", "17774", "18771", "17747", "24558", "17748", "26874", "24473", 
    "23156", "24837", "18737", "18733", "17768", "28489", "26876", "19267", "17259", 
    "18738", "17269", "26661", "26023", "17266", "28492", "23889", "26021", "23702", 
    "18708", "25711", "27246", "28491", "17246", "23088", "17763", "17760", "17288", 
    "18722", "17301", "17780", "17270", "25716", "23668", "17758", "17757", "17772", 
    "25188", "28197", "17303", "24838", "17292", "27408", "23604", "28192", "17280", 
    "27313", "26022", "24004", "27136", "17729", "24047", "17744", "17262", "17741", 
    "18797", "23374", "18712", "17776", "18731", "17258", "27607", "23578", "17775", 
    "18755", "24474", "25717", "17742", "27608", "24443", "26396", "18710", "18717", 
    "18795", "17736", "17771", "28193", "27321", "24762", "17769", "26493", "27135", 
    "17745", "17750", "26203", "24840", "17752", "18794", "17731", "17244", "17286", 
    "23373", "18756", "26879", "27315", "24703", "17759", "17307", "26663", "23887", 
    "28313", "23662", "27311", "17271", "17754", "26873", "18741", "26202", "17256", 
    "23428", "18732", "28194", "17751", "22289", "23916", "26336", "27407", "17242", 
    "23700", "24069", "23753", "27054", "17761", "17730", "27314", "25923", "24704", 
    "26494", "27319", "28094", "28195", "23376", "23564", "27506", "17738", "23701", 
    "27316", "17311", "23915", "17243", "23245", "17260", "18774", "23638", "28312", 
    "23551", "26875", "28490", "18796", "25712", "26662", "25922", "17773", "23777", 
    "27310", "26199", "27320", "26877", "17283", "17297", "17770", "24200", "18721", 
    "24559", "27172", "23124", "27317"
}

# Function to parse the ArrivalTime string into a datetime object
def parse_arrival_time(arrival_time_str):
    return datetime.strptime(arrival_time_str, "%m/%d/%Y %I:%M:%S %p")

# Open the input file and create the output file
try:
    filtered_rows = []
    total_lines = 0
    
    with open(input_file_path, mode="r", encoding="utf-8-sig") as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Read the header row

        for row in reader:
            total_lines += 1
            if total_lines % 100000 == 0:  # Print every 100000 lines parsed
                print(f"{total_lines} lines parsed...")

            device_id = row[headers.index("DeviceId")]
            if device_id in device_ids_with_street_id:
                filtered_rows.append(row)  # Append row if DeviceId is in the set

    # Sort the filtered rows first by DeviceId and then by ArrivalTime
    filtered_rows.sort(key=lambda x: (x[headers.index("DeviceId")], parse_arrival_time(x[headers.index("ArrivalTime")])))

    # Write the sorted rows to the output file
    with open(output_file_path, mode="w", newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write the header to the new file
        writer.writerows(filtered_rows)  # Write the sorted rows

except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print(f"Filtered and sorted data has been written to {output_file_path}.")
