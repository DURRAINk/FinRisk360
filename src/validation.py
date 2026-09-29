# src/validation.py

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, NumericType


NUMERIC_COLUMNS = [
    "transaction_amount",
    "emi_amount",
    "credit_score",
    "prior_transaction_count",
    "amount_to_average_ratio",
]

STRING_COLUMNS = [
    "account_type",
    "transaction_type",
    "merchant_category",
    "state",
    "loan_type",
    "channel",
    "kyc_status",
]

TIME_COLUMNS = [
    "transaction_hour",
    "transaction_minute",
]


def check(condition, message):
    if condition:
        print(f"Validation successful: {message}")
    else:
        raise ValueError(f"Validation failed: {message}")


def validate_data(df):
    # Check null values
    columns = NUMERIC_COLUMNS + STRING_COLUMNS + TIME_COLUMNS + ["is_fraud"]

    null_count = df.select(
        sum(
            F.col(column).isNull().cast("int")
            for column in columns
        )
    ).first()[0]

    check(
        null_count == 0,
        "no null values found",
    )

    # Check numerical data types and negative values
    schema = dict(df.dtypes)

    for column in NUMERIC_COLUMNS:
        check(
            isinstance(
                df.schema[column].dataType,
                NumericType,
            ),
            f"{column} is numerical",
        )

        negative_count = df.filter(
            F.col(column) < 0
        ).limit(1).count()

        check(
            negative_count == 0,
            f"{column} contains no negative values",
        )

    # Check string data types
    for column in STRING_COLUMNS:
        check(
            isinstance(
                df.schema[column].dataType,
                StringType,
            ),
            f"{column} is a string",
        )

    # Check time ranges
    check(
        df.filter(
            (F.col("transaction_hour") < 0)
            | (F.col("transaction_hour") > 23)
        ).limit(1).count() == 0,
        "transaction_hour is between 0 and 23",
    )

    check(
        df.filter(
            (F.col("transaction_minute") < 0)
            | (F.col("transaction_minute") > 59)
        ).limit(1).count() == 0,
        "transaction_minute is between 0 and 59",
    )

    # Check fraud labels
    check(
        df.filter(
            ~F.col("is_fraud").isin([0, 1])
        ).limit(1).count() == 0,
        "is_fraud contains only 0 and 1",
    )

    print("All validations passed successfully.")
    return df