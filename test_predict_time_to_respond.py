import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Basic test: Data loading and structure

def test_data_load():
    df = pd.read_excel('SalesOpportunityDataSet.xlsx', sheet_name='SalesOpportunityDataSet')
    # Check columns
    expected_cols = [
        'Opportunity_ID', 'Industry', 'Company_Size', 'Contact_Title',
        'Engagement_Score', 'Product_Interest', 'Region', 'Prior_Deals',
        'Time_to_Respond', 'Is_Good_Opportunity'
    ]
    for col in expected_cols:
        assert col in df.columns
    # Check no missing values in target
    assert df['Time_to_Respond'].isnull().sum() == 0

# Basic test: Model can fit and predict

def test_model_fit_predict():
    df = pd.read_excel('SalesOpportunityDataSet.xlsx', sheet_name='SalesOpportunityDataSet')
    X = df.drop(['Time_to_Respond', 'Opportunity_ID'], axis=1)
    y = df['Time_to_Respond']
    # Encode categoricals simply for test
    for col in X.select_dtypes(include=['object']).columns:
        X[col] = X[col].astype('category').cat.codes
    # Cast ints to float
    for col in X.select_dtypes(include=['int', 'int32', 'int64']).columns:
        X[col] = X[col].astype(float)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    # Check predictions are finite and non-negative
    assert all(pd.notnull(preds))
    assert (preds >= 0).all()
    # Check MSE is a finite number
    mse = mean_squared_error(y_test, preds)
    assert mse >= 0
