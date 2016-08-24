#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from resampler import sentiment_cleaning
from resampler import find_ratio


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


    zero_zero_float_test = pd.DataFrame({'message_count_user': [0.0],
                                         'message_count_contact': [0.0]})

    assert find_ratio(zero_zero_float_test, 'message_count') == 0


    zero_zero_int_test = pd.DataFrame({'message_count_user': [0],
                                         'message_count_contact': [0]})

    assert find_ratio(zero_zero_int_test, 'message_count') == 0


    divide_two_equal_floats = pd.DataFrame({'message_count_user': [0.5],
                                            'message_count_contact': [0.5]})

    assert find_ratio(divide_two_equal_floats, 'message_count') == 1

    div_two_floats_bottom = pd.DataFrame({'message_count_user': [0.5],
                                            'message_count_contact': [0.6]})

    assert find_ratio(div_two_floats_bottom, 'message_count') == 0.5/0.6

    div_two_floats_top = pd.DataFrame({'message_count_user': [0.6],
                                            'message_count_contact': [0.5]})

    assert find_ratio(div_two_floats_top, 'message_count') == 0.5/0.6

    div_zero_int = pd.DataFrame({'message_count_user': [0],
                                            'message_count_contact': [20]})
    assert find_ratio(div_zero_int, 'message_count') == 0

    div_int_zero = pd.DataFrame({'message_count_user': [20],
                                            'message_count_contact': [0]})
    assert find_ratio(div_int_zero, 'message_count') == 0

    div_small_int_big_int = pd.DataFrame({'message_count_user': [1],
                                 'message_count_contact': [20]})
    assert find_ratio(div_small_int_big_int, 'message_count') == 0.05

    div_big_int_small_int = pd.DataFrame({'message_count_user': [20],
                                 'message_count_contact': [1]})
    assert find_ratio(div_big_int_small_int, 'message_count') == 0.05

    div_big_float_little_int = pd.DataFrame({'message_count_user': [20.1],
                                 'message_count_contact': [20]})
    assert find_ratio(div_big_float_little_int, 'message_count') == 20/20.1

    div_big_int_little_float = pd.DataFrame({'message_count_user': [20],
                                 'message_count_contact': [20.1]})
    assert find_ratio(div_big_int_little_float, 'message_count') == 20/20.1

    swaps_OK_repeat = pd.DataFrame({'message_count_user': [1, 1, 2, 0, 1, 0],
                                    'message_count_contact': [2, 1, 1, 0, 0,1]})

    assert len(find_ratio(swaps_OK_repeat, 'message_count')) == 6
    assert sorted(find_ratio(swaps_OK_repeat, 'message_count')) == [0,0,0,
                                                                    0.5,0.5,1]


