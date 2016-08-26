import sys
import cPickle as pickle

import Shryne.mining.connector as connector
import Shryne.mining.query as query
import Shryne.cleaning.clean_df as clean_df
import Shryne.sentiment_analysis.vader_sentiment_analysis as vsa
import Shryne.analytics.feature_creation as feature_creator
import Shryne.modeling.create_training_datasets as labeller
import Shryne.modeling.build_model as model_builder

import Shryne.config as config


def main():

    # setup some objects
    db_connection = connector.ConnectDB()
    sentiment_analyser = vsa.SentimentAnalyser()

    # connect to database
    conn = db_connection.get_connection()

    # run query and get dataframe
    # query found in the config
    try:
        with open('../data/query_df.pickle', 'rb') as f:
            df = pickle.load(f)
    except Exception, e:
        print 'could not load query with error:', e
        df = query.Query(conn, config.q_make).get_query_dataframe()
        with open('../data/query_df.pickle', 'wb') as f:
            pickle.dump(df, f)

    # clean df
    df = clean_df.run_cleaning(df)

    # sentiment analysis
    try:
        with open('../data/sentiment_df.pickle', 'rb') as f:
            df = pickle.load(f)
    except Exception, e:
        print 'could not load sentiment df:', e
        df = sentiment_analyser.run_vader(df, 'message')
        with open('../data/sentiment_df.pickle', 'wb') as f:
            pickle.dump(df, f)

    # feature generation
    df = feature_creator.create_features(df)

    # create datasets
    labelled_df_romantic = labeller.build_labeled_samples(df, 'romantic')
    labelled_df_not_romantic = labeller.build_labeled_samples(df, 'not_romantic')

    # build model
    romatic_model = model_builder.build_model(labelled_df_romantic)
    not_romatic_model = model_builder.build_model(labelled_df_not_romantic)

    # dump models
    with open(config.romantic_model_file_path, 'wb') as f:
        pickle.dump(romatic_model, f)
    with open(config.not_romantic_model_file_path, 'wb') as f:
        pickle.dump(not_romatic_model, f)

if __name__ == "__main__":
    sys.exit(main())


