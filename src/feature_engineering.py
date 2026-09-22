from pyspark.ml import Transformer
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import functions as F


class EncodingPipeline(Transformer):
    def __init__(self, one_hot=None, freq=None):
        super().__init__()
        self.one_hot = one_hot or []
        self.freq = freq or []

    def _transform(self, df):
        for c in self.one_hot:
            idx = f"{c}_index"
            vec = f"{c}_encoded"
            df = StringIndexer(inputCol=c, outputCol=idx, handleInvalid="keep").fit(df).transform(df)
            df = OneHotEncoder(inputCols=[idx], outputCols=[vec], dropLast=False).fit(df).transform(df).drop(idx)
            df = df.drop(c)

        for c in self.freq:
            m = df.groupBy(c).count().withColumnRenamed("count", f"{c}_freq")
            df = df.join(m, c, "left")
            df = df.drop(c)

        return df
    

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





