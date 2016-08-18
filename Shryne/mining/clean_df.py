import re
import pandas as pd

def drop_one_sided(df):
    """Drop any rows which are part of a one sided conversation
    i.e. messages only from a contact to a user or vice versa"""

    group = df.groupby(['user_id', 'contact_id'])

    new_df = group.filter(lambda x: len(x['to_from'].unique()) == 2)

    return new_df

def clean_emails(df):
    """Remove Forwarded parts of messages"""


def