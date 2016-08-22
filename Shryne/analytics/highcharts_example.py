import pandas
from highcharts import Highchart
import resampler
import feature_creation
import sys
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.insert(0, '../cleaning')
import cPickle as pickle
import clean_df

### TO MAKE A TIME SERIES HIGHCHARTS PLOT FOR EVERY FIELD IN A PANDAS DATAFRAME

# This converts the string in the time field to a datetime, this will probably need changing

def highchart_analyser(df, period='M', name=""):

    charts = Highchart()
    # create highcharts instance

    # remove time field from either of the headers lists
    options = {
        'chart': {
            'zoomType': 'x'
        },
        'title': {
            'text': 'Shryne User/Contact Statistics at Resolution: ' + period
        },
        'xAxis': {
            'type': 'datetime',
            'crosshair': True
        }, 'credits': {
            'enabled': False
        },
        'yAxis': [{
            'gridLineWidth': 0,
            'title': {
                'text': 'Number of Messages',
                'style': {
                    'color': 'Highcharts.getOptions().colors[1]'
                }
            },
            'labels': {
                'format': '{value}',
                'style': {
                    'color': 'Highcharts.getOptions().colors[1]'
                }
            }
        }, {

                'gridLineWidth': 0,
                'title': {
                    'text': 'Reciprocity',
                    'style': {
                        'color': 'Highcharts.getOptions().colors[1]'
                    }
                },
                'labels': {
                    'format': '{value}',
                    'style': {
                        'color': 'Highcharts.getOptions().colors[1]'
                    }
                },
                'opposite': True
            },

            {

            'gridLineWidth': 0,
            'title': {
                'text': 'Number of Words',
                'style': {
                    'color': 'Highcharts.getOptions().colors[1]'
                }
            },
            'labels': {
                'format': '{value}',
                'style': {
                    'color': 'Highcharts.getOptions().colors[1]'
                }
            },
            'opposite': True
        },

            {
            'reversed': True,
            'gridLineWidth': 0,
            'title': {
                'enabled': False
                },
            'labels': {
                'enabled': False
            },
            'opposite': True
        }],
        'tooltip': {
            'shared': True,
        },
        'legend': {
            'layout': 'vertical',
            'align': 'left',
            'x': 80,
            'verticalAlign': 'top',
            'y': 55,
            'floating': True,
            'backgroundColor': "(Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'"
        }
    }
    x = df["sent_at"].index.values.tolist()
    x = [int(i)/1000000 for i in x]


    time_vs_counts = list(zip(x, df["message_count"]))
    time_vs_pos_sent = list(zip(x, df["compound"]))
    time_vs_word_length = list(zip(x, df["response_time"]))

    time_vs_message_reciprocity = list(zip(x, df["message_count_reciprocity"]))
    time_vs_word_length_reciprocity = list(zip(x, df["response_time_reciprocity"]))


    charts.set_dict_options(options)
    charts.add_data_set(time_vs_pos_sent, 'column', name="sentiment", yAxis=2, stack='sentiment', color='yellow')

    charts.add_data_set(time_vs_counts, series_type='spline', yAxis=0, name="Message Count", color='rgba(0,191,255, 1)')

    charts.add_data_set(time_vs_word_length, series_type='spline', yAxis=2, name="Response time", color='rgba(186,85,211, 1)')

    charts.add_data_set(time_vs_message_reciprocity, series_type='spline', yAxis=1, name="Message Count reciprocity",
                        color='red')
    charts.add_data_set(time_vs_word_length_reciprocity, series_type='spline', yAxis=1, name="response_time_reciprocity",
                        color='black')




    charts.save_file('plot/_time_series_'+period+str(name))


def main():

    df = pickle.load(open("../data/result", "rb"))
    #df = pandas.read_pickle('../data/result_19August')

    # setup pandas dataframe. It's not necessary, so replace this with what ever
    #  data source you have.

    df = df[df['relationship'] != "General"]
    df = df[df['relationship'] != "Family"]
    df = df[df['relationship'] != "Friend"]


    df = clean_df.drop_one_sided(df)
    
    pet_names = pandas.read_csv('pet_names_short.txt', delimiter='\n')
    emoji_list = pickle.load(open("emoji_list.p", "rb"))
    df = feature_creation.create_features(df)
    df = feature_creation.time_response(df)




    list_df =[]
    list_df_high =[]
    list_df_low =[]

    list_df_high_reciprocity = []
    list_df_low_reciprocity = []

    unique_contacts = df['contact_id'].unique()
    for unique_contact in unique_contacts:
        sub_df = df[df['contact_id'] == unique_contact]

        new_df = resampler.resample_dataframe(sub_df, "M")

        user_id = str(sub_df['user_id'][0])
        contact_id = str(sub_df['contact_id'][0])


        new_df = new_df[new_df["message_count"]!=0.0]

        percentage = int(new_df.shape[0]*0.30);

        high =new_df.sort_values("message_count", ascending=False)[0:percentage]
        low =new_df.sort_values("message_count", ascending=True)[0:percentage]

        percentage_reciprocity = int(high.shape[0]*0.50)

        high_reciprocity = high.sort_values("message_count_reciprocity", ascending=False)[0:percentage_reciprocity]
        low_reciprocity = low.sort_values("message_count_reciprocity", ascending=False)[0:percentage_reciprocity]



        # plot in highchart
        new_df.to_csv("../data/user_df/data_frame_"+user_id+"_"+contact_id)

        #highchart_analyser(new_df,"D",user_id+"_"+contact_id)
        print("appending dataframe for relationship "+user_id+"_"+contact_id)
        list_df.append(new_df)
        list_df_high.append(high)
        list_df_low.append(low)
        list_df_high_reciprocity.append(high_reciprocity)
        list_df_low_reciprocity.append(low_reciprocity)

    result = pandas.concat(list_df)
    result_high = pandas.concat(list_df_high)
    result_low = pandas.concat(list_df_low)
    result_high_reciprocity = pandas.concat(list_df_high_reciprocity)
    result_low_reciprocity = pandas.concat(list_df_low_reciprocity)

    result.to_pickle("../data/relationship_features_forclustering_M.pandas_df")
    result_high.to_pickle("../data/relationship_features_high")
    result_low.to_pickle("../data/relationship_features_low")

    result_low_reciprocity.to_pickle("../data/relationship_features_low_reciprocity")
    result_high_reciprocity.to_pickle("../data/relationship_features_high_reciprocity")

if __name__ == '__main__':
    main()
