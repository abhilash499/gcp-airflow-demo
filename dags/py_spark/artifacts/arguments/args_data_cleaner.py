import sys
import getopt


def get_arguments():
    should_prefix_partition = None
    current_timestamp = None
    skip_last_n_hours = None
    input_data_range_in_hours = None
    raw_data_bucket_name = None
    raw_data_bucket_key = None
    anonymized_data_bucket_name = None
    anonymized_data_bucket_key = None
    anonymized_data_column_name = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "spp:ct:slnh:idrih:rdbn:rdbk:adbn:adbk:adcn:",
                                   ["should_prefix_partition =",
                                    "current_timestamp =",
                                    "skip_last_n_hours =",
                                    "input_data_range_in_hours =",
                                    "raw_data_bucket_name =",
                                    "raw_data_bucket_key =",
                                    "anonymized_data_bucket_name =",
                                    "anonymized_data_bucket_key =",
                                    "anonymized_data_column_name ="
                                    ])
    except:
        print("Error")

    for opt, arg in opts:
        if opt in ['-spp', '--should_prefix_partition ']:
            should_prefix_partition = arg
        elif opt in ['-ct', '--current_timestamp ']:
            current_timestamp = arg
        elif opt in ['-slnh', '--skip_last_n_hours ']:
            skip_last_n_hours = arg
        elif opt in ['-idrih', '--input_data_range_in_hours ']:
            input_data_range_in_hours = arg
        elif opt in ['-rdbn', '--raw_data_bucket_name ']:
            raw_data_bucket_name = arg
        elif opt in ['-rdbk', '--raw_data_bucket_key ']:
            raw_data_bucket_key = arg
        elif opt in ['-adbn', '--anonymized_data_bucket_name ']:
            anonymized_data_bucket_name = arg
        elif opt in ['-adbk', '--anonymized_data_bucket_key ']:
            anonymized_data_bucket_key = arg
        elif opt in ['-adcn', '--anonymized_data_column_name ']:
            anonymized_data_column_name = arg

    job_args = {
        "SHOULD_PREFIX_PARTITION": should_prefix_partition,
        "CURRENT_TIMESTAMP": current_timestamp,
        "SKIP_LAST_N_HOURS_INPUT_DATA": skip_last_n_hours,
        "INPUT_DATA_RANGE_IN_HOURS": input_data_range_in_hours,
        "RAW_DATA_BUCKET_NAME": raw_data_bucket_name,
        "RAW_DATA_BUCKET_KEY": raw_data_bucket_key,
        "ANONYMIZED_DATA_BUCKET_NAME": anonymized_data_bucket_name,
        "ANONYMIZED_DATA_BUCKET_KEY": anonymized_data_bucket_key,
        "ANONYMIZED_DATA_COLUMN_NAME": anonymized_data_column_name,
    }

    return job_args
