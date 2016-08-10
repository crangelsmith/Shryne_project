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

    import connector
    import query

    q = "SELECT DISTINCT userid, first_name, last_name FROM fakes_names WHERE first_name NOT IN (\'Connor\', \'Danielle\', \'Garrett\',\'Anne\',\'Ethan\',\'Bethany\',\'Cody\');"

    dbconnection = connector.ConnectDB()
    conn = dbconnection.get_connection()
    the_query = query.Query(conn, q)
    query_df = the_query.get_query_dataframe()
    sentiment_analyser = SentimentAnalyser()
    sentiment_analyser.run_vader(query_df, 'body')