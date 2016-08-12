from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import math

import matplotlib.pyplot as plt

class SentimentAnalyser(object):

    def __init__(self):
        self.ss = SentimentIntensityAnalyzer()

    def run_vader(self, df, col):

        positive_list = []
        negative_list = []
        neutral_list = []
        compound_list = []

        for index, row in df.iterrows():
            #TODO decide whether to remove string assigment following set up of df cleaning
            senti_result = self.ss.polarity_scores(str(row[col]))


            positive_list.append(senti_result['pos'])
            negative_list.append(senti_result['neg'])
            neutral_list.append(senti_result['neu'])
            compound_list.append(senti_result['compound'])

        df['positive'] = pd.Series(positive_list)
        df['negative'] = pd.Series(negative_list)
        df['neutral'] = pd.Series(neutral_list)
        df['compound'] = pd.Series(compound_list)

        return df


if __name__ == "__main__":

    import Shryne.mining.connector as connector
    import Shryne.mining.query as query

    q = """SELECT *
           FROM feed_items
           JOIN contacts
           ON feed_items.from_id = contacts.id
           JOIN contact_types
           ON contacts.contact_type_id=contact_type_id
           WHERE contact_types.id=1 LIMIT 1000;"""

    dbconnection = connector.ConnectDB()
    conn = dbconnection.get_connection()
    the_query = query.Query(conn, q)
    query_df = the_query.get_query_dataframe()
    query_df.dropna()
    sentiment_analyser = SentimentAnalyser()
    result = sentiment_analyser.run_vader(query_df, 'body')
    print result

    import matplotlib.pyplot as plt

    positive = list(result["positive"])
    negative = list(result["negative"])
    neutral = list(result["neutral"])
    compound = list(abs(result["compound"]))

    size=(len(positive)/100)


    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']

    params = {'figure.facecolor': 'white',
              'figure.subplot.bottom': 0.0,
              'font.size': 16,
              'legend.fontsize': 16,
              'legend.borderpad': 0.2,
              'legend.labelspacing': 0.2,
              'legend.handlelength': 1.5,
              'legend.handletextpad': 0.4,
              'legend.borderaxespad': 0.2,
              'lines.markeredgewidth': 2.0,
              'lines.linewidth': 2.0,
              'axes.prop_cycle': plt.cycler('color', colors)}
    plt.rcParams.update(params)

    fig, ax = plt.subplots(4)
    ax[0].hist(positive , size, label='Positive', histtype='bar')
    ax[0].set_xlim([0.1, 1])
    ax[0].set_ylabel("entries")
    ax[0].set_xlabel("score")
    ax[0].legend(loc='upper right')
    ax[1].hist(negative, size,label='Negative', histtype='bar')
    ax[1].set_xlim([0.1, 1])
    ax[1].set_ylabel("entries")
    ax[1].set_xlabel("score")
    ax[1].legend(loc='upper right')
    ax[2].hist(neutral,size, label='Neutral', histtype='bar')
    ax[2].set_xlim([0, 0.9])
    ax[2].set_ylabel("entries")
    ax[2].set_xlabel("score")
    ax[2].legend(loc='upper right')
    ax[3].hist(compound, size,label='Compound', histtype='bar')
    ax[3].set_xlim([0.1, 1])
    ax[3].set_ylabel("entries")
    ax[3].set_xlabel("score")
    ax[3].legend(loc='upper right')
    #fig.tight_layout()
    fig.savefig('../out/score_distributions.png')
    #plt.show()