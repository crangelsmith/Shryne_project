import sys
import os
import pickle

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import mining.connector as connector
import mining.query as query
import cleaning.clean_df as clean_df
import sentiment_analysis.vader_sentiment_analysis as vsa
import analytics.feature_creation as feature_creator
import modeling.create_training_datasets as labeller
import modeling.build_model as model_builder

import config as config


def main():

    # setup some objects
    db_connection = connector.ConnectDB()

    # connect to database
    conn = db_connection.get_connection()

    sentiment_analyser = vsa.SentimentAnalyser()
    querier = query.Query(conn, config.q_make)

    # run query and get dataframe
    # query found in the config
    try:
        pickle.load("../data/result_10000.p")
    except:
        #current_query = querier(conn, config.q_make)
        df = querier.get_query_dataframe()
        pickle.dump(df, open('../data/result_10000.p', 'wb'))


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


