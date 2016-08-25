import pandas as pd
import numpy as np
import datetime

from feature_creation import _word_count_feature
from feature_creation import _time_response_feature


def test__word_count_feature():

    word_count_test = pd.DataFrame(["This is a test message"], index=[0], columns=['message'])
    word_count_pass = pd.DataFrame({'message': ["This is a test message"],
                                    'word_count': [5]})
    assert _word_count_feature(word_count_test).equals(word_count_pass)


def test__time_response_feature():
    hours_24 = 24*3600

    time_response_test = pd.DataFrame({'sent_at': [datetime.date(2011, 5, 1),
                                                  datetime.date(2011, 5, 2),
                                                  datetime.date(2011, 5, 3),
                                                  datetime.date(2011, 5, 4),
                                                  datetime.date(2011, 5, 5),
                                                  datetime.date(2011, 5, 6)],
                                      'contact_id': [0, 0, 0, 0, 0, 0],
                                      'to_from': [False, True, True, False, True, False]})
    time_response_pass = time_response_test.copy()
    time_response_pass['response_time'] = [np.nan, hours_24, np.nan, hours_24*2, hours_24, hours_24]

    assert _time_response_feature(time_response_test).equals(time_response_pass)
