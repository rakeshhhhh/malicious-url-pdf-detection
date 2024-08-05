import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer
import pickle

# Load the dataset
df = pd.read_csv('EvasivePDFmalware2022.csv')

# Check for any missing values
print(df.isnull().sum())

# Define features and target
X = df.drop(columns=['class'])
y = df['class']

# Handle missing values by filling with the mean of the column
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the imputer and scaler for later use
with open('imputer.pkl', 'wb') as f:
    pickle.dump(imputer, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)




# Create and train the KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# Evaluate the model
accuracy = knn.score(X_test_scaled, y_test)
print(f'Accuracy: {accuracy:.2f}')

# Save the trained model
with open('knn_model.pkl', 'wb') as f:
    pickle.dump(knn, f)





import numpy as np

def preprocess_pdf(pdf_features):
    # Load the imputer and scaler
    with open('imputer.pkl', 'rb') as f:
        imputer = pickle.load(f)
        
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    # Convert the PDF features into a DataFrame
    pdf_df = pd.DataFrame([pdf_features], columns=X.columns)
    
    # Handle missing values by filling with the mean of the column
    pdf_df = imputer.transform(pdf_df)
    
    # Standardize the features
    pdf_scaled = scaler.transform(pdf_df)
    
    return pdf_scaled




def predict_pdf(pdf_features):
    # Preprocess the PDF features
    pdf_scaled = preprocess_pdf(pdf_features)
    
    # Load the trained KNN model
    with open('knn_model.pkl', 'rb') as f:
        knn = pickle.load(f)
    
    # Make a prediction
    prediction = knn.predict(pdf_scaled)
    
    # Return the result
    return 'Malicious' if prediction[0] == 1 else 'Benign'

# Example usage
pdf_features = {
    'pdfsize': 12345,
    'pages': 10,
    'title characters': 50,
    'images': 2,
    'obj': 100,
    'endobj': 100,
    'stream': 10,
    'endstream': 10,
    'xref': 1,
    'trailer': 1,
    'startxref': 1,
    'ObjStm': 0,
    'JS': 0,
    'OBS_JS': 0,
    'Javascript': 0,
    'OBS_Javascript': 0,
    'OpenAction': 0,
    'OBS_OpenAction': 0,
    'Acroform': 0,
    'OBS_Acroform': 0
}

result = predict_pdf(pdf_features)
print(result)
