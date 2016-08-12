import pandas
from highcharts import Highchart

### TO MAKE A TIME SERIES HIGHCHARTS PLOT FOR EVERY FIELD IN A PANDAS DATAFRAME


def main():
   
    df = pandas.read_csv('../data/SELECT_ALL_FROM_all_messages_metadata.csv')
    # setup pandas dataframe. It's not necessary, so replace this with what ever data source you have.

    charts = Highchart() 
    # create highcharts instance
    
    time_field = 'sent_at'
  
    if isinstance(df[time_field].tolist()[0], str):
        df[time_field] = pandas.to_datetime(df[time_field])
    else:
        print("nothing to be done")
        
    # This converts the string in the time field to a datetime, this will probably need changing
    def _sum(x):
        if len(x) == 0: return 0
        else: return sum(x)

    x_day = df[time_field].value_counts().resample('D',how="sum").index.values.tolist()
    y_day = df[time_field].value_counts().resample('D',how=_sum).tolist()
    x_day = [int(i)/1000000 for i in x_day]
    df_day = pandas.DataFrame(list(zip(x_day, y_day)), columns=['date', 'counts'])

    df_day.date = pandas.to_datetime(df_day.date, unit='ms')
    df_day.set_index('date', inplace=True)
    df_month = pandas.DataFrame()
    df_month['x_month'] = df_day.resample('M',how=_sum).index.tolist()
    df_month['y_month'] = df_day.counts.resample('M',how=_sum).tolist()

    # remove time field from either of the headers lists
    options = {'chart': {
        'type': 'scatter',
        'zoomType': 'x'
    }, 'xAxis': {
        'type': 'datetime'
    }, 'credits': {
        'enabled': False
    }, 'title': {'text': str("daily and monthly")},
        'yAxis': {'type': 'float', 'title': {'enabled': True, 'text': 'counts'}}}

    y_day = [int(i) for i in y_day]
    y_month = [int(i) for i in df_month.y_month.tolist()]

    data_day = list(zip(x_day, y_day))
    data_month = list(zip(df_month.x_month.tolist(), y_month))
    charts.set_dict_options(options)
        
    charts.add_data_set(data_day, series_type='area', name="daily")
    charts.add_data_set(data_month, series_type='line', name='monthly')
     
    charts.save_file('time_series')
        
if __name__ == '__main__':
    main()
