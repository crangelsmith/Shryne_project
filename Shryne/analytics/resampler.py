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
        return sum(x)/len(x)


def resampler_dataframe(df, period = 'D'):

    time_field = 'sent_at'

    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pd.to_datetime(df[time_field])
    else:
        print("nothing to be done")

    output_df = pd.DataFrame()

    df["sentiment_mag"] = (df["positive"]-df["negative"])



    # first set up the time axis analysis for either month or day
    output_df["time"] = df[time_field].value_counts().resample(period)
    output_df["message_count"] = df[time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_user"] = df[df["is_user"] == True][time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_contact"] = df[df["is_user"] == False][time_field].value_counts().resample(period, how=_sum)


    df.set_index(time_field,inplace=True)
    output_df["sentiment_pos"] = df["positive"].resample(period, how=_average)
    output_df["sentiment_neg"] = df["negative"].resample(period, how=_average)
    output_df["sentiment_neu"] = df["neutral"].resample(period, how=_average)
    output_df["word_count"] = df["word_count"].resample(period, how=_sum)

    output_df["sentiment_mag"] = df["sentiment_mag"].resample(period, how=_average)


    #TODO: NEED TO DECIDE HOW TO DEFINE THIS SENTIMENT VARIABLE PROPERLY

    output_df["sentiment_pos_user"] = df[df["is_user"]==True]["positive"].resample(period, how=_average)
    output_df["sentiment_neg_user"] = df[df["is_user"]==True]["negative"].resample(period, how=_average)
    output_df["sentiment_neu_user"] = df[df["is_user"] == True]["neutral"].resample(period, how=_average)
    output_df["sentiment_mag_user"] = df[df["is_user"] == True]["sentiment_mag"].resample(period, how=_average)
    output_df["word_count_user"] = df[df["is_user"] == True]["word_count"].resample(period, how=_sum)

    output_df["sentiment_pos_contact"] = df[df["is_user"] == False]["positive"].resample(period, how=_average)
    output_df["sentiment_neg_contact"] = df[df["is_user"] == False]["negative"].resample(period, how=_average)
    output_df["sentiment_neu_contact"] = df[df["is_user"] == False]["neutral"].resample(period, how=_average)
    output_df["sentiment_mag_contact"] = df[df["is_user"] == False]["sentiment_mag"].resample(period, how=_average)
    output_df["word_count_contact"] = df[df["is_user"] == False]["word_count"].resample(period, how=_sum)

    output_df["sentiment_reciprocity"]=(output_df["sentiment_mag_contact"]-output_df["sentiment_mag_user"]).abs()

    output_df["message_count_reciprocity"] =find_ratio(output_df,"message_count")
    output_df["word_count_reciprocity"] =find_ratio(output_df,"word_count")

    return output_df


def find_ratio(df,variable):

    ratio_array = np.array(df[variable+"_user"].size)
    index = df[variable+"_user"].values > df[variable+"_contact"].values

    ratio_array[index] = df[variable+"_contact"][index].values / df[variable+"_user"][index].values
    ratio_array[~index] = df[variable+"_user"][~index].values / df[variable+"_contact"][~index].values

    return ratio_array







