from pyspark.sql import functions as F

def correct_datetime(df, date_col="transaction_date", ts_col="transaction_time"):
    if date_col not in df.columns:
        raise ValueError(f"date_col '{date_col}' not found in df.columns")
    if ts_col not in df.columns:
        raise ValueError(f"ts_col '{ts_col}' not found in df.columns")
    else:
        df = df.withColumn(
            "transaction_datetime",
            F.concat_ws(" ", F.col(date_col).cast("string"), F.date_format(F.col(ts_col), "HH:mm:ss"))
        ).withColumn(
            "transaction_datetime",
            F.to_timestamp("transaction_datetime", "yyyy-MM-dd HH:mm:ss")
        ).drop(date_col, ts_col)
        return df
   

def loan_type_preprocess(df):
    if 'loan_type' not in df.columns:
        raise ValueError(f"'loan_type' not found in df.columns")
    else:
        return df.withColumn('loan_type', F.when((F.col('has_loan') == 1) & (F.col('loan_type') == 'None'),
                                        F.lit('Unknown'))
                                    .otherwise(F.col('loan_type')))







