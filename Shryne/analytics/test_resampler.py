#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from resampler import sentiment_cleaning


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