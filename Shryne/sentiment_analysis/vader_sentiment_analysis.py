from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyser(object):

    def __init__(self):
        self.ss = SentimentIntensityAnalyzer()

    def run_vader(self, df, col):

        senti_result = self.ss(df[col])
        df['positive'] = senti_result['pos']
        df['negative'] = senti_result['pos']
        df['neutral'] = senti_result['neu']
        df['compound'] = senti_result['compound']

        return df



if __name__ == "__main__":

    import Shryne.mining.connector as connector
    import Shryne.mining.query as query

    q = "SELECT * FROM feed_items limit 10"

    dbconnection = connector.ConnectDB()
    conn = dbconnection.get_connection()
    the_query = query.Query(conn, q)
    query_df = the_query.get_query_dataframe()
    sentiment_analyser = SentimentAnalyser()
    sentiment_analyser.run_vader(query_df, 'body')