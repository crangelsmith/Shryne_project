# based on http://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python

# set flag for processing type

# Query for make_model.py
q_make = "SELECT * FROM all_msgs_tf LIMIT 10000"

# Query for run_model.py
# Contact id must be changed to the contact you wish to analyse.
q_run = "SELECT * FROM all_msgs_tf WHERE contact_id = 33008"

# set the model type to be run
model = 'romantic'  # 'not_romantic'

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
romantic_model_file_path = '../data/romantic_model.p'
not_romantic_model_file_path = '../data/not_romantic_model.p'
