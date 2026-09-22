# Feature Engineering Specification

## Project

FinRisk360 — Explainable Digital-Payment Fraud Detection

## Version

`fraud_features_v1`

## Purpose

This document defines the engineered features used by the fraud-detection
pipeline. The features are created in Azure Databricks using PySpark and
consumed by Azure Machine Learning for model training and deployment.

The features are designed to be available at transaction-scoring time and
must not use the current transaction or future transactions when calculating
historical customer behavior.

---

## Feature 1: `amount_to_average_ratio`

### Description

Measures how large the current transaction is compared with the customer’s
average transaction amount before the current transaction.

### Business purpose

Fraudulent transactions may be unusually large relative to a customer’s
normal behavior. This feature captures customer-specific transaction
deviation rather than relying only on the absolute transaction amount.

### Formula

```text
amount_to_average_ratio = transaction_amount / 
                        historical_average_transaction_amount
```

The historical average is calculated using only transactions from the same
customer that occurred before the current transaction.

### Source columns

```text
customer_id
transaction_datetime
transaction_amount
```

### Availability

Available at transaction-scoring time if the customer’s prior transaction
history can be retrieved.

### Leakage controls

- The current transaction is excluded from the historical average.
- Future transactions are excluded.
- `customer_id` is used only as a grouping or lookup key.
- `customer_id` is not passed to the ML model as a predictive feature.
- The feature must be generated using point-in-time-correct logic.

### Edge-case handling

| Condition | Treatment |
|---|---|
| No prior customer history | Set ratio to `1.0` |
| Historical average is null | Set ratio to `1.0` |
| Historical average is zero | Set ratio to `1.0` |

### Example

```text
Customer historical average: ₹1,500
Current transaction amount: ₹12,000
amount_to_average_ratio: 8.0
```

---

## Feature 2: `transaction_minutes`

### Description

Represents the number of minutes after midnight when the transaction
occurred.

### Business purpose

Transaction behavior can vary by time of day. This feature allows the model
to learn patterns such as unusual temporal activity or customer behavior
outside normal transaction hours.

### Source columns

```text
transaction_time
```

or, if available:

```text
transaction_hour
transaction_minute
```

### Valid range

```text
0 to 60
```

### Availability

Available at transaction-scoring time.
---


```text
customer_id
transaction_id
transaction_ts
```

## Feature 3: `prior_transaction_count`
### Description

The number of transactions previously completed by the same customer before
the current transaction.

### Business purpose

This feature represents the customer’s prior activity level. A transaction
from a customer with little or no history may require greater scrutiny than
a transaction from a well-established customer.

### Calculation

```text
prior_transaction_count = count of the customer’s 
                            transactions before transaction_ts
```

### Source columns

```text
customer_id
transaction_amount
transaction_ts
```

### Availability and leakage control

- Calculated using only transactions before the current transaction.
- The current transaction is excluded.
- Future transactions are excluded.
- `customer_id` is used only as a grouping or lookup key.
- `customer_id` is excluded from the model’s predictive input columns.

### Edge-case handling

| Condition | Treatment |
|---|---|
| First customer transaction | Set to `0` |
| Missing customer ID | Quarantine or apply a documented fallback |
| Duplicate timestamp | Use `transaction_id` as a deterministic tie-breaker |
| Invalid transaction timestamp | Quarantine for data-quality review |

### Example

```text
Customer prior transactions: 7
Current transaction: 8th transaction
prior_transaction_count: 7
```

### Expected type and range

```text
Data type: Integer
Minimum value: 0
Maximum value: Dataset-dependent
```

### Leakage risk

Medium. The feature is valid only when computed with point-in-time-correct
logic. Using a full-dataset customer count would include future activity and
could inflate model performance.


## Recommended model features include:

```text
 'account_type',
 'transaction_type',
 'transaction_amount',
 'transaction_direction',
 'merchant_category',
 'state',
 'credit_score',
 'loan_type',
 'emi_amount',
 'channel',
 'kyc_status',
 'transaction_hour',
 'transaction_minute',
 'prior_transaction_count',
 'amount_to_average_ratio'
```
---

## Validation requirements

Before exporting the feature dataset, verify:

- `amount_to_average_ratio >= 0`
- `transaction_minutes` is between `0` and `60`
- No current transaction is included in its historical average.
- No future transaction is included in the historical average.
- `customer_id` is not included in the model input matrix.
- First-time customers are handled consistently.
- Missing timestamps are reported.
- Duplicate transaction ordering is deterministic.
- Feature values are versioned.
- Feature output row count matches the input row count unless invalid records
  are intentionally quarantined.

---

## Data lineage

```text
Raw transaction data
        ↓
Azure Databricks validation
        ↓
PySpark feature engineering
        ↓
fraud_features_v1
        ↓
Azure ML data asset
        ↓
AutoML training and evaluation
        ↓
Registered fraud model
        ↓
Azure ML online endpoint
```

## Version history

### `fraud_features_v1`

- Added `amount_to_average_ratio`.
- Added `prior_transaction_count`.
- Added `transaction_minutes`.
- Implemented point-in-time customer history logic.
- Excluded identifiers from model inputs.

## Limitations

- Historical features require reliable transaction ordering.
- New customers may have no prior transaction history.
- A production deployment requires a low-latency customer-history lookup or
  online feature store.
- The dataset must be independently checked for synthetic patterns and
  target leakage before production use.