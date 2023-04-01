import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

# Load the dataset
df = pd.read_csv('data.csv', header=None)

# Set the column names
column_names = ['TA_eval', 'Helpfulness', 'Clarity', 'Difficulty', 'Interest', 'Score']
df.columns = column_names

# Perform exploratory data analysis
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Preprocess the data
X = df.drop('Score', axis=1)
y = df['Score']

# Convert the categorical variable to numerical
X['TA_eval'] = X['TA_eval'].replace({1: 'low', 2: 'medium', 3: 'high'})
X = pd.get_dummies(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a logistic regression model
model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
model.fit(X_train, y_train)

# Save the model to the local drive
filename = 'TA_performance_model.sav'
pickle.dump(model, open(filename, 'wb'))

# Evaluate the model on the testing set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1-score:', f1)
