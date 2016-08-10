from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

class SentimentAnalyser(object):

    def __init__(self):
        self.ss = SentimentIntensityAnalyzer()

    def run_vader(self, df, col):

        positive_list = []
        negative_list = []
        neutral_list = []
        compound_list = []

        for index, row in df.iterrows():
            #TODO decide whether to remove string assigment following set up of df cleaning
            senti_result = self.ss.polarity_scores(str(row[col]))

            positive_list.append(senti_result['pos'])
            negative_list.append(senti_result['neg'])
            neutral_list.append(senti_result['neu'])
            compound_list.append(senti_result['compound'])

        df['postive'] = pd.Series(positive_list)
        df['negative'] = pd.Series(negative_list)
        df['neutral'] = pd.Series(neutral_list)
        df['compound'] = pd.Series(compound_list)

        return df



if __name__ == "__main__":

    import Shryne.mining.connector as connector
    import Shryne.mining.query as query

    q = "SELECT * FROM feed_items LIMIT 10;"

    dbconnection = connector.ConnectDB()
    conn = dbconnection.get_connection()
    the_query = query.Query(conn, q)
    query_df = the_query.get_query_dataframe()
    sentiment_analyser = SentimentAnalyser()
    result = sentiment_analyser.run_vader(query_df, 'body')
    print result