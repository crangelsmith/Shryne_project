import pandas as pd
import numpy as np


def _sum(x):
    if len(x) == 0:
        return 0
    else:
        return sum(x)


def _average(x):
    if len(x) == 0:
        return 0
    else:
        return sum(x) / len(x)


def _average_sentiment(x):
    return np.nanmean(x)


def _average_time(x):

    #TODO we may need to tweak the time limit
    time_limit = 6*3600  # in seconds
    try:
        x_mean = np.nanmean(x)
    except:
        return time_limit
    if x_mean > time_limit:
        return time_limit
    elif x_mean == 0:
        return time_limit
    else:
        return x_mean


def sentiment_cleaning(df):
    """Where neutral = 1 or if +ve, -ve
    and neutral = 0 then replace with nan"""

    mask_neutral = df["neutral"] == 1.0
    mask_zeroes = df[['positive', 'negative', 'neutral']].sum(axis=1) == 0

    for col in ['positive', 'negative', 'neutral', 'compound']:
        df[col].where(~mask_neutral, np.nan, inplace=True)
        df[col].where(~mask_zeroes, np.nan, inplace=True)
    return df


def find_ratio(df, variable):
    numerator_array = np.zeros(df[variable + "_user"].size)
    denominator_array = np.zeros(df[variable + "_user"].size)

    # here find the indexes where the assoicated user value is larger than the contact
    index = df[variable + "_user"].values > df[variable + "_contact"].values

    # where the above index is true (i.e. the user variable > contact variable)
    # place the user variable into the denominator and the contact variable in the
    # numerator.
    denominator_array[index] = df[variable + "_user"][index].values
    numerator_array[index] = df[variable + "_contact"][index].values

    # now for the indexes where the contact variable is > user variable
    # place it into the denominator and the user variable into the numerator.
    denominator_array[~index] = df[variable + "_contact"][~index].values
    numerator_array[~index] = df[variable + "_user"][~index].values

    # prevent div by 0 and compute ratio
    denominator_array[denominator_array == 0] = 1
    ratio_array = numerator_array / denominator_array

    #TODO: IF DENOMINATOR IS ==0 WE SHOULD SET RATIO TO 0.

    return ratio_array


def resample_dataframe(df, period='D'):
    '''
    This function resamples the features
    in the dataframe to the defined timeseries

    It create reciprocity features based on this
    resampling

    :param df: the dataframe to be resampled
    :param period: the resampling time interval
    :return: df with the resampled features
    '''

    #TODO perhaps this cleaning of sentiment should be outside the resampling of the dataframe
    df = sentiment_cleaning(df)

    time_field = 'sent_at'
    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pd.to_datetime(df[time_field])
    else:
        print("nothing to be done")

    output_df = pd.DataFrame()

    # get the message counts total and for the user and contact
    output_df["message_count"] = df[time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_user"] = df[~df["to_from"]][time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_contact"] = df[df["to_from"]][time_field].value_counts().resample(period, how=_sum)

    output_df['sent_at'] = df[time_field]

    df.set_index(time_field, inplace=True, drop=False)

    # get the total word counts and for the user and contact
    keys = ["word_count"]
    for k in keys:
        output_df[k] = df[k].resample(period, how=_sum)
        output_df[k + "_user"] = df[~df["to_from"]][k].resample(period, how=_sum)
        output_df[k + "_contact"] = df[df["to_from"]][k].resample(period, how=_sum)

    # get the sentiments overall and for the user and contact individually
    keys = ["positive", "negative", "neutral", "compound"]
    for k in keys:
        output_df[k] = df[k].resample(period, how=_average_sentiment)
        output_df[k + "_user"] = df[~df["to_from"]][k].resample(period, how=_average_sentiment)
        output_df[k + "_contact"] = df[df["to_from"]][k].resample(period, how=_average_sentiment)

    # get the time differences
    output_df["response_time"] = df["response_time"].resample(period, how=_average_time)
    output_df["response_time_user"] = df[~df["to_from"]]["response_time"].resample(period, how=_average_time)
    output_df["response_time_contact"] = df[df["to_from"]]["response_time"].resample(period, how=_average_time)

    # now compute reciprocity between users
    output_df["sentiment_reciprocity"] = (output_df["compound_contact"] - output_df["compound_user"]).abs()
    for k in ["message_count", "word_count", "response_time"]:
        output_df[k + "_reciprocity"] = find_ratio(output_df, k)

    # now normalise number of mesages, words, etc
    keys = ["word_count", "message_count",
            "message_count_user","message_count_contact",
            "word_count_user","word_count_contact"]
    for k in keys:
        output_df[k] = output_df[k] / (output_df[k].sum(axis=0))

    # compute the relative difference of the response time over the course of the relationship
    keys = ["response_time", "response_time_user", "response_time_contact"]
    for k in keys:
        if output_df[k].dropna().size == 0:
            denom = 1
        else:
            denom = output_df[k].dropna().size
        mean_time = output_df[k].sum(axis=0) / denom  # don't want to average with null months
        output_df[k] = (output_df[k] - mean_time) / mean_time

    # now reset dataframe values where there is only a single communication during the month from
    # each user.  This gets rid of comms where there are only single messages sent each month, which
    # where leading to issues in the ananlysis.
    no_comm_mask = (output_df['message_count_contact'] <= 1) | (output_df['message_count_user'] <= 1)
    keys = ['word_count_reciprocity', 'message_count_reciprocity', "response_time",
            "response_time_reciprocity", "sentiment_reciprocity"]
    values = [0, 0, 6*3600, 0, 1]
    for k, v in zip(keys, values):
        output_df[k].where(~no_comm_mask, v, inplace=True)

    return output_df
