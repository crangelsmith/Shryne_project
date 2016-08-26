from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyser(object):

    def __init__(self):
        self.ss = SentimentIntensityAnalyzer()

    def run_vader(self, df, col):

        positive_list = []
        negative_list = []
        neutral_list = []
        compound_list = []

        for _, row in df.iterrows():
            #TODO decide whether to remove string assigment following set up of df cleaning
            if type(row[col]) is str:
                senti_result = self.ss.polarity_scores(row[col])
            else:
                print 'Message is not a string:', row[col]

            positive_list.append(senti_result['pos'])
            negative_list.append(senti_result['neg'])
            neutral_list.append(senti_result['neu'])
            compound_list.append(senti_result['compound'])

        df['positive'] = positive_list
        df['negative'] = negative_list
        df['neutral'] = neutral_list
        df['compound'] = compound_list

        return df


# if __name__ == "__main__":
#
#
#     df = pd.read_pickle('../data/all_messages_to_from_pickled')
#
#     # run through the standard processing
#     df_no_email = df[df['channel'] != 'gmail']
#     df_no_email = df_no_email[df_no_email['message'] != '        ']
#     b = [len(str(x).split()) for x in df_no_email['message']]
#     df_no_email['word_count'] = b
#
#     # now let look the sentiment analysis, looking at the effect
#     # of using strings in the analysis
#     sentiment_analyser = SentimentAnalyser()
#     updated_df = sentiment_analyser.run_vader(df_no_email, 'message')

