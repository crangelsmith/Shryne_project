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
    # First find and screen where there is only neutral sentiment.
    # These location indicate where vader cannot interpret the sentece
    # or where the sentiment is actually neutral.
    mask = df["neutral"] == 1.0
    for k in ['positive', 'negative', 'neutral', 'compound']:
        df[k][mask] = np.nan

    # also find where the sum of the sentiment is equal to 0
    # as this indicated an empty message
    mask = df[['positive', 'negative', 'neutral']].sum(axis=1) == 1.0
    for k in ['positive', 'negative', 'neutral', 'compound']:
        df[k][mask] = np.nan

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
    This function resamples and adds new features
    to the dataframe

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
    output_df["time"] = df[time_field].value_counts().resample(period, how=_sum)

    # get the message counts total and for the user and contact
    output_df["message_count"] = df[time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_user"] = df[df["to_from"] == False][time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_contact"] = df[df["to_from"] == True][time_field].value_counts().resample(period,
                                                                                                       how=_sum)

    df.set_index(time_field, inplace=True)

    # get the total words used by user and contact
    output_df["word_count"] = df["word_count"].resample(period, how=_sum)

    # get the mean sentiments for the user and contact
    feature_names = ["sentiment_pos", "sentiment_neg", "sentiment_neu", "sentiment_comp"]
    df_keys = ["positive", "negative", "neutral", "compound"]
    for f, k in zip(feature_names, df_keys):
        output_df[f] = df[k].resample(period, how=_average_sentiment)

    # get the individual sentiments for the user and the contact
    feature_names = ["sentiment_pos", "sentiment_neg", "sentiment_neu", "sentiment_comp"]
    df_keys = ["positive", "negative", "neutral", "compound"]
    for f, k in zip(feature_names, df_keys):
        output_df[f+"_user"] = df[df["to_from"] == False][k].resample(period, how=_average_sentiment)
        output_df[f+"_contact"] = df[df["to_from"] == True][k].resample(period, how=_average_sentiment)

    # user and contact word counts
    output_df["word_count_user"] = df[df["to_from"] == False]["word_count"].resample(period, how=_sum)
    output_df["word_count_contact"] = df[df["to_from"] == True]["word_count"].resample(period, how=_sum)

    # now compute reciprocities
    output_df["sentiment_reciprocity"] = (output_df["sentiment_mag_contact"] - output_df["sentiment_mag_user"]).abs()
    output_df["message_count_reciprocity"] = find_ratio(output_df, "message_count")
    output_df["word_count_reciprocity"] = find_ratio(output_df, "word_count")

    return output_df