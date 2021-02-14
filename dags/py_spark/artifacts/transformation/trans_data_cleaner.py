from pyspark.sql.functions import explode, col, split, concat_ws, udf, lit, coalesce, regexp_replace
from pyspark.sql.functions import when, lpad, length
from pyspark.sql.functions import to_timestamp, year, month, dayofmonth, hour, to_utc_timestamp, unix_timestamp

from hashlib import sha256


def transform(df, column_name):

    return df
