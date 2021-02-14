from datetime import datetime
import time


def zero_fill(number):
    return str(number).zfill(2)


def utc_datetime_list_by_hour(hours_in_range, current_timestamp, skip_last_n_hours):
    return [datetime.utcfromtimestamp(current_timestamp - ((hour + skip_last_n_hours) * 60 * 60))
            for hour in range(0, hours_in_range)]


def get_end_timestamp(current_timestamp):
    return time.time() if (current_timestamp == 'now') else int(current_timestamp)


def get_gs_paths_by_hour_partition(gs_bucket_name, gs_bucket_key, current_timestamp, hours_in_range=24,
                                   skip_last_n_hours=1, gs_protocol="gs", partition_prefix="event",
                                   should_prefix_partition=True):
    datetime_list = utc_datetime_list_by_hour(hours_in_range=hours_in_range,
                                              current_timestamp=get_end_timestamp(current_timestamp),
                                              skip_last_n_hours=skip_last_n_hours)

    if should_prefix_partition:
        result = [
            "{}://{}/{}/{}_year={}/{}_month={}/{}_day={}/{}_hour={}".format(
                gs_protocol, gs_bucket_name, gs_bucket_key, partition_prefix, date.year, partition_prefix,
                zero_fill(date.month), partition_prefix, zero_fill(date.day), partition_prefix, zero_fill(date.hour)
            ) for date in datetime_list]
        print(result)
        return result

    result = [
        "{}://{}/{}/{}/{}/{}/{}".format(
            gs_protocol, gs_bucket_name, gs_bucket_key, date.year, zero_fill(date.month),
            zero_fill(date.day), zero_fill(date.hour)
        ) for date in datetime_list]
    print(result)
    return result


def get_gs_paths_by_published_day(gs_bucket_name, gs_bucket_key, current_timestamp, hours_in_range=24,
                                  skip_last_n_hours=1, gs_protocol="gs"):

    datetime_list = utc_datetime_list_by_hour(hours_in_range=hours_in_range,
                                              current_timestamp=get_end_timestamp(current_timestamp),
                                              skip_last_n_hours=skip_last_n_hours)

    result = [
        "{}://{}/{}/published_year={}/published_month={}/published_day={}".format(
            gs_protocol, gs_bucket_name, gs_bucket_key, date.year, zero_fill(date.month), zero_fill(date.day)
        ) for date in datetime_list]
    unique_gs_paths = list(set(result))
    print(unique_gs_paths)
    return unique_gs_paths
