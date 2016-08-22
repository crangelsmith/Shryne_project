from collections import Counter


def create_features(df, pet_names, emoji_list):

    word_count = []
    # You_count = []
    # We_count = []
    # Us_count = []
    # I_count = []
    # pet_count = []
    # emoji_count = []

    for x in df['message']:
        x = str(x)
        split_string = x.split()

        word_count.append(len(split_string))
        # I_count.append(x.lower().count(' i '))
        # You_count.append(x.lower().count(" you "))
        # We_count.append(x.lower().count(" we "))
        # Us_count.append(x.lower().count(" us "))
        #
        # # now do the pet name analysis on the string
        # total = 0
        # counts = dict(Counter(split_string).most_common())
        # intersection = filter(set(counts.keys()).__contains__, pet_names)
        # for item in intersection:
        #     total += counts[item]
        # pet_count.append(total)
        #
        # total = 0
        # counts = dict(Counter(split_string).most_common())
        # intersection = filter(set(counts.keys()).__contains__, emoji_list)
        # for item in intersection:
        #     total += counts[item]
        # emoji_count.append(total)

    df['word_count'] = word_count
    # df['I_count'] = I_count
    # df['You_count'] = You_count
    # df['We_count'] = We_count
    # df['Us_count'] = Us_count
    # df['Pet_count'] = pet_count
    # df['emoji_count'] = emoji_count

    return df


# def count_emoji(msg):
#     count = 0
#
#     emoticons = set(range(int('1f600', 16), int('1f650', 16)))
#     for char in msg:
#         if ord(char) in emoticons:
#             count += 1
#     return count


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

    return df


def identify_high_low_quantile(df,column,large=True):

    percentage = df.size/10;

    if large == True:
        new = df.nlargest(percentage,column)
    else:
        new = df.nsmallest(percentage,column)

    return new

