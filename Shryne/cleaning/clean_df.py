import re
import pandas as pd


## a dictionary mapping hex representations of emojis to their punctuation
## representations as emoticons. All the emoticons are found in vader's lexicon
## Source for this: an ugly python notebook in the sentiment_analysis folder

def drop_one_sided(df):
    """Drop any rows which are part of a one sided conversation
    i.e. messages only from a contact to a user or vice versa"""

    group = df.groupby(['user_id', 'contact_id'])

    df = group.filter(lambda x: len(x['to_from'].unique()) == 2)

    return df


def remove_empty_messages(df):
    """
    :param df - a pandas dataframe with a column containing a string named
    message and columns of metadata
    :return df - a pandas dataframe with no rows containing messages with
    the type 'none' or 'nan':
    """
    df = df[df['message'].notnull()]
    df = df.reset_index(drop=True)
    return df


def remove_signatures_and_after(df):
    """
    # Get rid of anything after these strings.
    :param df - a pandas dataframe with a column containing a string named
    message and columns of metadata:
    :return the same df but with all messages cleaned of email signatures
    that indicate the start of forwarded messages:
    """
    sep = ['\n--\n', 'Begin forwarded message', 'Forwarded message',
           '------', 'Sent from my iPhone', 'Sent from my iPad',
           'Sent from my Windows Phone', 'Sent from my Samsung',
           'Sent from my Sony']

    for s in sep:
        df['message'] = df['message'].apply(lambda x: x.split(s, 1)[0])

    df = remove_excess_whitespace(df)

    return df


def remove_excess_whitespace(df):
    """
    :param df - a dataframe with a series named 'message' containing strings:
    :return: df - as above but the strings have leading, trailing and excess
    whitespace removed
    """
    df['message'] = df['message'].str.replace('[\s]+', ' ', case=False,
                                              flags=re.MULTILINE)
    df['message'] = df['message'].str.strip()

    return df


def remove_urls(df):
    """
    Takes a dataframe with a Series named 'message' consisting of strings and
    returns the same dataframe but with the message stripped of urls
    :param df:
    :return df:
    """
    subs = ["On\s[A-Z][a-z]{2}\s[0-9]{1,3}[\s\S]*",
            r'https?:\/\/[\S]*[\s\n\r]+', r'www\.[\S]*[\s\n\r]+',
            r'https?:\/\/[\S]*$', r'www\.[\S]*$']
    for s in subs:
        df['message'] = df['message'].str.replace(s, ' ', case=False,
                                                  flags=re.MULTILINE)

    df = remove_excess_whitespace(df)

    return df


def replace_emojis(df):
    """
    Takes a dataframe with a Series named 'message' consisting of strings and
    returns the same dataframe but with the emojis converted from their
    unicode codepoints to corresponding punctuation emoticons
    :param df:
    :return:
    """
    emoji_dictionary = {'\xe2\x9d\xa4\xef\xb8\x8f': str(u'<3'),
                        '\xf0\x9f\x91\xa8': str(u':3'),
                        '\xf0\x9f\x92\x94': str(u'</3'),
                        '\xf0\x9f\x98\x82': str(u":')"),
                        '\xf0\x9f\x98\x83': str(u':)'),
                        '\xf0\x9f\x98\x84': str(u':D'),
                        '\xf0\x9f\x98\x87': str(u'o:)'),
                        '\xf0\x9f\x98\x89': str(u';)'),
                        '\xf0\x9f\x98\x8d': str(u':*'),
                        '\xf0\x9f\x98\x8e': str(u'8)'),
                        '\xf0\x9f\x98\x90': str(u':|'),
                        '\xf0\x9f\x98\x92': str(u':$'),
                        '\xf0\x9f\x98\x95': str(u':/'),
                        '\xf0\x9f\x98\x97': str(u':*'),
                        '\xf0\x9f\x98\x98': str(u':*'),
                        '\xf0\x9f\x98\x99': str(u':*'),
                        '\xf0\x9f\x98\x9a': str(u':*'),
                        '\xf0\x9f\x98\x9b': str(u':p'),
                        '\xf0\x9f\x98\x9c': str(u';d'),
                        '\xf0\x9f\x98\x9d': str(u'x-p'),
                        '\xf0\x9f\x98\x9e': str(u":'("),
                        '\xf0\x9f\x98\xa0': str(u'>:('),
                        '\xf0\x9f\x98\xa1': str(u':@'),
                        '\xf0\x9f\x98\xa2': str(u":'("),
                        '\xf0\x9f\x98\xa5': str(u":'("),
                        '\xf0\x9f\x98\xa6': str(u':('),
                        '\xf0\x9f\x98\xae': str(u':o')}

    df['message'] = df['message'].replace(emoji_dictionary)

    return df


def run_cleaning(df):
    df = drop_one_sided(df)
    df = remove_empty_messages(df)
    df = remove_signatures_and_after(df)
    df = remove_urls(df)
    df = replace_emojis(df)
    df = remove_excess_whitespace(df)

    return df
