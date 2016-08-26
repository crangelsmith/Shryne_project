### Shryne project

Authors: Camila Rangel Smith, Alexander Green, Daniel Fisher and Sophie Cowie

We built a machine learning model that predicts a relationship health score based on social media comunications such as
email, text, facebook and whatsapp messages.

To build the model we use Shryne data selecting extreme values observed in the relationships contained in the
 database:
- We resample the time-line of each relationship in a monthly basis (this was done to reduce the noise due to the size of the sample).
- We assume that a "good" month of a relationship will show a good volume of communications and high reciprocity in
  the exchange. A "bad" month of the relationship will show a reduced amount of communications.
- Based on the latter point we process each relationship in the database a select its extreme values: the months with
  the top 50% of communication volume and 50% of top reciprocity is labeled as "good". In the other hand,
the months with the bottom 30% of the communication volume are labeled as "bad".
- This is done separately for two models, one for romantic realtionships and one for non-romantic ones.

Once we have our labeled dataset we build our Logistic Regression Model based in the following features:

- Average sentiment of the messages during that month (scores for neutral, positive, negative and compound value).
- Average reciprocity in the sentiment between both sides of the relationship, defined as: |sentiment_user - sentiment_contact|
- Proportion of words sent in that month wrt the whole relationship.
- Average of the word reciprocity during that month. Word reciprocity is the ratio of words sent vs recieved.
- Average of the response time between messages during that month.
- Average of the response time reciprocity during that month. Where reciprocity is the ratio of response time of the user vs the contact.

The model will return a probabily from 0 to 1 of the relationship being from the category "good" (1) or "bad" (0).
In order to have a prediction, the relationship that is evaluated has to have a communication exchange of at least 4
units during that month. Also, the communications have to be from both the user and the contact.

The model needs to be trained regularly (especially if the database grows) and evaluated for each user. For this we have
created two python scripts.

1. **make_model.py**: This script does the model training and consist of the following steps:
    - Connect to the Shryne database
    - Run query to access the relevant data from the database, dumps it into a dataframe.
    - Performs the cleaning of the data: selects relationships with 2-sided communication, clean text for sentiment
     analysis.
    - Run the sentiment analysis to all cleaned messages.
    - Generate the features needed in the model.
    - Creates the datasets needed for the training.
    - Builds two models, one for romantic relationships, and one for non-romantic ones.
    - Dumps this two models into a pickle object to be called later in the evaluation.

2. **run_model.py**: This script evaluates the model in a relationship and consist of the following steps:
    - Connect to the Shryne database
    - Run query to access the relevant data of that particular relationship from the database, dumps it into a dataframe.
    - Performs the cleaning of the data: selects only with 2-sided communications, clean text for sentiment
     analysis.
    - Run the sentiment analysis to all cleaned messages.
    - Generate the features needed in the model.
    - Depending on the relationship type (romantic or non-romantic), loads the train model and evaluates it
    for every month of the relationship.
    - Returns a json object with the results for each month of the relationship in the following format:

        d = {
        'dates':df.index.strftime('%Y/%m/%d/').tolist(),
        'MessageCount':df['message_count'].tolist(),
        'MessageCountReciprocity':df['message_count_reciprocity'].tolist(),
        'Sentiment':df['sentiment'].tolist(),
        'SentimentUser':df['sentiment_user'].tolist(),
        'SentimentContact':df['sentiment_contact'].tolist(),
        'HealthScore':df['probs'].tolist()
    }


The structure of this repo is the following:

- **mining**: classes that conect to the Shryne servers and query the database.
- **cleaning**: all cleaning functions are stored here: cleaning emails, text, one sided relationships, etc.
- **analytics**: here we store functions that create features for the model
- **data**: directory to store datasets that might be used in the processing
- **out**: place that stores the trained model and json output
- **bin**: contains run_model.py and make_model.py scripts to be ran.

Steps to run this code:
-




