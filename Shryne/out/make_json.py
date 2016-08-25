import json


def make_json:(df)
    """Make json file from a dataframe
     and output to the data folder"""


    d = {
        'contactid':contactid,
        'userid':userid,
        'dates':df_new.index.tolist(),
        'MessageCount':df['message_count'].tolist(),
        'MessageCountReciprocity':df_new['message_count_reciprocity'].tolist(),
        'Sentiment':df_new['sentiment'].tolist(),
        'HealthScore':df_new['output'].tolist()
    }

    return contact_json = json.dumps(d, open(' json_output.txt', 'wb'))