#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clean_df import remove_empty_messages
from clean_df import remove_signatures_and_after
from clean_df import remove_excess_whitespace
import pandas as pd

escape_chars_message = ['\t','\n','\s']

emojis_message = [':)','😀','\xF0\x9F\x98\x81']

non_english_message = ['W Szczebrzeszynie chrząszcz brzmi w trzcinie',
                       'Das ist nicht mein bier']

url_message = ['www.zombo.com/', 'www.zombo.com', 'https://www.google.co.uk/',
               'http://www.google.co.uk/',
               'http://pandas.pydata.org/pandas-docs/stable/dsintro.html']


def test_remove_empty_messages():
    null_message = ['a', None, '', ' ', '   ', None]  # penultimate is a tab
    null_time = [None, 2, 3, 'a', 'b', None]
    df = pd.DataFrame({'message': null_message, 'time': null_time})

    assert remove_empty_messages(df).shape == (4, 2)
    assert remove_empty_messages(df)['message'][0] == 'a'
    assert remove_empty_messages(df)['time'][0] == None


def test_remove_excess_whitespace():
    white_msg = [' a ', ' b c ', ' d    e   ','\n\t\rf\n\r\t', 'a       a',
                 'c\t\r\n"\t\n\rd', '" asdf "']
    white_msg_pass = ['a','b c', 'd e','f','a a','c " d','" asdf "']

    white_msg_time = [1, 2, 3, 4, 5, 6, 7]

    df = pd.DataFrame({'message': white_msg, 'time': white_msg_time})
    df_pass = pd.DataFrame({'message': white_msg_pass, 'time': white_msg_time})

    assert remove_excess_whitespace(df).equals(df_pass)


def test_remove_signatures_and_after():

    sig_msg = ['Hi Alex', 'Hi Ben Sent from my iPhone asdf',
               'Hi Clara Begin forwarded message Bye Alex',
               'Hi Dawn \n--\n bye', 'Hi Elco Forwarded message bye',
               'Hi Frances Sent from my iPad bye',
               'Hi Grzegorz Sent from my Windows Phone bye',
               'Hi Heidi Sent from my Samsung bye']

    sig_msg_pass = ['Hi Alex', 'Hi Ben', 'Hi Clara', 'Hi Dawn', 'Hi Elco',
                    'Hi Frances', 'Hi Grzegorz', 'Hi Heidi']

    sig_time = [1, 2, 3, 4, 5, 6, 7, 8]

    df = pd.DataFrame({'message': sig_msg, 'time': sig_time})
    df_pass = pd.DataFrame({'message': sig_msg_pass, 'time': sig_time})

    assert remove_signatures_and_after(df).equals(df_pass)