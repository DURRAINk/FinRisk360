# FinRisk360 (Under Developement)

## Explainable Fraud Detection for Indian Digital Payments with Azure Machine Learning

FinRisk360 is an end-to-end machine learning system for detecting potentially fraudulent digital-payment transactions across the Indian financial ecosystem.

The project uses transaction behavior, authentication signals, device information, merchant context, customer history, and location-related features to estimate fraud probability and support analyst review.

The system is designed to demonstrate the complete machine learning lifecycle:

- Data validation and feature engineering.
- Fraud detection under class imbalance.
- Leakage-aware model evaluation.
- Explainable predictions using SHAP.
- Experiment tracking with MLflow.
- Model registration and deployment through Azure Machine Learning.
- Real-time inference through a managed online endpoint.
- Streamlit dashboard for analyst-style review.
- Automated testing with GitHub Actions.

> This is a research and portfolio project based on a limited dataset. It is not a production banking system and must not be used for real financial decisions without extensive validation, governance, security review, and regulatory approval.

---

## Project Demo

### Dashboard

![FinRisk360 Dashboard](assets/dashboard-preview.png)

### Prediction Example

```json
{
  "fraud_probability": 0.84,
  "risk_band": "High",
  "recommended_action": "Investigate",
  "model_version": "1"
}
```

### Architecture

![FinRisk360 Architecture](assets/architecture.png)

---

## Business Problem

Digital-payment fraud can occur across multiple channels, including:

- UPI.
- Internet banking.
- IMPS.
- NEFT.
- RTGS.
- Debit cards.
- Credit cards.
- Mobile wallets.

A fraud-detection system should not only classify transactions as legitimate or fraudulent. It should also:

1. Identify suspicious behavior.
2. Minimize missed fraudulent transactions.
3. Control false positives.
4. Explain why a transaction was flagged.
5. Support real-time scoring.
6. Monitor the model after deployment.

FinRisk360 produces a fraud probability, risk category, recommended action, and explanation for each transaction.

---

## Key Features

### Fraud classification

The system predicts whether a transaction is:

- `Legitimate`
- `Fraudulent`

### Risk-based decision support

Transactions are assigned to operational risk bands:

| Risk band | Suggested action |
|---|---|
| Low | Approve |
| Medium | Send for analyst review |
| High | Investigate or hold |

The thresholds are selected using validation results and business-cost assumptions rather than an arbitrary probability of 0.5.

### Explainable predictions

Each prediction can include reason codes such as:

- Transaction amount is unusually high compared with the customer's historical average.
- Transaction originated from a new device.
- Transaction location does not match the customer's usual location.
- Multiple failed login attempts were detected.
- Merchant or IP risk score is elevated.

### Azure ML lifecycle

The project uses Azure Machine Learning for:

- Data-asset management.
- Reproducible training jobs.
- MLflow experiment tracking.
- Model registration.
- Managed online endpoint deployment.
- Model and endpoint lifecycle management.

### Testing and automation

The repository includes:

- Unit tests.
- Input-validation tests.
- Model-output tests.
- GitHub Actions CI.
- Reproducible configuration.

---

## Dataset

The dataset contains 15,000 financial transaction records representing digital banking and electronic payment activities in an Indian financial context.

It includes information about:

- Customers.
- Banks.
- Merchants.
- Transactions.
- Payment methods.
- Authentication.
- Devices.
- Locations.
- Customer behavior.
- Risk indicators.

### Target column

```text
fraud_label
```

Possible values:

```text
Legitimate
Fraudulent
```

### Main feature groups

| Feature group | Example columns |
|---|---|
| Transaction | `transaction_amount`, `transaction_type`, `transaction_hour` |
| Payment | `payment_method`, `upi_app`, `currency` |
| Customer | `customer_age`, `occupation`, `annual_income` |
| Account | `account_type`, `account_balance` |
| Merchant | `merchant_category`, `merchant_risk_score` |
| Authentication | `authentication_method`, `authentication_status` |
| Device | `device_type`, `device_brand`, `device_trust_score` |
| Security | `login_attempts`, `failed_login_count`, `ip_risk_score` |
| Location | `state`, `city`, `location_match`, `transaction_distance_km` |
| Behavior | `previous_transactions`, `average_transaction_amount` |

### Dataset limitations

The dataset may be synthetic or simulated. Therefore:

- Results should not be interpreted as real banking performance.
- The fraud distribution may not match production data.
- Some risk-score features may already encode information related to fraud.
- A reliable transaction timestamp may not be available.
- Generalization to real financial institutions has not been established.

---

## Leakage Audit

Financial fraud datasets can contain features that make a model appear stronger than it would be in production.

The following features were specifically reviewed:

- `merchant_risk_score`
- `device_trust_score`
- `ip_risk_score`
- `authentication_status`
- `new_device`
- `location_match`
- `high_value_transaction`
- `failed_login_count`
- `beneficiary_age_days`

The project compares multiple feature configurations:

| Experiment | Description |
|---|---|
| Full model | Uses all approved features |
| Risk-score ablation | Removes merchant, device, and IP risk scores |
| Authentication ablation | Removes authentication-related fields |
| Context-only model | Uses transaction, customer, merchant, and behavioral context |

This analysis helps determine whether performance depends heavily on precomputed risk indicators or potentially leaky features.

---

## Feature Engineering

The project creates behavior-based and transaction-context features such as:

```text
amount_to_average_ratio
amount_to_income_ratio
balance_after_transaction
login_failure_ratio
risk_score_average
unusual_hour_flag
device_location_mismatch
beneficiary_newness_flag
```

Example:

\[
\text{amount\_to\_average\_ratio}
=
\frac{\text{transaction\_amount}}
{\text{average\_transaction\_amount}+\epsilon}
\]

All engineered features are reviewed for:

- Availability at prediction time.
- Target leakage.
- Missing values.
- Extreme values.
- Business interpretability.

---

## Machine Learning Approach

### Baseline model

The project begins with Logistic Regression because it is:

- Interpretable.
- Fast to train.
- Useful as a reference point.
- Suitable for probability-based decisions.

### Tree-based model

A tree-based model such as XGBoost or Random Forest is used to capture nonlinear relationships between:

- Transaction amount.
- Customer behavior.
- Device signals.
- Authentication activity.
- Merchant risk.
- Location mismatch.

### Evaluation metrics

Because fraud detection is usually imbalanced, accuracy is not the primary metric.

The project evaluates:

- PR-AUC.
- ROC-AUC.
- Fraud precision.
- Fraud recall.
- F1-score.
- Confusion matrix.
- False-positive rate.
- Expected business cost.
- Probability calibration.

### Results

Replace the following values with results from your experiments.

| Model | PR-AUC | ROC-AUC | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` |
| Random Forest | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` |
| XGBoost | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` |

> Do not publish placeholder values. Replace every metric before making the repository public.

---

## Explainability

SHAP is used to inspect global and transaction-level model behavior.

Example:

```text
Fraud probability: 0.84
Risk band: High
Recommended action: Investigate

Main contributing factors:
- Transaction amount is significantly higher than usual.
- Transaction originated from a new device.
- Location differs from the customer's normal location.
- Multiple failed login attempts were recorded.
```

SHAP explanations describe factors that influenced the model's prediction. They should not be interpreted as proof that a feature caused fraud.

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │  Raw Transaction Data│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Validation      │
                    │ and Feature Creation │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure ML Data Asset  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure ML Training Job│
                    │ + MLflow Tracking    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Registered Model     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Managed Online       │
                    │ Endpoint             │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐         ┌──────────────────┐
       │ Streamlit        │         │ REST/API Client   │
       │ Analyst Dashboard│         │                  │
       └──────────────────┘         └──────────────────┘
```

---

## Azure ML Workflow

```text
1. Register the dataset as an Azure ML data asset.
2. Submit a reproducible Azure ML training job.
3. Track parameters, metrics, and artifacts with MLflow.
4. Evaluate the trained model.
5. Register the approved model.
6. Deploy the model to a managed online endpoint.
7. Send real-time scoring requests.
8. Monitor endpoint and model behavior.
```

### Azure ML components

| Component | Purpose |
|---|---|
| Azure ML Workspace | Central project workspace |
| Data Asset | Versioned dataset reference |
| Compute | Training and inference resources |
| Command Job | Reproducible training execution |
| MLflow | Experiment and metric tracking |
| Model Registry | Model version management |
| Managed Online Endpoint | Real-time prediction service |
| Application Insights / Azure Monitor | Operational monitoring |

---

## Example API Request

```bash
curl -X POST "<AZURE_ML_ENDPOINT_URL>/score" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "transaction_amount": 25000,
    "payment_method": "UPI",
    "transaction_hour": 2,
    "login_attempts": 4,
    "failed_login_count": 3,
    "previous_transactions": 18,
    "average_transaction_amount": 3500,
    "new_device": true,
    "location_match": false
  }'
```

### Example API Response

```json
{
  "fraud_probability": 0.84,
  "risk_band": "High",
  "recommended_action": "Investigate",
  "reason_codes": [
    "Unusually high transaction amount",
    "New device detected",
    "Location mismatch",
    "Multiple failed login attempts"
  ],
  "model_version": "1"
}
```

Do not commit real endpoint URLs, tokens, keys, or connection strings to GitHub.

---

## Repository Structure

```text
finrisk360/
├── data/
│   └── README.md
├── notebooks/
│   ├── 01_data_audit.ipynb
│   └── 02_model_analysis.ipynb
├── src/
│   ├── preprocess.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── evaluate.py
│   └── explain.py
├── api/
│   └── score.py
├── dashboard/
│   └── app.py
├── azureml/
│   ├── train_job.yml
│   ├── endpoint.yml
│   └── deployment.yml
├── tests/
│   ├── test_preprocess.py
│   ├── test_features.py
│   ├── test_model.py
│   └── test_api.py
├── assets/
│   ├── architecture.png
│   ├── dashboard-preview.png
│   └── shap-summary.png
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/finrisk360.git
cd finrisk360
```

### Create a virtual environment

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

### Run the dashboard locally

```bash
streamlit run dashboard/app.py
```

---

## Azure ML Setup

Install the Azure ML CLI extension:

```bash
az extension add -n ml
```

Log in to Azure:

```bash
az login
```

Set the subscription:

```bash
az account set --subscription "<SUBSCRIPTION_ID>"
```

Submit the training job:

```bash
az ml job create \
  --file azureml/train_job.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>"
```

Deploy the endpoint:

```bash
az ml online-endpoint create \
  --file azureml/endpoint.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>"
```

```bash
az ml online-deployment create \
  --file azureml/deployment.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>" \
  --endpoint-name "<ENDPOINT_NAME>"
```

Replace placeholder values with your own Azure resources. Never commit credentials or secrets.

---

## Testing

The test suite validates:

- Data preprocessing.
- Feature creation.
- Missing-value handling.
- Prediction probability range.
- Risk-band assignment.
- API input validation.
- Model artifact loading.
- Error handling.

Run:

```bash
pytest -v
```

The GitHub Actions workflow runs automated checks on pushes and pull requests.

---

## Responsible AI and Limitations

This project is intended for research and portfolio demonstration only.

Important limitations:

- The dataset contains only 15,000 records.
- The dataset may be synthetic or simulated.
- The fraud distribution may not represent real banking data.
- Some risk-score features may contain proxy information.
- The available fields may not include a reliable transaction timestamp.
- The model has not been validated on live financial transactions.
- No automated financial decision should be made solely from this model.
- Real deployment would require security, privacy, fairness, auditability, human oversight, and regulatory review.

Before production use, the system would require:

- Independent validation.
- Temporal out-of-sample testing.
- Bias and fairness assessment.
- Data-drift monitoring.
- Security testing.
- Access control.
- Privacy review.
- Human-in-the-loop procedures.
- Incident-response processes.
- Formal model governance.

---

## Future Improvements

Potential next steps include:

- Add reliable transaction timestamps.
- Evaluate temporal and rolling-window features.
- Add transaction velocity features.
- Test graph-based customer–merchant relationships.
- Add model calibration monitoring.
- Add data-drift detection.
- Add analyst feedback loops.
- Add challenger models.
- Add controlled model rollbacks.
- Add Azure Monitor and Application Insights dashboards.
- Add secure deployment through managed identity.
- Add a grounded fraud-investigation policy assistant.
- Evaluate the system on a larger and independently sourced dataset.

---

## Learning Outcomes

This project demonstrates practical experience with:

- Python.
- SQL.
- Data cleaning.
- Feature engineering.
- Imbalanced classification.
- Leakage prevention.
- Cost-sensitive evaluation.
- Explainable AI.
- SHAP.
- MLflow.
- Azure Machine Learning.
- Model registration.
- Managed online endpoints.
- REST APIs.
- Streamlit.
- Testing.
- GitHub Actions.
- MLOps fundamentals.
- Technical documentation.

---

## Author

**Durrain Khan**

- LinkedIn: [<YOUR_LINKEDIN_PROFILE>](https://www.linkedin.com/in/durrain-khan-pathan-728762304/)
- Email: `durrainpathan123@gmail.com`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
