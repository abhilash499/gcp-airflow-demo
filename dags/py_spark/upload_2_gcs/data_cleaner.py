import sys
import os
from pyspark.sql import SparkSession


# Define dependency module paths for execution in dataproc.
if os.path.exists('artifacts.zip'):
    sys.path.insert(0, 'artifacts.zip')
else:
    sys.path.insert(0, 'artifacts')

from arguments.args_data_cleaner import get_arguments
from common.get_gs_paths_by_partition import get_gs_paths_by_hour_partition
from common.logger_adapter import PySparkLoggerAdapter, JobLogger
from transformation import trans_data_cleaner as data_transformer


# Retrieve command line arguments into a dict for further use.
args = get_arguments()


# Define Configurations
SHOULD_PREFIX_PARTITION = bool(int(args.get("SHOULD_PREFIX_PARTITION")))
INPUT_DATA_RANGE_IN_HOURS = int(args.get("INPUT_DATA_RANGE_IN_HOURS"))
CURRENT_TIMESTAMP = args.get("CURRENT_TIMESTAMP")
SKIP_LAST_N_HOURS_INPUT_DATA = int(args.get("SKIP_LAST_N_HOURS_INPUT_DATA"))
RAW_DATA_BUCKET_NAME = args.get("RAW_DATA_BUCKET_NAME")
RAW_DATA_BUCKET_KEY = args.get("RAW_DATA_BUCKET_KEY")
ANONYMIZED_DATA_BUCKET_NAME = args.get("ANONYMIZED_DATA_BUCKET_NAME")
ANONYMIZED_DATA_BUCKET_KEY = args.get("ANONYMIZED_DATA_BUCKET_KEY")
ANONYMIZE_DATA_COLUMN_NAME = args.get("ANONYMIZE_DATA_COLUMN_NAME")

# Create Spark Session.
spark = SparkSession.builder.appName("data-cleaner").getOrCreate()


# Define Spark Logger
logger_adapter = PySparkLoggerAdapter(spark)
spark_logger = JobLogger(logger_adapter)


# Extract all respective input data
paths = get_gs_paths_by_hour_partition(RAW_DATA_BUCKET_NAME,
                                       RAW_DATA_BUCKET_KEY,
                                       skip_last_n_hours=SKIP_LAST_N_HOURS_INPUT_DATA,
                                       hours_in_range=INPUT_DATA_RANGE_IN_HOURS,
                                       current_timestamp=CURRENT_TIMESTAMP,
                                       should_prefix_partition=SHOULD_PREFIX_PARTITION,
                                       )


print(paths)

df = spark.read \
    .option("header", "true") \
    .csv(paths)

print(df.head())


# Process extracted data
df_filtered = data_transformer.transform(df, ANONYMIZE_DATA_COLUMN_NAME)


# Save processed data
df_filtered.write \
    .option("compression", "gzip")\
    .mode("overwrite")\
    .csv('gs://' + ANONYMIZED_DATA_BUCKET_NAME + '/' + ANONYMIZED_DATA_BUCKET_KEY)


# Print overall job metrics
spark_logger.info("INFO: INPUT COLUMNS ARE {}".format(df.columns))
spark_logger.info("INFO: INPUT COUNT = {}".format(df.count()))
spark_logger.info("INFO: OUTPUT COLUMNS ARE {}".format(df_filtered.columns))
spark_logger.info("INFO: OUTPUT COUNT = {}".format(df_filtered.count()))
spark_logger.info("INFO: JOB Completed")
