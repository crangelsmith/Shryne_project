# based on http://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python

# set flag for processing type

# set the model type to be run
model = 'romantic'  # 'not_romantic'

#set the proessing parameters for resampler
resampler = {'response_time_limit_romantic': 6,  # max time for response in hours
             'response_time_limit_not_romantic': 168,   # max time for response in hours
             }