import pandas
from highcharts import Highchart

### TO MAKE A TIME SERIES HIGHCHARTS PLOT FOR EVERY FIELD IN A PANDAS DATAFRAME

# This converts the string in the time field to a datetime, this will probably need changing
def _sum(x):
    if len(x) == 0:
        return 0
    else:
        return sum(x)


def _average(x):
    if len(x) == 0:
        return 0
    else:
        return sum(x)/len(x)


def highchart_analyser(df, period='D'):

    charts = Highchart() 
    # create highcharts instance

    time_field = 'sent_at'

    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pandas.to_datetime(df[time_field])
    else:
        print("nothing to be done")

    # first set up the time axis analysis for either month or day
    x = df[time_field].value_counts().resample('D',how=_sum).index.values.tolist()
    x = [int(i)/1000000 for i in x]

    # communication count
    y_count = df[time_field].value_counts().resample(period, how=_sum).tolist()

    # mean sentiments
    df.set_index(time_field, inplace=True)
    y_pos = df["positive"].resample(period, how=_average).tolist()
    y_neg = df["negative"].resample(period, how=_average).tolist()
    y_neu = df["neutral"].resample(period, how=_average).tolist()

    # total length
    y_word_count = df["word_count"].resample(period, how=_sum).tolist()

    if period == 'M':
        df_day = pandas.DataFrame(list(zip(x, y_count, y_pos, y_neg, y_neu, y_word_count)),
                                  columns=['date', 'counts', 'positive',
                                           'negative', 'neutral', 'word_count'])
        df_day.date = pandas.to_datetime(df_day.date, unit='ms')
        df_day.set_index('date', inplace=True)
        x = df_day.resample('M', how=_sum).index.tolist()
        y_count = df_day.counts.resample('M', how=_sum).tolist()
        y_pos = df_day["positive"].resample(period, how=_average).tolist()
        y_neg = df_day["negative"].resample(period, how=_average).tolist()
        y_neu = df_day["neutral"].resample(period, how=_average).tolist()
        y_word_count = df_day["word_count"].resample(period, how=_sum).tolist()

    # remove time field from either of the headers lists
    options = {'chart': {
        'type': 'scatter',
        'zoomType': 'x'
    }, 'xAxis': {
        'type': 'datetime'
    }, 'credits': {
        'enabled': False
    }, 'title': {'text': str("daily and monthly")},
        'yAxis': [{
            'labels': {
                'format': '{value}',
            'style': {
                'color': 'Highcharts.getOptions().colors[2]'
            }
        },
        'title': {
            'text': 'Number of Words',
            'style': {
                'color': 'Highcharts.getOptions().colors[2]'
            }
        },
        'opposite': True

    }, {
        'gridLineWidth': 0,
        'title': {
            'text': 'Number of Messages',
            'style': {
                'color': 'Highcharts.getOptions().colors[0]'
            }
        },
        'labels': {
            'format': '{value}',
            'style': {
                'color': 'Highcharts.getOptions().colors[0]'
            }
        }

    }, {
        'gridLineWidth': 0,
        'title': {
            'text': 'Sentiment',
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
    }]}


    time_vs_counts = list(zip(x, y_count))
    time_vs_pos_sent = list(zip(x, y_pos))
    time_vs_neu_sent = list(zip(x, y_neu))
    time_vs_neg_sent = list(zip(x, y_neg))
    time_vs_word_length = list(zip(x, y_word_count))

    charts.set_dict_options(options)
    charts.add_data_set(time_vs_counts, series_type='line', name="Message Count")
    charts.add_data_set(time_vs_pos_sent, series_type='bar', name="Positive", stack='sentiment')
    charts.add_data_set(time_vs_neu_sent, series_type='bar', name="Neutral", stack='sentiment')
    charts.add_data_set(time_vs_neg_sent, series_type='bar', name="Negative", stack='sentiment')
    charts.add_data_set(time_vs_word_length, series_type='line', name="Word Count")

    user_id = str(df['user_id'][0])
    contact_id = str(df['contact_id'][0])

    charts.save_file(user_id+contact_id+'_time_series_'+period)


def main():

    df = pandas.read_csv('../data/textsentiment.csv')
    # setup pandas dataframe. It's not necessary, so replace this with what ever data source you have.

    df['word_count'] = 0

    # TODO split off dataframe by partner type

    unique_contacts = df['contact_id'].unique()
    for unique_contact in unique_contacts:
        sub_df = df[df['contact_id'] == unique_contact]

        # plot in highchart
        highchart_analyser(sub_df, period='M')


        
if __name__ == '__main__':
    main()
