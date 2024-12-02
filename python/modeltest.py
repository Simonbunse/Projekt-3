import joblib
import pandas as pd
import numpy as np

# Load the saved model and encoder
print("Loading saved model and encoder...")
model = joblib.load('parking_availability_model.pkl')
encoder = joblib.load('onehot_encoder.pkl')

# Function to preprocess the user input data
def preprocess_user_input(street_name, between_streets, day_of_week, month, interval_of_day, day_of_month):
    print("Preprocessing user input data...")

    # Map dayOfWeek and month to numerical values
    day_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                   'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    month_mapping = {'January': 0, 'February': 1, 'March': 2, 'April': 3,
                     'May': 4, 'June': 5, 'July': 6, 'August': 7,
                     'September': 8, 'October': 9, 'November': 10, 'December': 11}

    # Ensure that the inputs are valid
    if day_of_week not in day_mapping:
        raise ValueError(f"Invalid dayOfWeek: {day_of_week}")
    if month not in month_mapping:
        raise ValueError(f"Invalid month: {month}")
    
    # Prepare the feature DataFrame
    user_input_data = pd.DataFrame({
        'streetName': [street_name],
        'betweenStreets': [between_streets],
        'dayOfWeek': [day_mapping[day_of_week]],
        'month': [month_mapping[month]],
        'IntervalOfDay': [interval_of_day],
        'dayOfMonth': [day_of_month]  # Added dayOfMonth as an input feature
    })

    print("User input data preprocessing complete.")
    print(user_input_data)
    return user_input_data

# Function to make the prediction with a confidence score
def predict_parking_availability(street_name, between_streets, day_of_week, month, interval_of_day, day_of_month):
    # Preprocess the user input
    user_data = preprocess_user_input(street_name, between_streets, day_of_week, month, interval_of_day, day_of_month)

    # OneHot encode the categorical features
    categorical_features = ['betweenStreets', 'streetName']
    encoded_data = encoder.transform(user_data[categorical_features])

    # Convert categorical features into a DataFrame
    encoded_columns = encoder.get_feature_names_out(categorical_features)
    encoded_df = pd.DataFrame(encoded_data, columns=encoded_columns)

    # Concatenate encoded categorical features with numerical features
    numerical_features = ['IntervalOfDay', 'dayOfWeek', 'month', 'dayOfMonth']  # Include dayOfMonth here
    user_data_numerical = user_data[numerical_features].reset_index(drop=True)
    final_input_data = pd.concat([encoded_df, user_data_numerical], axis=1)

    # Get the predicted probabilities for both classes
    prob = model.predict_proba(final_input_data)

    # The confidence score is the probability for the "parking available" class (True)
    confidence_score = prob[0][1]  # Index 1 corresponds to "True" (parking available)

    # Define a threshold for parking availability based on confidence
    if confidence_score >= 0.5:
        result = "Parking is likely available."
    else:
        result = "Parking is likely unavailable."

    # Return the result and confidence score as a percentage
    return f"{result} Confidence: {confidence_score * 100:.2f}%"

# Take user input
print("Please enter the following details:")

street_name = input("Street Name: ")
between_streets = input("Between Streets: ")
day_of_week = input("Day of Week (e.g., Monday, Tuesday, etc.): ")
month = input("Month (e.g., January, February, etc.): ")
interval_of_day = int(input("Interval of Day (e.g., 0 for midnight, 1 for 10 minutes past, etc.): "))
day_of_month = int(input("Day of the Month (1-31): "))  # Take dayOfMonth as input

# Get the prediction with the confidence score
result = predict_parking_availability(street_name, between_streets, day_of_week, month, interval_of_day, day_of_month)
print(result)
