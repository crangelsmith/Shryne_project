#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import Shryne.config as config

from resampler import sentiment_cleaning
from resampler import _sum, _average, _average_time
from resampler import find_ratio
from resampler import resample_dataframe


def test_sentiment_cleaning():
    """
    Where neutral = 1 or if +ve, -ve
    and neutral = 0 then replace with nan
    """

    neutral_test = pd.DataFrame({'neutral': [1, 0, 1.000001, 0.999999, 1.0],
                                 'compound': [1, 1, 1, 1, 1],
                                 'positive': [1, 1, 1, 1, 1],
                                 'negative': [1, 1, 1, 1, 1]})

    neutral_pass = pd.DataFrame({'neutral': [np.NaN, 0, 1.000001, 0.999999,
                                             np.NaN],
                                 'compound': [np.NaN, 1, 1 ,1, np.NaN],
                                 'positive': [np.NaN, 1, 1, 1, np.NaN],
                                 'negative': [np.NaN, 1, 1, 1, np.NaN]})

    zeros_to_nan_test = pd.DataFrame({'positive' : [0], 'neutral':  [0],
                                       'negative': [0], 'compound': [1]})

    zeros_float_to_nan_test = pd.DataFrame({'positive': [0.0], 'neutral': [0.0],
                                      'negative': [0.0], 'compound': [1.0]})

    zeros_pass = pd.DataFrame({'positive': [np.NaN], 'neutral': [np.NaN],
                               'negative': [np.NaN], 'compound': [np.NaN]})

    unchanged_test = pd.DataFrame({'positive': [0, 0, 0, 1, 1, 1, 1],
                                   'neutral': [0, 1, 1, 0, 0, 1, 1],
                                   'negative': [1, 0, 1, 0, 1, 0, 1],
                                   'compound': [1, 1, 1, 1, 1, 1, 1]})

    assert sentiment_cleaning(neutral_test).equals(neutral_pass)

    assert sentiment_cleaning(zeros_to_nan_test).equals(zeros_pass)

    assert sentiment_cleaning(unchanged_test).equals(unchanged_test)

    assert sentiment_cleaning(zeros_float_to_nan_test).equals(zeros_pass)


def test_find_ratio():

    one_zero_test = pd.DataFrame({'message_count_user': [1],
                                  'message_count_contact': [0]})

    assert find_ratio(one_zero_test, 'message_count') == 0

    zero_one_test = pd.DataFrame({'message_count_user': [0],
                                  'message_count_contact': [1]})

    assert find_ratio(zero_one_test, 'message_count') == 0

    one_one_test = pd.DataFrame({'message_count_user': [1],
                                 'message_count_contact': [1]})

    assert find_ratio(one_one_test, 'message_count') == 1

    user = [1, 0, 0, 1, 0.5, 1.0, 0.0, 0.5, 0.6, 2, 1]

    contact = [0, 1, 0, 1, 0.5, 1.0, 0.0, 0.6, 0.5, 1, 2]

    ratio_pass = [0, 0 ,0 ,1, 1, 1, 0, 0.5/0.6, 0.5/0.6, 0.5, 0.5]

    for x in range(len(user)):
        test = pd.DataFrame({'message_count_user': [user[x]],
                             'message_count_contact': [contact[x]]})
        assert find_ratio(test, 'message_count') == ratio_pass[x]


def test__sum():
    empty_test = []
    empty_pass = 0

    sum_test = [1,2,3,4,5,6,7,8,9,10]
    sum_pass = 55

    nan_test = [np.nan, np.nan, np.nan]
    nan_pass = 0

    assert _sum(empty_test) == empty_pass
    assert _sum(sum_test) == sum_pass
    assert _sum(nan_test) == nan_pass


def test__average():
    empty_test = []

    avg_test = [1,2,3,4,5,6,7,8,9,10]
    avg_pass = 5.5

    nan_test = [np.nan, np.nan, np.nan]

    assert np.isnan(_average(empty_test))
    assert _average(avg_test) == avg_pass
    assert np.isnan(_average(nan_test))


def test__average_time():

    # set up correct time limit for testing
    if config.model == 'not_romantic':
        time_limit = config.resampler['response_time_limit_not_romantic'] * 3600  # in seconds
    elif config.model == 'romantic':
        time_limit = config.resampler['response_time_limit_romantic'] * 3600

    empty_test = []
    empty_pass = time_limit

    greater_than_time_limit = [time_limit + 1] * 2
    greater_than_time_limit_pass = time_limit

    zero_mean_time_limit = [0,0,0,0,0,0]
    zero_mean_time_limit_pass = time_limit

    less_than_time_limit = [1,2,3,4,5,6,7,8,9,10]
    less_than_time_limit_pass = 5.5

    nan_mean_time_limit = [np.nan,2,3,np.nan,np.nan,7,8,np.nan,np.nan,10]
    nan_mean_pass = 6.0

    assert _average_time(empty_test) == empty_pass
    assert _average_time(greater_than_time_limit) == greater_than_time_limit_pass
    assert _average_time(zero_mean_time_limit) == zero_mean_time_limit_pass
    assert _average_time(less_than_time_limit) == less_than_time_limit_pass
    assert _average_time(nan_mean_time_limit) == nan_mean_pass

def test_resample_dataframe():

    df = pd.DataFrame()
    output_df = pd.DataFrame()

    df['sent_at'] = ['2016-05-01','2016-05-02','2016-05-03','2016-05-04',
                     '2016-06-02','2016-06-03','2016-07-02','2016-07-03',
                     '2016-09-01','2016-09-02','2016-09-03','2016-09-04',
                     '2016-10-01''2016-10-02']

    output_df['sent_at'] =

    df['relationship'] = ['Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex','Ex']

    output_df['relationship'] = ['Ex','Ex','Ex','Ex','Ex','Ex']

    df['to_from'] = [True, False, True, False, True, True, True, True, True,
                     False, True, False, True, True]

    df['positive'] = [0,0,0,0,0,0,0,0,0.5,0.2,0.2,0.3,0.1,0.1]

    df['negative'] = [0,0,0,0,0,0,0,0,0.5,0.9,0.9,0.3,0.1,0.2]

    df['neutral'] = [ 0,0,0,0,0,0,0,0,0.5,0.5,0.2,0.3,0.1,0.1]

    df['compound'] = [0,0,0,0,0,0,0,0,0.5,-0.5,-0.3,0.3,0.1,-0.1]

    df['word_count'] = [20,0,10,2,10,10,0,0,0,0,0,0,0,0]

    output_df['message_count_user'] = [0.5,0.25,0.25,0,0,0]

    output_df['message_count_contact'] = [1,0,0,0,0,0]

    output_df['message_count'] = [0.6,0.2,0.2,0,0,0]

    output_df['word_count'] = [52/72,20/72,0,0,0,0]

    output_df['word_count_user'] = [5/7, 2/7, 0, 0,0,0]

    output_df['word_count_contact'] = [1,0,0,0,0,0]

    output_df['message_count_reciprocity'] = [0.5,0,0,0,0,0]

    output_df['word_count_reciprocity'] = [0.04,0,0,0,0,0]

    output_df['positive'] = [0,0,0,0,0.3,0.1]

    output_df['negative'] = [0,0,0,0,0.65,0.15]

    output_df['neutral'] = [0,0,0,0,0.375,0.1]

    output_df['compound'] = [0,0,0,0,0,0]

    output_df['positive_user'] = [0,0,0,0,0.35,0.1]

    output_df['negative_user'] = [0,0,0,0,0.7,0.15]

    output_df['neutral_user'] = [0,0,0,0,0.35,0.1]

    output_df['compound_user'] = [0,0,0,0,0.1,0]

    output_df['positive_contact'] = [0,0,0,0,0.25,0]

    output_df['negative_contact'] = [0,0,0,0,0.6,0]

    output_df['neutral_contact'] = [0,0,0,0,0.4,0]

    output_df['compound_contact'] = [0,0,0,0,-0.1,0]

    output_df['sentiment_reciprocity'] = [0,0,0,0,0.2,0]

    assert resample_dataframe(df, 'M').equals(output_df)
