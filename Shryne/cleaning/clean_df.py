import re
import pandas as pd

emoji_dictionary = {'\xe2\x9d\xa4\xef\xb8\x8f': u'<3',
 '\xf0\x9f\x91\xa8': u':3',
 '\xf0\x9f\x92\x94': u'</3',
 '\xf0\x9f\x98\x82': u":')",
 '\xf0\x9f\x98\x83': u':)',
 '\xf0\x9f\x98\x84': u':D',
 '\xf0\x9f\x98\x87': u'o:)',
 '\xf0\x9f\x98\x89': u';)',
 '\xf0\x9f\x98\x8d': u':*',
 '\xf0\x9f\x98\x8e': u'8)',
 '\xf0\x9f\x98\x90': u':|',
 '\xf0\x9f\x98\x92': u':$',
 '\xf0\x9f\x98\x95': u':/',
 '\xf0\x9f\x98\x97': u':*',
 '\xf0\x9f\x98\x98': u':*',
 '\xf0\x9f\x98\x99': u':*',
 '\xf0\x9f\x98\x9a': u':*',
 '\xf0\x9f\x98\x9b': u':p',
 '\xf0\x9f\x98\x9c': u';d',
 '\xf0\x9f\x98\x9d': u'x-p',
 '\xf0\x9f\x98\x9e': u":'(",
 '\xf0\x9f\x98\xa0': u'>:(',
 '\xf0\x9f\x98\xa1': u':@',
 '\xf0\x9f\x98\xa2': u":'(",
 '\xf0\x9f\x98\xa5': u":'(",
 '\xf0\x9f\x98\xa6': u':(',
 '\xf0\x9f\x98\xae': u':o'}

## a dictionary mapping hex representations of emojis to their punctuation
## representations as emoticons. All the emoticons are found in vader's lexicon
## Source for this: an ugly python notebook in the sentiment_analysis folder

def drop_one_sided(df):
    """Drop any rows which are part of a one sided conversation
    i.e. messages only from a contact to a user or vice versa"""

    group = df.groupby(['user_id', 'contact_id'])

    new_df = group.filter(lambda x: len(x['to_from'].unique()) == 2)

    return new_df

def clean_emails(df):
    """Remove Forwarded parts of messages"""


def turn_emoji_to_emoticon(df, dictionary):
    # takes in a df looks for emojis in the 'message' column, in the messages
    # column
    # turns them into punctuation emoticons according to the dictionary provided
    return df.replace({'message': dictionary})


def remove_newlines(df):
    return df['message'].str.replace('\n', ' ')


def remove_carriage_returns(df):
    return df['message'].str.replace('\r', ' ')


def remove_tabs(df):
    return df['message'].str.replace('\t', ' ')
