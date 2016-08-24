#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clean_df import remove_empty_messages
from clean_df import remove_signatures_and_after
from clean_df import remove_excess_whitespace
from clean_df import remove_urls

import pandas as pd

escape_chars_message = ['\t','\n','\s']

emojis_message = [':)','😀','\xF0\x9F\x98\x81']

non_english_message = ['W Szczebrzeszynie chrząszcz brzmi w trzcinie',
                       'Das ist nicht mein bier']


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
               'Hi Heidi Sent from my Samsung bye',
               'Hi Ignacio Sent from my Sony']

    sig_msg_pass = ['Hi Alex', 'Hi Ben', 'Hi Clara', 'Hi Dawn', 'Hi Elco',
                    'Hi Frances', 'Hi Grzegorz', 'Hi Heidi', 'Hi Ignacio']

    sig_time = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    df = pd.DataFrame({'message': sig_msg, 'time': sig_time})
    df_pass = pd.DataFrame({'message': sig_msg_pass, 'time': sig_time})

    assert remove_signatures_and_after(df).equals(df_pass)


def test_remove_urls():
    url_message = ['I like www.zombo.com/, really I do',
                   'I like www.zombo.com...',
                   'what is your favourite?https://www.google.co.uk/',
                   'I lovehttp://www.google.co.uk/',
                   'does this work http://pandas.pydata.org/pandas-docs/stable/dsintro.html I hope so']

    url_message_pass = ['I like, really I do', 'I like ...',
                        'what is your favourite?',
                        'I love',
                        'does this work I hope so']

    url_time = [1,2,3,4,5]

    df = pd.DataFrame({'message': url_message, 'time': url_time})
    df_pass = pd.DataFrame({'message': url_message_pass, 'time': url_time})

    assert remove_urls(df).equals(df_pass)