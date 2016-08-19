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

        x = str(x)
        split_string = x.split()

        word_count.append(len(split_string))
        I_count.append(x.lower().count(' i '))
        You_count.append(x.lower().count(" you "))
        We_count.append(x.lower().count(" we "))
        Us_count.append(x.lower().count(" us "))

    df['word_count'] = word_count
    df['I_count'] = I_count
    df['You_count'] = You_count
    df['We_count'] = We_count
    df['Us_count'] = Us_count

    return df


def count_emoji(msg):
    count = 0

    emoticons = set(range(int('1f600', 16), int('1f650', 16)))
    for char in msg:
        if ord(char) in emoticons:
             count += 1
    return count


def time_response(df):

    # this cannot work with hangouts as there are no time stamps

    # create a list for holding the times
    result = np.zeros(df['to_from'].size)

    # shift to_from and check if they are the same.  If they
    # are not this indicates a change in the communicator
    new_communcation = ~(df['to_from'].shift(1) == df['to_from'])

    # extract the times associated with the change in communicator
    change_times = df['sent_at'][new_communcation]

    # shift the times down one and an the first time to the list
    shifted_change_times = change_times.shift(1)
    #shifted_change_times[0] = df['to_from'][0]

    # compute the time difference
    time_diff = change_times - shifted_change_times

    result[new_communcation] = time_diff.
    result[~new_communcation] = np.nan

    df['time_response'] = result



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