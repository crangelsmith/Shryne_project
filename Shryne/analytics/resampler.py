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


def sentiment_cleaning(df):
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
    #TODO Should new features be constructed in here?
    df = sentiment_cleaning(df)

    time_field = 'sent_at'
    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pd.to_datetime(df[time_field])
    else:
        print("nothing to be done")

    output_df = pd.DataFrame()

    # get the time series
    output_df["time"] = df[time_field].value_counts().resample(period).apply(_sum)

    # get the message counts total and for the user and contact
    output_df["message_count"] = df[time_field].value_counts().resample(period).apply(_sum)
    output_df["message_count_user"] = df[~df["to_from"]][time_field].value_counts().resample(period).apply(_sum)
    output_df["message_count_contact"] = df[df["to_from"]][time_field].value_counts().resample(period).apply(_sum)

    df.set_index(time_field, inplace=True)

    # get the total words used by user and contact
    output_df["word_count"] = df["word_count"].resample(period).apply(_sum)

    # get the sentiments overall and for the user and contact individually
    keys = ["positive", "negative", "neutral", "compound"]
    for k in keys:
        output_df[k] = df[k].resample(period).apply(_average_sentiment)
        output_df[k+"_user"] = df[~df["to_from"]][k].resample(period).apply(_average_sentiment)
        output_df[k+"_contact"] = df[df["to_from"]][k].resample(period).apply(_average_sentiment)

    # user and contact word counts
    output_df["word_count_user"] = df[~df["to_from"]]["word_count"].resample(period).apply(_sum)
    output_df["word_count_contact"] = df[df["to_from"]]["word_count"].resample(period).apply(_sum)

    # now compute reciprocity between users
    output_df["sentiment_reciprocity"] = (output_df["compound_contact"] - output_df["compound_user"]).abs()
    output_df["message_count_reciprocity"] = find_ratio(output_df, "message_count")
    output_df["word_count_reciprocity"] = find_ratio(output_df, "word_count")

    return output_df