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

        return df
