import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sklearn.preprocessing import OneHotEncoder

# File path
file_path = r"C:\Users\simon\OneDrive\IT-Teknolog\projekt3\machinelearning_data.csv"

# Percentile threshold (change as needed, here it's set to 40%)
availability_percentile = 45

# Read data in chunks and combine them into a single DataFrame
chunksize = 100000  # Adjust the chunk size as needed
data_chunks = []

print("Starting to read data in chunks...")
for chunk in pd.read_csv(file_path, engine='python', chunksize=chunksize):
    data_chunks.append(chunk)

print("Concatenating data chunks...")
data = pd.concat(data_chunks, axis=0)
print(f"Full data shape: {data.shape}")

# Define the function to preprocess the data
def preprocess_data(df):
    print("Preprocessing data...")

    # Ensure categorical features are strings
    categorical_features = ['streetName', 'betweenStreets']
    print("Ensuring categorical features are strings...")
    df[categorical_features] = df[categorical_features].astype(str)

    # Convert the target variable to boolean
    print("Converting target variable to boolean...")
    df['vehiclePresent'] = df['vehiclePresent'].astype(bool)

    # Map days of the week and months to numerical values
    print("Mapping dayOfWeek and month to numerical values...")
    day_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                   'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    month_mapping = {'January': 0, 'February': 1, 'March': 2, 'April': 3,
                     'May': 4, 'June': 5, 'July': 6, 'August': 7,
                     'September': 8, 'October': 9, 'November': 10, 'December': 11}

    df['dayOfWeek'] = df['dayOfWeek'].map(day_mapping)
    df['month'] = df['month'].map(month_mapping)

    # Ensure dayOfMonth is a numerical feature
    df['dayOfMonth'] = pd.to_numeric(df['dayOfMonth'], errors='coerce')

    print("Preprocessing complete.")
    return df

# Preprocess the full data
print("Preprocessing full data...")
data = preprocess_data(data)
print(f"Processed data shape: {data.shape}")

# Aggregating data by betweenStreets, streetName, and time features
print("Aggregating data by betweenStreets, streetName, and time features...")
aggregated_data = data.groupby(['betweenStreets', 'streetName', 'dayOfWeek', 'month', 'dayOfMonth', 'IntervalOfDay'], as_index=False).agg(
    vehiclePresentPercent=('vehiclePresent', lambda x: (x == False).mean())
)

# Determine parking availability based on percentile
aggregated_data['parkingAvailable'] = aggregated_data['vehiclePresentPercent'] >= np.percentile(aggregated_data['vehiclePresentPercent'], availability_percentile)

# Display the first few rows of the aggregated data
print(aggregated_data.head())

# Split into features and target variable
X = aggregated_data.drop('parkingAvailable', axis=1)
y = aggregated_data['parkingAvailable']

# Randomly split data into training and testing sets (80% train, 20% test)
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Training data shape: {X_train.shape}, Test data shape: {X_test.shape}")

# Initialize OneHotEncoder
print("Initializing OneHotEncoder...")
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Categorical features
categorical_features = ['betweenStreets', 'streetName']

print("Fitting encoder on training data...")
X_train_cat = encoder.fit_transform(X_train[categorical_features])
X_test_cat = encoder.transform(X_test[categorical_features])

print("Getting categorical feature names...")
categorical_feature_names = encoder.get_feature_names_out(categorical_features)

print("Converting encoded features to DataFrame...")
X_train_cat = pd.DataFrame(X_train_cat, columns=categorical_feature_names)
X_test_cat = pd.DataFrame(X_test_cat, columns=categorical_feature_names)

# Numerical features
numerical_features = ['IntervalOfDay', 'dayOfWeek', 'month', 'dayOfMonth']  # Include dayOfMonth here
X_train_num = X_train[numerical_features].reset_index(drop=True)
X_test_num = X_test[numerical_features].reset_index(drop=True)

# Combine categorical and numerical features
print("Combining categorical and numerical features...")
X_train = pd.concat([X_train_cat, X_train_num], axis=1)
X_test = pd.concat([X_test_cat, X_test_num], axis=1)

print("Defining target variable...")
y_train = y_train
y_test = y_test

# Split training data for validation
print("Splitting training data for validation...")
X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
print(f"Split training data shape: {X_train_split.shape}, {X_val_split.shape}")

# Initialize Logistic Regression model
print("Initializing Logistic Regression model...")
model = LogisticRegression(max_iter=10000, verbose=1)

# Fitting Logistic Regression model
print("Fitting Logistic Regression model...")
model.fit(X_train_split, y_train_split)

# Evaluating model performance on validation set
print("Evaluating model performance on validation set...")
y_pred = model.predict(X_val_split)
val_accuracy = accuracy_score(y_val_split, y_pred)
print(f'Validation Accuracy: {val_accuracy:.4f}')

# Testing model on test set
print("Testing model on test set...")
y_test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
print(f'Test Accuracy: {test_accuracy:.4f}')

# Model coefficients and intercept
print("Model coefficients and intercept:")
print(f"Model Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")

# Saving model and encoder
print("Saving model and encoder...")
joblib.dump(model, 'parking_availability_model.pkl')
joblib.dump(encoder, 'onehot_encoder.pkl')

print("Process complete.")
