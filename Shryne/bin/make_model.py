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
    querier = query.Query()

    # connect to database
    conn = db_connection.get_connection()

    # run query and get dataframe
    # query found in the config
    try:
        pickle.load("")
    except:
        current_query = querier(conn, q_make)
        df = current_query.get_query_dataframe()
        pickle.dump(df, '')


    # clean df
    cleaned_df = clean_df.run_cleaning(df)

    # sentiment analysis
    cleaned_df_with_sentiment = sentiment_analyser.run_vader(cleaned_df, 'message')

    # feature generation
    cleaned_df_with_sentiment_and_features = feature_creator.create_features(cleaned_df_with_sentiment)

    # create datasets
    labelled_df_romantic = labeller.build_labeled_samples(cleaned_df_with_sentiment_and_features, 'romantic')
    labelled_df_not_romantic = labeller.build_labeled_samples(cleaned_df_with_sentiment_and_features, 'not_romantic')

    # build model
    romatic_model = model_builder.build_model(labelled_df_romantic)
    not_romatic_model = model_builder.build_model(labelled_df_not_romantic)

    # dump models
    pickle.dump(romatic_model, config.romantic_model_file_path)
    pickle.dump(not_romatic_model, config.not_romantic_model_file_path)

if __name__ == "__main__":
    sys.exit(main())


