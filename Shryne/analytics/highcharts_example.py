import pandas
from highcharts import Highchart
import resampler
import numpy as np

### TO MAKE A TIME SERIES HIGHCHARTS PLOT FOR EVERY FIELD IN A PANDAS DATAFRAME

# This converts the string in the time field to a datetime, this will probably need changing

def highchart_analyser(df, period='M'):

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
        },  {
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

    time_vs_counts = list(zip(df["Time"], df["message_count"]))
    time_vs_pos_sent = list(zip(df["Time"], df["sentiment_mag"]))
    time_vs_word_length = list(zip(df["Time"], df["word_count"]))

    charts.set_dict_options(options)
    charts.add_data_set(time_vs_pos_sent, 'column', name="Positive", yAxis=2, stack='sentiment', color='rgba(178,34,34, .9)')
    charts.add_data_set(time_vs_counts, series_type='spline', yAxis=0, name="Message Count", color='rgba(0,191,255, 1)')
    charts.add_data_set(time_vs_word_length, series_type='spline', yAxis=1, name="Word Count", color='rgba(186,85,211, 1)')

    user_id = str(df['user_id'][0])
    contact_id = str(df['contact_id'][0])

    charts.save_file(user_id+contact_id+'_time_series_'+period)


def main():

    df = pandas.read_csv('../data/textsentiment.csv')

    # setup pandas dataframe. It's not necessary, so replace this with what ever data source you have.

    # TODO split off dataframe by partner type

    df["is_user"]= np.random.randint(2,size=df["contact_id"].size)

    #TODO make sure the analysis starts at 0, i.e. remove [1:]
    unique_contacts = df['contact_id'].unique()[1:]
    for unique_contact in unique_contacts:
        sub_df = df[df['contact_id'] == unique_contact]

        new_df = resampler.resampler_dataframe(sub_df, "M")

        # plot in highchart
        highchart_analyser(new_df)

        # TODO remove this break!
        break



        
if __name__ == '__main__':
    main()
