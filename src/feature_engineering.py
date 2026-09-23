from pyspark.sql import functions as F


def transaction_minute_extract(df, ts_col="transaction_datetime"):
    if ts_col not in df.columns:
        raise ValueError(f"ts_col '{ts_col}' not found in df.columns")
    else:
        df = df.withColumn(
            "transaction_minute",
            F.minute(F.col(ts_col))
        )
        return df
    
def amount_to_average_ratio(df,customer_id = None, transaction_amount = 100):
    if customer_id:
        atvr = df.filter(F.col("customer_id") == customer_id).agg(F.mean("transaction_amount")).collect()[0][0]
        if atvr:
            return atvr / transaction_amount
        else:
            return 1
    else:
        return 1

def prior_transaction_count(df,customer_id = None):
    if customer_id:
        ptc = df.filter(F.col("customer_id") == customer_id).agg(F.count("transaction_amount")).collect()[0][0]
        if ptc:
            return ptc
        else:
            return 0
    else:
        return 0





