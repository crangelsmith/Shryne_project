import pandas
from highcharts import Highchart
import resampler
import feature_creation
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import Shryne.modeling.create_training_datasets as datasets

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

    #df = pandas.read_csv("../data/result_csv_no_message.csv")
    df = pandas.read_pickle('../data/result_19August')

    # setup pandas dataframe. It's not necessary, so replace this with what ever
    #  data source you have.

    df = clean_df.drop_one_sided(df)
    df = feature_creation.create_features(df)
    df = feature_creation.time_response(df)

    result_romantic = datasets.build_labeled_samples(df, "romantic")
    result_non_romantic = datasets.build_labeled_samples(df, "non_romantic")

    result_romantic.to_pickle("../data/relationship_features_romantic")
    result_non_romantic.to_pickle("../data/relationship_features_non_romantic")



if __name__ == '__main__':
    main()
