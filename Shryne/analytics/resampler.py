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


def resampler_dataframe(df, period='D'):
    time_field = 'sent_at'

    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pd.to_datetime(df[time_field])
    else:
        print("nothing to be done")

    output_df = pd.DataFrame()

    df["sentiment_mag"] = (df["positive"] - df["negative"])

    # first set up the time axis analysis for either month or day
    output_df["time"] = df[time_field].value_counts().resample(period)
    output_df["message_count"] = df[time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_user"] = df[df["is_user"] == True][time_field].value_counts().resample(period, how=_sum)
    output_df["message_count_contact"] = df[df["is_user"] == False][time_field].value_counts().resample(period,
                                                                                                        how=_sum)

    df.set_index(time_field, inplace=True)
    output_df["sentiment_pos"] = df["positive"].resample(period, how=_average)
    output_df["sentiment_neg"] = df["negative"].resample(period, how=_average)
    output_df["sentiment_neu"] = df["neutral"].resample(period, how=_average)
    output_df["word_count"] = df["word_count"].resample(period, how=_sum)

    output_df["sentiment_mag"] = df["sentiment_mag"].resample(period, how=_average)

    # TODO: NEED TO DECIDE HOW TO DEFINE THIS SENTIMENT VARIABLE PROPERLY

    output_df["sentiment_pos_user"] = df[df["is_user"] == True]["positive"].resample(period, how=_average)
    output_df["sentiment_neg_user"] = df[df["is_user"] == True]["negative"].resample(period, how=_average)
    output_df["sentiment_neu_user"] = df[df["is_user"] == True]["neutral"].resample(period, how=_average)
    output_df["sentiment_mag_user"] = df[df["is_user"] == True]["sentiment_mag"].resample(period, how=_average)
    output_df["word_count_user"] = df[df["is_user"] == True]["word_count"].resample(period, how=_sum)

    output_df["sentiment_pos_contact"] = df[df["is_user"] == False]["positive"].resample(period, how=_average)
    output_df["sentiment_neg_contact"] = df[df["is_user"] == False]["negative"].resample(period, how=_average)
    output_df["sentiment_neu_contact"] = df[df["is_user"] == False]["neutral"].resample(period, how=_average)
    output_df["sentiment_mag_contact"] = df[df["is_user"] == False]["sentiment_mag"].resample(period, how=_average)
    output_df["word_count_contact"] = df[df["is_user"] == False]["word_count"].resample(period, how=_sum)

    output_df["sentiment_reciprocity"] = (output_df["sentiment_mag_contact"] - output_df["sentiment_mag_user"]).abs()

    output_df["message_count_reciprocity"] = find_ratio(output_df, "message_count")
    output_df["word_count_reciprocity"] = find_ratio(output_df, "word_count")

    return output_df


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
