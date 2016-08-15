import vader_sentiment_analysis as vsa
import pandas as pd


if __name__ == "__main__":

    sentiment_analyser = vsa.SentimentAnalyser()

    df = pd.read_csv("../data/all_messages_no_gmail_tf_wc_sentiment.csv")

    for i, row in df.iterrows():

        print row['negative'], row['neutral'], row['positive'], row['compound']
        print sentiment_analyser.ss.polarity_scores(row['message'])
        print row['message']
        print ''

