import pandas as pd
import numpy as np

def create_features(df):
    df = word_count_feature(df)
    df = time_response(df)
    return df


def word_count_feature(df):
    word_count = []
    for x in df['message']:
        x = str(x)
        split_string = x.split()
        word_count.append(len(split_string))
    df['word_count'] = word_count
    return df


def time_response(df):
    '''
    Vectorised response time calculator.  Algorithm is:

    user  to_from  shift_tf  diff_tf  time  true_time shift_time  time_response
    A     T        ~         T        1     1         ~           ~
    B     F        T         T        2     2         1           1
    B     F        F         F        3     ~         ~           ~
    B     F        F         F        4     ~         ~           ~
    A     T        F         T        5     5         2           3
    B     F        T         T        6     6         5           1

    user: user A or B
    to_from: T is from A or F if from B (i.e. not from A)
    shift_tf: shift to_from down by one row
    diff_tf: True is to_from and shift_tf are difference, False otherwise
    time: a unit of time
    true_time: time where diff_tf is true
    shift_time: shift true_time down by one row
    time_response: true_time - shift_time giving the response time

    :param df:  input dataframe
    :return:  dataframe with response time between users
    '''
    time_field = 'sent_at'
    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pd.to_datetime(df[time_field])

    df['response_time'] = 0

    unique_contacts = df['contact_id'].unique()
    for unique_contact in unique_contacts:

        contact_mask = df['contact_id'] == unique_contact
        contact_df = df[contact_mask]

        # shift to_from and check if they are the same.  If they
        # are not this indicates a change in the communicator
        new_communcation = ~(contact_df['to_from'].shift(1) == contact_df['to_from'])

        # extract the times associated with the change in communicator
        change_times = contact_df['sent_at'][new_communcation]

        # shift the times down one and an the first time to the list
        shifted_change_times = change_times.shift(1)
        # shifted_change_times[0] = df['to_from'][0]

        # compute the time difference
        df['response_time'].where(~contact_mask,
                                  (change_times - shifted_change_times).astype('timedelta64[s]').astype('float'),
                                  inplace=True)

    # in case where the response time is zero (i.e. message sent at the same
    # time which is highly unlikely) set the values to nan
    zero_mask = df['response_time'].values == 0
    df['response_time'].where(~zero_mask, np.nan, inplace=True)

    return df