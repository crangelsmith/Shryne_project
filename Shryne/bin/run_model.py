import sys
import cPickle as pickle

import Shryne.mining.connector as connector
import Shryne.mining.query as query
import Shryne.cleaning.clean_df as clean_df
import Shryne.sentiment_analysis.vader_sentiment_analysis as vsa
import Shryne.analytics.feature_creation as feature_creator
import Shryne.out.make_json as js

import Shryne.config as config


def main():

    # setup some objects
    db_connection = connector.ConnectDB()
    sentiment_analyser = vsa.SentimentAnalyser()

    # connect to database
    conn = db_connection.get_connection()

    # run query and get dataframe
    df = query.Query(conn, config.q_run).get_query_dataframe()

    # clean df
    cleaned_df = clean_df.run_cleaning(df)

    # sentiment analysis
    cleaned_df_with_sentiment = sentiment_analyser.run_vader(cleaned_df, 'message')

    # feature generation
    cleaned_df_with_sentiment_and_features = feature_creator.create_features(cleaned_df_with_sentiment)

    # check relationship type, load correct model based on type and run model
    if cleaned_df['relationship'][0] in ['Family', 'Friends', 'General']:
        with open(config.not_romantic_model_file_path, 'rb') as f:
            model = pickle.load(f)
    else:
        with open(config.romantic_model_file_path, 'rb') as f:
            model = pickle.load(f)

    # drop the nans and run model
    cleaned_df_with_sentiment_and_features.dropna(inplace=True)
    cleaned_df_with_sentiment_and_features['probs'] = model.predict_proba(cleaned_df_with_sentiment_and_features)

    # return json output

    js.make_json(cleaned_df_with_sentiment_and_features,33008)





if __name__ == "__main__":
    sys.exit(main())


