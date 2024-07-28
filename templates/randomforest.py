import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from sklearn.preprocessing import StandardScaler


# Load the dataset
data = pd.read_csv('C:\Users\r4rak\Downloads\final\EvasivePDFmalware2022.csv')

# Check for missing values
print(data.isnull().sum())

# Dropping rows with missing values (if any)
data = data.dropna()

# Define features and target variable
X = data.drop('class', axis=1)  # Features
y = data['class']  # Target variable

# Convert target variable to numerical values (0 for benign, 1 for malicious)
y = np.where(y == 'malicious', 1, 0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the feature values
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# Initialize and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


# Save the model to a file
joblib.dump(model, 'malicious_pdf_model.joblib')

# Save the scaler for later use
joblib.dump(scaler, 'scaler.joblib')

def predict_pdf_maliciousness(pdf_features):
    # Load the saved model and scaler
    model = joblib.load('malicious_pdf_model.joblib')
    scaler = joblib.load('scaler.joblib')

    # Check if the number of features matches
    if len(pdf_features) != 20:  # Change this to 20
        raise ValueError(f"Expected 20 features, but got {len(pdf_features)}.")

    # Preprocess the input features (standardize)
    pdf_features_scaled = scaler.transform([pdf_features])

    # Make a prediction
    prediction = model.predict(pdf_features_scaled)

    return 'malicious' if prediction[0] == 1 else 'benign'

# Example user input features for a PDF (must have 20 features)
# Replace with actual feature values that match your dataset
user_input_pdf_features = [200, 5, 10, 2, 3, 5, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]  # Adjusted to have 20 features

# Make a prediction
result = predict_pdf_maliciousness(user_input_pdf_features)
print("The PDF is:", result)