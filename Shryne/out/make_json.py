import json

import Shryne.config as config

def make_json(df, contact_id):
    """Make json file from a dataframe
     and output to the data folder"""

    d = {
        'dates':df.index.strftime('%Y/%m/%d/').tolist(),
        'MessageCount':df['message_count'].tolist(),
        'MessageCountReciprocity':df['message_count_reciprocity'].tolist(),
        'Sentiment':df['compound'].tolist(),
        'SentimentUser':df['compound_user'].tolist(),
        'SentimentContact':df['compound_contact'].tolist(),
        'HealthScore':df['probs'].tolist()
    }

    with open(config.json_path + str(contact_id) + '_json_output.txt', 'wb') as f:
        json.dump(d, f)
