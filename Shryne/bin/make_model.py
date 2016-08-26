import sys
import cPickle as pickle

sys.path.insert(0, '../mining')
sys.path.insert(0, '../cleaning')
sys.path.insert(0, '../sentiment_analysis')
sys.path.insert(0, '../analytics')
sys.path.insert(0, '../modeling')
sys.path.insert(0, '../test')
sys.path.insert(0, '../')

import connector
import query
import clean_df
import vader_sentiment_analysis as vsa
import feature_creation as feature_creator
import create_training_datasets as labeller
import build_model as model_builder
import config

# import Shryne.mining.connector as connector
# import Shrye.mining.query as query
# import Shryne.cleaning.clean_df as clean_df
# import Shryne.sentiment_analysis.vader_sentiment_analysis as vsa
# import Shryne.analytics.feature_creation as feature_creator
# import Shryne.modeling.create_training_datasets as labeller
# import Shryne.modeling.build_model as model_builder
# import Shryne.config as config



def main():
    the_query = """SELECT * FROM all_msgs_tf LIMIT 10000"""

    # setup some objects and connect to the database
    db_connection = connector.ConnectDB()
    sentiment_analyser = vsa.SentimentAnalyser()
    # conn = db_connection.get_connection()
    # querier = query.Query(conn, the_query)


    # run query and get dataframe
    # query found in the config
    try:
        print 'am i here?'
        pickle.load("../data/all_messages.p")
    except:
        # current_query = querier(conn, the_query)
        print 'or here?'
        conn = db_connection.get_connection()
        querier = query.Query(conn, the_query)
        df = querier.get_query_dataframe()
        pickle.dump(df, open('../data/all_messages.p', 'wb'))
        #pickle.dump(df, '../data/all_messages.p')



    # clean df
    cleaned_df = clean_df.run_cleaning(df)

    # sentiment analysis
    try:
        pickle.load("../data/all_messages_with_sentiment.p")
    except:
        cleaned_df_with_sentiment = sentiment_analyser.run_vader(cleaned_df,'message')
        pickle.dump(cleaned_df_with_sentiment, '../data/all_messages_with_sentiment.p')



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


