import numpy as np
import pandas as pd

def drop_one_sided(df):
    """Drop any rows which are part of a one sided conversation
    i.e. messages only from a contact to a user or vice versa"""

    group = df.groupby(['user_id', 'contact_id'])

    new_df = group.filter(lambda x: len(x['to_from'].unique()) == 2)

    return new_df



def create_features(df):

    word_count = []
    You_count = []
    We_count = []
    Us_count = []
    I_count =[]

    for x in df['message']:

        word_count.append(len(str(x).split()))
        I_count.append(count_nouns(str(x),"I"))
        You_count.append(count_nouns(str(x),"you"))
        We_count.append(count_nouns(str(x),"we"))
        Us_count.append(count_nouns(str(x),"us"))

    df['word_count'] = word_count
    df['I_count'] = I_count
    df['You_count'] = You_count
    df['We_count'] = We_count
    df['Us_count'] = Us_count

    return df


def count_nouns(msg,noun):

    list_message = msg.split()

    c = 0
    for i in list_message:
        if i == noun:
            c += 1

    return c

def count_emoji(msg):
    count = 0

    emoticons = set(range(int('1f600', 16), int('1f650', 16)))
    for char in msg:
        if ord(char) in emoticons:
             count += 1
    return count


def time_response(df):
    list_df=[]
    unique_contacts = df['contact_id'].unique()
    for unique_contact in unique_contacts:
        sub_df = df[df['contact_id'] == unique_contact]
        is_user = sub_df["to_from"].iloc[0]
        time = sub_df["sent_at"].iloc[0]
        list_times= []

        for _, row in df.iterrows():
            time_diff = np.nan
            if row["to_from"]!=is_user:
                time_diff = abs((time - row["sent_at"]).seconds)
                if time_diff==0 or time_diff>10800:
                    time_diff = np.nan
                is_user = row["to_from"]
                time = row["sent_at"]
            list_times.append(time_diff)
        sub_df['time_reponse'] = list_times
        list_df.append(sub_df)

    result = pd.concat(list_df)
    return result