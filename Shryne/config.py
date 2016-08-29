# based on http://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python

# set flag for processing type

# Query for make_model.py
q_make = "SELECT * FROM all_msgs_tf"

# Query for run_model.py
# Contact id must be changed to the contact you wish to analyse.
q_run = "SELECT * FROM all_msgs_tf WHERE contact_id = "

#set the proessing parameters for resampler
resampler = {'response_time_limit_romantic': 6,  # max time for response in hours
             'response_time_limit_not_romantic': 168,   # max time for response in hours
            'period': 'M', # period in reampler set to months. It can be days or weeks.
             }

extremes_sample = {'top': 0.5,  # choose the top 50 %
             'bottom': 0.3,  # choose the bottom 30%
                   }
predictors =["neutral","negative","positive","compound","message_count_reciprocity",
             "word_count","word_count_reciprocity","response_time","response_time_reciprocity",
             "sentiment_reciprocity"]


robust_model = {'mean':0.65, 'std':0.1}

# file paths
models_file_path = '/home/dan/S2DS/test/model'
json_path = '/home/dan/S2DS/test/outputs'
