# Prediction of time to respond to a sales opportunity
# Definition: Time to respond is the duration (in hours) between the initial contact with a sales opportunity and the first meaningful engagement (e.g., a follow-up call or meeting).
# Definition of Linear Regression: A statistical method that models the relationship between a dependent variable and one or more independent variables by fitting a linear equation to observed data. 
# It is used for predicting continuous outcomes.

# Update 9/18/2025
# Lasso (L1) gave the lowest Mean Squared Error and highest R², suggesting it’s capturing the signal more cleanly—possibly by zeroing out noisy or less relevant features.
# Ridge (L2) also improved over plain Linear Regression, but not as dramatically.
# L2
# Mean Squared Error: 12.73
# R² Score: 0.70

import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from schemas import OpportunityFeatures

# Set MLFlow tracking URI (defaults to local ./mlruns directory)
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("SalesOpportunityPrediction")  # Create or use an experiment

# Step 2: Load dataset from Excel
file_path = 'SalesOpportunityDataSet.xlsx'  # Adjust if needed
data = pd.read_excel(file_path, sheet_name='SalesOpportunityDataSet')
print("Data Loaded from Excel:")
print(data.head())

# Step 3: Encode categorical features
label_encoders = {}
for col in ['Industry', 'Company_Size', 'Contact_Title', 'Product_Interest', 'Region', 'Prior_Deals']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Step 4: Split features and target
X = data.drop(['Time_to_Respond', 'Opportunity_ID'], axis=1)
y = data['Time_to_Respond']

# Cast integer columns to float to avoid MLflow schema warning
for col in X.select_dtypes(include=['int', 'int32', 'int64']).columns:
    X[col] = X[col].astype(float)

# Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Function to train and log a model with MLFlow
def train_and_log_model(model, model_name, params=None):
    with mlflow.start_run(run_name=model_name):
        # Log parameters if any
        if params:
            mlflow.log_params(params)
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Log metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)
        
        # Log the model
        mlflow.sklearn.log_model(model, name="model", input_example=X_train.iloc[0:1])
        
        print(f"{model_name} Results:")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")
        
        return model

# Train and log models
linear_model = train_and_log_model(LinearRegression(), "LinearRegression")

ridge_params = {"alpha": 1.0}
ridge_model = train_and_log_model(Ridge(**ridge_params), "Ridge", ridge_params)

lasso_params = {"alpha": 0.1}
lasso_model = train_and_log_model(Lasso(**lasso_params), "Lasso", lasso_params)

elastic_params = {"alpha": 0.1, "l1_ratio": 0.5}
elastic_model = train_and_log_model(ElasticNet(**elastic_params), "ElasticNet", elastic_params)

# Step 8: Predict a new sample (using one model for demo; you can repeat for others)
raw_sample = {
    'Industry': 'Finance',
    'Company_Size': 'Medium',
    'Contact_Title': 'Risk Manager',
    'Engagement_Score': 70,
    'Product_Interest': 'Risk Analytics',
    'Region': 'West',
    'Prior_Deals': 'Yes',
    'Is_Good_Opportunity': 1
}

# Validate and parse with Pydantic
sample = OpportunityFeatures(**raw_sample)

new_sample = pd.DataFrame([{  # Use validated sample
    'Industry': label_encoders['Industry'].transform([sample.Industry])[0],
    'Company_Size': label_encoders['Company_Size'].transform([sample.Company_Size])[0],
    'Contact_Title': label_encoders['Contact_Title'].transform([sample.Contact_Title])[0],
    'Engagement_Score': float(sample.Engagement_Score),
    'Product_Interest': label_encoders['Product_Interest'].transform([sample.Product_Interest])[0],
    'Region': label_encoders['Region'].transform([sample.Region])[0],
    'Prior_Deals': label_encoders['Prior_Deals'].transform([sample.Prior_Deals])[0],
    'Is_Good_Opportunity': float(sample.Is_Good_Opportunity)
}])
predicted_time = max(0, linear_model.predict(new_sample)[0])
print(f"Predicted Time to Respond (Linear): {predicted_time:.2f} hours")

# Predict with others
ridge_time = max(0, ridge_model.predict(new_sample)[0])
print(f"Predicted Time to Respond (Ridge): {ridge_time:.2f} hours")

lasso_time = max(0, lasso_model.predict(new_sample)[0])
print(f"Predicted Time to Respond (Lasso): {lasso_time:.2f} hours")

elastic_time = max(0, elastic_model.predict(new_sample)[0])
print(f"Predicted Time to Respond (Elastic Net): {elastic_time:.2f} hours")