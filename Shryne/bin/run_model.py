import sys
import cPickle as pickle

import Shryne.mining.connector as connector
import Shryne.mining.query as query
import Shryne.cleaning.clean_df as clean_df
import Shryne.sentiment_analysis.vader_sentiment_analysis as vsa
import Shryne.analytics.feature_creation as feature_creator
import Shryne.out.make_json as js
import Shryne.analytics.resampler as resampler
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
    df = clean_df.run_cleaning(df)

    # sentiment analysis
    df = sentiment_analyser.run_vader(df, 'message')

    # check relationship type, load correct model based on type and run model
    relationship = df['relationship'][0]

    # feature generation
    df = feature_creator.create_features(df)

    df = resampler.resample_dataframe(df, config.resampler['period'])

    # check relationship type, load correct model based on type and run model
    if relationship in ['Family', 'Friends', 'General']:
        with open(config.not_romantic_model_file_path, 'rb') as f:
            model = pickle.load(f)
    else:
        with open(config.romantic_model_file_path, 'rb') as f:
            model = pickle.load(f)

    df = df[config.predictors]
    df.dropna(inplace=True)
    df['probs'] = model.predict_proba(df)

    # return json output

    js.make_json(df,33008)





if __name__ == "__main__":
    sys.exit(main())


