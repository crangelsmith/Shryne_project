import sys
import cPickle as pickle

import Shryne.mining.connector as connector
import Shryne.mining.query as query
import Shryne.cleaning.clean_df as clean_df
import Shryne.sentiment_analysis.vader_sentiment_analysis as vsa
import Shryne.analytics.feature_creation as feature_creator
import Shryne.out.

import Shryne.config as config


def main():

    # setup some objects
    db_connection = connector.ConnectDB()
    sentiment_analyser = vsa.SentimentAnalyser()
    querier = query.Query()

    # connect to database
    conn = db_connection.get_connection()

    # run query and get dataframe
    current_query = querier(conn, q_run)
    df = current_query.get_query_dataframe()

    # clean df
    cleaned_df = clean_df.run_cleaning(df)

    # sentiment analysis
    cleaned_df_with_sentiment = sentiment_analyser.run_vader(cleaned_df, 'message')

    # feature generation
    cleaned_df_with_sentiment_and_features = feature_creator.create_features(cleaned_df_with_sentiment)

    # check relationship type, load correct model based on type and run model
    if cleaned_df['relationship'][0] in ['Family', 'Friends', 'General']:
        model = pickle.load(config.not_romantic_model_file_path)
    else:
        model = pickle.load(config.romantic_model_file_path)
    cleaned_df_with_sentiment_and_features['probs'] = model.predict_proba(cleaned_df_with_sentiment_and_features)

    # return json output





if __name__ == "__main__":
    sys.exit(main())


