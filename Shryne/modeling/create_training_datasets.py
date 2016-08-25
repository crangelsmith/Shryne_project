import Shryne.config as config
import Shryne.analytics.resampler as resampler
import pandas as pd


# this function creates labeled samples for training the model.
# The idea is to use extreme behaviour for the labeling .
# This extremes are: high volume of communication and reciprocity vs low level of communications

def build_labeled_samples(df, model):

    # select subset of resampled input dataframe based on the model we'll train
    selection_mask = (df['relationship'] != "Family") & (df['relationship'] != "Friend") & (df['relationship'] != "General")
    if model == "romantic":
        df = df[selection_mask]
    else:
        df = df[~selection_mask]


    list_good = []
    list_bad = []

    # iterate over all relationships and pick the extreme values

    unique_contacts = df['contact_id'].unique()
    for unique_contact in unique_contacts:

        df_rel = df[df['contact_id'] == unique_contact]

        # resample per relationship
        df_rel = resampler.resample_dataframe(df_rel, config.resampler['period'])

        df_rel = df_rel[df_rel["message_count"] != 0]

        #pick the 50% of the samples with higher volume of comunication

        top_volume = int(df_rel.shape[0] * config.extremes_sample['top'])
        high_volume_sample = df_rel.sort_values("message_count", ascending=False)[0:top_volume]

        #from the selected sample pick the 50% of the samples with higher reciprocity

        top_reciprocity = int(high_volume_sample.shape[0] * config.extremes_sample['top'])
        high_volume_reciprocity_sample = high_volume_sample.sort_values("message_count_reciprocity", ascending=False)[0:top_reciprocity]

        #pick the 30% of the samples with lower volume of comunication

        bottom_volume = int(df_rel.shape[0] * config.extremes_sample['bottom'])
        low_volume_sample = df_rel.sort_values("message_count", ascending=True)[0:bottom_volume]

        list_good.append(high_volume_reciprocity_sample)
        list_bad.append(low_volume_sample)

    ## create labels

    good_df = pd.concat(list_good)
    good_df['label'] = 1

    bad_df = pd.concat(list_bad)
    bad_df['label'] = 0

    labeled_sample = pd.concat([good_df, bad_df])

    return labeled_sample



