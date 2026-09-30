import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("endpoint_api_key")

# Azure ML endpoint details
scoring_uri = 'https://fraud-detection-22654607.centralindia.inference.ml.azure.com/score' # replace with your endpoint key

st.title("FinRisk360 - Transaction Fraud Detection")

# Account details
account_type = st.selectbox("Account Type", ['Current', 'Savings', 'NRI', 'Salary', 'Fixed Deposit'])
transaction_type = st.radio("Transaction Type", ['ATM_Withdrawal', 'UPI', 'POS', 'RTGS', 'IMPS', 'NEFT',
                                                'Net_Banking', 'Credit_Card', 'Auto_Debit', 'Cheque'])
transaction_direction = st.radio("Transaction Direction", ["Debit", "Credit"])

# Transaction amounts
transaction_amount = st.number_input("Transaction Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
emi_amount = st.number_input("EMI Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
amount_to_average_ratio = st.slider("Amount-to-Average Ratio", min_value=0.0, max_value=50.0, step=0.1)

# Merchant and channel
merchant_category = st.selectbox("Merchant Category", ['Food & Dining', 'Salary', 'Retail', 'Entertainment',
                                                    'Real Estate', 'Government', 'Travel', 'Peer Transfer',
                                                    'Investment', 'Insurance', 'Utilities', 'Fuel', 'Healthcare',
                                                    'E-Commerce', 'Education'])
channel = st.selectbox("Channel", ['Mobile_App', 'Web', 'ATM', 'API', 'POS_Terminal', 'Branch'])

# Location and state
state = st.selectbox("State", ['Rajasthan', 'Maharashtra', 'Tamil Nadu', 'Gujarat', 'Karnataka',
                                'Punjab', 'West Bengal', 'Delhi', 'Telangana', 'UP'])

# Credit & loan info
credit_score = st.slider("Credit Score", min_value=300, max_value=900, step=10)
loan_type = st.selectbox("Loan Type", ['None', 'Unknown', 'Gold', 'Personal', 'Home', 'Education', 'Auto', 'Business'])
kyc_status = st.radio("KYC Status", ['Verified', 'Pending', 'Expired'])

# Time features
transaction_hour = st.slider("Transaction Hour", min_value=0, max_value=23)
transaction_minute = st.slider("Transaction Minute", min_value=0, max_value=59)

# History
prior_transaction_count = st.number_input("Prior Transaction Count", min_value=0, step=1)

if st.button("Predict"):
    # Build payload
    
    data = {
  "input_data": {
    "columns": [
      "account_type",
      "transaction_type",
      "transaction_amount",
      "transaction_direction",
      "merchant_category",
      "state",
      "credit_score",
      "loan_type",
      "emi_amount",
      "channel",
      "kyc_status",
      "transaction_hour",
      "transaction_minute",
      "prior_transaction_count",
      "amount_to_average_ratio"
    ],
    "data": [
      [
        account_type,
        transaction_type,
        transaction_amount,
        transaction_direction,
        merchant_category,
        state,
        credit_score,
        loan_type,
        emi_amount,
        channel,
        kyc_status,
        transaction_hour,
        transaction_minute,
        prior_transaction_count,
        amount_to_average_ratio
      ]
    ]
  },
  "params": {"method": "predict_proba"}
}

    # Send request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(scoring_uri, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        result = response.json()[0]
        if result:
            st.success(f"Prediction: The transaction is Fraudulent.")
        else:
            st.success(f"Prediction: The transaction is Legitimate.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")
