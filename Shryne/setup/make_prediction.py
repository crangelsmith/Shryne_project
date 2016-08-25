## Master script to make a dataframe, clean it, run sentiment analysis and 
## train the logistical model.
# Only uses 

import pandas as pd
import pickle

# Querying data, connecting to the database and making a dataframe
import connector
import query

# Sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vader_sentiment_analysis import SentimentAnalyser

# Cleaning data
from clean_df import drop_one_sided, clean_message, remove_newlines, 
remove_carriage_returns, remove_tabs

# For making features
from feature_creation import create_features, time_response
import resampler

# Training the model
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score



###### QUERY ##################

# Query to select all messages from both users and contacts.
# all_msgs_tf is a view which you can see the code for with
# >>> \d+ all_msgs_tf
q = "SELECT * FROM all_msgs_tf;"

dbconnection = connector.ConnectDB()
conn = dbconnection.get_connection()
query = Query(conn, q)
query_list = query.get_query_list()
df = query.get_query_dataframe()

######## CLEAN ##################

# We only want to use Partners and Exs
df = df[df['relationship'] != "General"]
df = df[df['relationship'] != "Family"]
df = df[df['relationship'] != "Friend"]

# Drop one-sided conversations
df = drop_one_sided(df)

# get rid of forwarded emails and signatures such as "sent from iphone"
df = clean_message(df)
df = remove_newlines(df) 
df = remove_carriage_returns(df)
df = remove_tabs(df)


# Make more features to go to the model
df = create_features(df)
df = time_response(df)


########### SENTIMENT ANALYSIS ###############################

sentiment_analyser = SentimentAnalyser()

# result is a dataframe
result = sentiment_analyser.run_vader(df, 'message')

########### RESAMPLING ######################################

# for each contact 
unique_contacts = df['contact_id'].unique()
    
    for unique_contact in unique_contacts:
      
    new_df = resampler.resample_dataframe(sub_df, "M")

    # Making strings to go into the naming of dataframes and charts
    user_id = str(sub_df['user_id'][0])
    contact_id = str(sub_df['contact_id'][0])

    # Drop any rows that are zero
    new_df = new_df[new_df["message_count"] != 0.0]

    # store values for 30% and 50% of rows
    percentage_30 = int(new_df.shape[0]*0.30);

    percentage_50 = int(new_df.shape[0]*0.50);

    # store the top 50% of values in high and lowest 30% in low
    high = new_df.sort_values("message_count", ascending=False)[0:percentage_50]
    low = new_df.sort_values("message_count", ascending=True)[0:percentage_30]

    list_df.append(new_df)
    list_df_high.append(high)
    list_df_low.append(low)
        
# Final dataframes to be used to modelling
result = pandas.concat(list_df)
result_high = pandas.concat(list_df_high)
result_low = pandas.concat(list_df_low)

# Just selecting certain features which are important for the model
df_high = result_high[[
"message_count","compound","word_count","message_count_reciprocity", 
"word_count_reciprocity","response_time","response_time_reciprocity", 
"sentiment_reciprocity"]]

df_low = result_low[[
"message_count","compound","word_count","message_count_reciprocity", 
"word_count_reciprocity","response_time","response_time_reciprocity", 
"sentiment_reciprocity"]]

# Replacing all the nans with 0's
df.fillna(0,inplace = True)
df_high.fillna(0,inplace = True)
df_low.fillna(0,inplace = True)

# Creating labels for high and low message count
df_high['label']=1
df_low['label']=0

# concatenating into one training set
label_data = pd.concat([df_high,df_low])

# Train the model
model = LogisticRegression()
model = model.fit(X_train, y_train)





