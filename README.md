# FinRisk360

## Big-Data Fraud Detection with Azure Databricks and Azure Machine Learning

FinRisk360 is an end-to-end fraud-detection project for digital-payment transactions in the Indian financial ecosystem.

The project uses Azure Databricks for large-scale data analysis and feature engineering, then uses Azure Machine Learning Automated ML to train, compare, register, and deploy fraud-detection models.

The workflow demonstrates how a data scientist can move from raw transaction data to a deployed machine-learning service:

```text
Raw transaction data
        ↓
Azure Databricks
        ↓
Data analysis and feature engineering
        ↓
Versioned feature dataset
        ↓
Azure Machine Learning AutoML
        ↓
Model evaluation and MLflow tracking
        ↓
Azure ML model registry
        ↓
Managed online endpoint
        ↓
Fraud-risk prediction API
```

> This is a research and portfolio project based on a limited dataset. It is not a production banking system and must not be used for real financial decisions without extensive validation, security review, governance, and regulatory approval.

---

## Business Problem

Digital-payment fraud can occur through multiple channels, including:

- UPI.
- Internet banking.
- IMPS.
- NEFT.
- RTGS.
- Debit cards.
- Credit cards.
- Mobile wallets.

Banks and fintech companies need to identify suspicious transactions quickly while avoiding unnecessary declines of legitimate customer payments.

FinRisk360 aims to support fraud operations by:

1. Identifying suspicious transactions.
2. Estimating fraud probability.
3. Prioritizing transactions for investigation.
4. Providing explainable risk signals.
5. Supporting real-time scoring through an Azure ML endpoint.

The system is designed as a decision-support tool, not an autonomous financial-decision system.

---

## Project Objectives

- Analyze large-scale transaction data using Azure Databricks and Apache Spark.
- Clean and validate financial transaction data.
- Engineer behavioral, transaction, customer, and risk-related features.
- Track Databricks processing and experiments with MLflow where required.
- Use Azure Machine Learning AutoML for model experimentation.
- Compare candidate fraud-detection models.
- Register the approved model in Azure Machine Learning.
- Deploy the model to an Azure ML managed online endpoint.
- Return fraud probability, risk band, and recommended action.
- Provide model explanations using SHAP.
- Demonstrate an end-to-end cloud MLOps workflow.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │ Raw Transaction Data│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure Storage        │
                    │ Data Lake / Blob     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure Databricks     │
                    │                     │
                    │ - Data validation   │
                    │ - EDA               │
                    │ - Spark processing  │
                    │ - Feature engineering│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Versioned Feature    │
                    │ Dataset              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure ML AutoML      │
                    │                     │
                    │ - Model search      │
                    │ - Model comparison  │
                    │ - Evaluation        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure ML + MLflow    │
                    │ Experiment Tracking  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Azure ML Model       │
                    │ Registry             │
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
       │ Dashboard        │         │                  │
       └──────────────────┘         └──────────────────┘
```

---

## Technology Stack

### Data engineering and analysis

- Azure Databricks.
- Apache Spark.
- PySpark.
- Python.
- SQL.
- pandas.

### Machine learning

- Azure Machine Learning AutoML.
- scikit-learn.
- XGBoost or other AutoML-selected models.
- SHAP.
- Precision–recall analysis.
- Cost-sensitive threshold selection.

### Experiment tracking and MLOps

- MLflow in Azure Databricks for Databricks-side experiments, where required.
- MLflow in Azure Machine Learning for AutoML experiment tracking and final model lineage.
- Azure ML model registry.
- Azure ML managed online endpoint.
- GitHub for source control.
- GitHub Actions for basic testing.

### Application

- Streamlit.
- REST API.
- JSON input and output.

---

## About Dataset

🏦 Indian Banking Transactions Dataset - Data Dictionary From Kaggle.com
[Link_to_the_dataset](https://www.kaggle.com/datasets/belbino/indian-banking-transactions-20192024)

Dataset Overview

|Property |	Value|
|---|---:|
|Rows	|550,000|
|Columns |	20|
|Date Range	| 2019-01-01 → 2024-01-01 (5 Years)|
|Domain	| Retail Banking / Financial Transactions|
|Target Variable |	is_fraud|
|Fraud Rate	| ~0.89% (realistic class imbalance) |
|Geography |	India (10 major states) |



---

## Data Processing in Azure Databricks

Azure Databricks is used for big-data analysis and feature engineering.

### Processing workflow

```text
Raw data
   ↓
Schema validation
   ↓
Data-quality checks
   ↓
Duplicate removal
   ↓
Missing-value handling
   ↓
Leakage review
   ↓
Feature engineering
   ↓
Feature dataset output
```

### Data-quality checks

The Databricks workflow checks:

- Column names and data types.
- Missing values.
- Duplicate transactions.
- Invalid numerical values.
- Unexpected categorical values.
- Fraud-label consistency.
- Identifier uniqueness.
- Class distribution.
- Feature availability at prediction time.

### Engineered features

Examples include:

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

Every engineered feature is reviewed for:

- Business meaning.
- Availability at decision time.
- Target leakage.
- Missing values.
- Extreme values.
- Production usability.

---

## MLflow Strategy

MLflow is used in both platforms, but for different purposes.

### MLflow in Azure Databricks

Databricks-side MLflow is used optionally to track:

- Data-processing jobs.
- Feature-engineering versions.
- Spark-based model experiments.
- Input and output dataset versions.
- Data-quality statistics.
- Feature counts.
- Git commit information.

Example metadata:

```text
source_dataset = indian-digital-payment-fraud
feature_version = v1
processing_platform = azure-databricks
feature_count = <value>
row_count = <value>
```

### MLflow in Azure Machine Learning

Azure ML MLflow is the authoritative tracking layer for the final modeling workflow.

It tracks:

- AutoML runs.
- Candidate models.
- Parameters.
- Metrics.
- Validation results.
- Feature schema.
- Model artifacts.
- Dataset version.
- Model version.
- Deployment metadata.

### Model registry decision

The final approved model is registered in the Azure Machine Learning model registry.

The same final model is not registered separately in multiple registries unless there is a specific organizational requirement.

The simplified lifecycle is:

```text
Databricks MLflow
        ↓
Track data and feature engineering
        ↓
Azure ML data asset
        ↓
Azure ML MLflow
        ↓
Track AutoML experiments
        ↓
Azure ML model registry
        ↓
Azure ML endpoint
```

Azure Databricks provides MLflow tracking and model lifecycle capabilities, while Azure ML supports MLflow-based tracking, model registration, and deployment workflows. [238][235]

---

## Azure Machine Learning AutoML

The engineered feature dataset is registered as an Azure ML data asset and used as input for AutoML.

### AutoML workflow

```text
Versioned feature dataset
        ↓
Azure ML classification AutoML job
        ↓
Candidate model training
        ↓
Metric comparison
        ↓
Best-model selection
        ↓
SHAP and error analysis
        ↓
Model registration
```

### Evaluation metrics

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

Accuracy is not used as the only success metric because fraud detection is usually an imbalanced classification problem.

### Results

Replace the placeholders below with actual values:

| Model | PR-AUC | ROC-AUC | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|---:|
| Baseline Logistic Regression | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` |
| AutoML Best Model | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` |

Do not publish placeholder metrics.

---

## Leakage Audit

Potentially sensitive or leakage-prone features include:

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
| Full valid feature set | Uses approved features after initial audit |
| Risk-score ablation | Removes precomputed risk-score features |
| Authentication ablation | Removes authentication-related fields |
| Context-only model | Uses transaction, customer, merchant, and behavioral context |

The purpose is to determine whether performance depends heavily on precomputed risk indicators or features that may not be available at the time of prediction.

---

## Risk-Based Decision Logic

The system returns a fraud probability and maps it to an operational risk band.

```text
Low risk       → Approve
Medium risk    → Analyst review
High risk      → Investigate or hold
```

Example:

```json
{
  "fraud_probability": 0.84,
  "risk_band": "High",
  "recommended_action": "Investigate",
  "model_version": "1"
}
```

The thresholds are selected using validation results, fraud recall, false-positive rate, and expected business cost.

The model is intended to support human decision-making. It does not independently approve, reject, or block real financial transactions.

---

## Explainability

SHAP is used to explain global model behavior and individual predictions.

Example:

```text
Fraud probability: 0.84
Risk band: High
Recommended action: Investigate

Main contributing factors:
- Transaction amount is significantly higher than usual.
- A new device was used.
- Transaction location does not match the customer's normal location.
- Multiple failed login attempts were recorded.
```

SHAP values describe features that influenced the model prediction. They should not be interpreted as proof that a feature caused fraud.

---

## Azure ML Deployment

The approved model is deployed to an Azure ML managed online endpoint for real-time inference.

```text
Registered model
        ↓
Scoring script
        ↓
Environment
        ↓
Managed online endpoint
        ↓
REST prediction request
```

Azure ML managed online endpoints are used for real-time model inference and deployment management. [165]

### Example API request

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

### Example response

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

## Streamlit Dashboard

The dashboard provides an analyst-style interface with:

### Transaction scoring

- Transaction input form.
- Fraud probability.
- Risk band.
- Recommended action.
- Reason codes.

### Model performance

- PR-AUC.
- Precision.
- Recall.
- Confusion matrix.
- SHAP feature importance.

### Risk overview

- Risk-band distribution.
- Fraud distribution.
- Payment-method analysis.
- Merchant-category analysis.
- State-level summary.

### Run locally

```bash
streamlit run dashboard/app.py
```

---

## Repository Structure

```text
finrisk360/
├── data/
│   └── README.md
├── databricks/
│   ├── notebooks/
│   │   ├── 01_data_audit.py
│   │   ├── 02_feature_engineering.py
│   │   └── 03_feature_export.py
│   ├── jobs/
│   │   └── feature_pipeline.yml
│   └── README.md
├── azureml/
│   ├── data_asset.yml
│   ├── automl_job.yml
│   ├── endpoint.yml
│   └── deployment.yml
├── src/
│   ├── validation.py
│   ├── preprocessing.py
│   ├── evaluate.py
│   ├── explain.py
│   └── predict.py
├── api/
│   └── score.py
├── dashboard/
│   └── app.py
├── tests/
│   ├── test_validation.py
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
├── requirements.txt
├── Dockerfile
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
pytest -v
```

### Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

## Azure Databricks Setup

Use Azure Databricks for large-scale data analysis and feature engineering.

The Databricks workflow should:

1. Read data from Azure Storage.
2. Validate the schema.
3. Analyze missing values and duplicates.
4. Create engineered features with PySpark.
5. Write the curated feature dataset.
6. Record feature and dataset metadata.
7. Make the output available to Azure ML.

Example output:

```text
abfss://features@<STORAGE_ACCOUNT>.dfs.core.windows.net/fraud_features/
```

Do not commit storage account keys or connection strings. Use managed identity, secret scopes, or secure environment configuration.

---

## Azure Machine Learning Setup

Install the Azure ML CLI extension:

```bash
az extension add -n ml
```

Log in:

```bash
az login
```

Set the subscription:

```bash
az account set --subscription "<SUBSCRIPTION_ID>"
```

Register the engineered feature dataset:

```bash
az ml data create \
  --file azureml/data_asset.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>"
```

Submit the AutoML job:

```bash
az ml job create \
  --file azureml/automl_job.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>"
```

Create the endpoint:

```bash
az ml online-endpoint create \
  --file azureml/endpoint.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>"
```

Deploy the model:

```bash
az ml online-deployment create \
  --file azureml/deployment.yml \
  --resource-group "<RESOURCE_GROUP>" \
  --workspace-name "<WORKSPACE_NAME>" \
  --endpoint-name "<ENDPOINT_NAME>"
```

Replace all placeholder values with your Azure resources.

---

## Testing

The test suite checks:

- Schema validation.
- Missing-value handling.
- Feature calculations.
- Input validation.
- Prediction probability range.
- Risk-band assignment.
- Model loading.
- API responses.
- Invalid request handling.

Run:

```bash
pytest -v
```

GitHub Actions runs the test suite on pushes and pull requests.

---

## Security

Never commit:

```text
.env
Azure credentials
API keys
Storage connection strings
Access tokens
Raw sensitive transaction data
Private certificates
```

Recommended `.gitignore` entries:

```gitignore
.venv/
.env
.vscode/
__pycache__/
.ipynb_checkpoints/
data/raw/
data/processed/
*.csv
*.parquet
*.key
*.pem
```

For real Azure deployments, use secure authentication such as managed identities, secret management, or federated GitHub authentication.

---

## Limitations

This project is a proof of concept.

Known limitations include:

- The dataset is limited in size.
- The dataset may be synthetic or simulated.
- The fraud distribution may not match real production traffic.
- Precomputed risk features may introduce target leakage.
- A reliable transaction timestamp may not be available.
- The model has not been validated on live banking data.
- The model may not generalize to other banks, customers, or payment platforms.
- No production financial decision should be made solely from this model.
- Real deployment would require privacy, security, fairness, governance, monitoring, and regulatory review.

---

## Future Improvements

- Add reliable transaction timestamps.
- Use chronological validation.
- Add customer and merchant velocity features.
- Add model-drift monitoring.
- Add analyst feedback.
- Add human-in-the-loop review workflows.
- Add challenger models.
- Add model rollback procedures.
- Add automated retraining.
- Add Azure Monitor and Application Insights dashboards.
- Add graph-based customer–merchant analysis.
- Test on a larger independently sourced dataset.
- Add secure private networking for the endpoint.

Azure ML supports endpoint deployment and security configurations such as restricting public network access for managed online endpoints. [240]

---

## Learning Outcomes

This project demonstrates experience with:

- Azure Databricks.
- Apache Spark.
- PySpark.
- SQL.
- Big-data analysis.
- Feature engineering.
- Data validation.
- Fraud detection.
- Imbalanced classification.
- Precision–recall evaluation.
- Leakage analysis.
- AutoML.
- MLflow.
- Azure Machine Learning.
- Model registration.
- Online endpoint deployment.
- SHAP explainability.
- Streamlit.
- GitHub.
- GitHub Actions.
- MLOps fundamentals.

---

## Author

**<YOUR_NAME>**

- GitHub: [@<YOUR_GITHUB_USERNAME>](https://github.com/<YOUR_GITHUB_USERNAME>)
- LinkedIn: [<YOUR_LINKEDIN_PROFILE>](<YOUR_LINKEDIN_URL>)
- Email: `<YOUR_EMAIL>`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Durrain Khan**

- LinkedIn: [<YOUR_LINKEDIN_PROFILE>](https://www.linkedin.com/in/durrain-khan-pathan-728762304/)
- Email: `durrainpathan123@gmail.com`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
