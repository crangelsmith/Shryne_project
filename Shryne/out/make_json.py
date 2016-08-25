import json

def make_json(df, contact_id):
    """Make json file from a dataframe
     and output to the data folder"""

    d = {
        'dates':df.index.tolist(),
        'MessageCount':df['message_count'].tolist(),
        'MessageCountReciprocity':df['message_count_reciprocity'].tolist(),
        'Sentiment':df['sentiment'].tolist(),
        'SentimentUser':df['sentiment_user'].tolist(),
        'SentimentContact':df['sentiment_contact'].tolist(),
        'HealthScore':df['probs'].tolist()
    }

    with open(contact_id + '_json_output.txt', 'wb') as f:
        json.dumps(d, f)
