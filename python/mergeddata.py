import pandas as pd

# File paths
training_file = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\filtered_training_data_10minuteinterval.csv"
test_file = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\filtered_test_data_10minuteinterval.csv"
output_file = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\machinelearning_data.csv"

# Month sorting order
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Load the training and test data
training_data = pd.read_csv(training_file)
test_data = pd.read_csv(test_file)

# Merge the two datasets
merged_data = pd.concat([training_data, test_data], ignore_index=True)

# Ensure the 'month' column uses the specified order
merged_data["month"] = pd.Categorical(merged_data["month"], categories=month_order, ordered=True)

# Sort by deviceId, month, dayOfMonth, and IntervalOfDay
merged_data.sort_values(by=["deviceId", "month", "dayOfMonth", "IntervalOfDay"], inplace=True)

# Save the sorted merged data to a new CSV file
merged_data.to_csv(output_file, index=False)

print(f"Merged file saved at: {output_file}")
