#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import Shryne.config as config

from resampler import sentiment_cleaning
from resampler import _sum, _average, _average_time

def test_sentiment_cleaning():
    """
    Where neutral = 1 or if +ve, -ve
    and neutral = 0 then replace with nan
    """

    neutral_test = pd.DataFrame({'neutral' : [1,0,1.000001,0.999999,1.0],
                                 'compound' : [1, 1, 1, 1, 1],
                                 'positive' : [1,1,1,1,1],
                                 'negative': [1, 1, 1, 1, 1]})

    neutral_pass = pd.DataFrame({'neutral' : [np.NaN, 0, 1.000001, 0.999999,
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


def test__sum():
    empty_test = []
    empty_pass = 0

    sum_test = [1,2,3,4,5,6,7,8,9,10]
    sum_pass = 55

    nan_test = [np.nan, np.nan, np.nan]
    nan_pass = np.nan

    assert _sum(empty_test).equals(empty_pass)
    assert _sum(sum_test).equals(sum_pass)
    assert _sum(nan_test).equals(nan_pass)


def test__average():
    empty_test = []
    empty_pass = 0

    avg_test = [1,2,3,4,5,6,7,8,9,10]
    avg_pass = 5.5

    nan_test = [np.nan, np.nan, np.nan]
    nan_pass = np.nan

    assert _average(empty_test).equals(empty_pass)
    assert _average(avg_test).equals(avg_pass)
    assert _average(nan_test).equals(nan_pass)


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

    nan_mean_time_limit = [np.nan,2,3,np.nan,np.nan,6,7,np.nan,np.nan,10]
    nan_mean_pass = 6

    assert _average_time(empty_test).equals(empty_pass)
    assert _average_time(greater_than_time_limit).equals(greater_than_time_limit_pass)
    assert _average_time(zero_mean_time_limit).equals(zero_mean_time_limit_pass)
    assert _average_time(less_than_time_limit).equals(less_than_time_limit_pass)
    assert _average_time(nan_mean_time_limit).equals(nan_mean_pass)



