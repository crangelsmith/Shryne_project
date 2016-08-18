
def create_features(df):


    word_count = [len(str(x).split()) for x in df['message']]
    df['word_count'] = word_count

    I_count = [count_nouns(str(x), "I") for x in df['message']]
    df['I_count'] = I_count

    You_count = [count_nouns(str(x), "you") for x in df['message']]
    df['You_count'] = You_count

    We_count = [count_nouns(str(x), "we") for x in df['message']]
    df['We_count'] = We_count

    Us_count = [count_nouns(str(x), "us") for x in df['message']]
    df['Us_count'] = Us_count

    emoji_count = [count_emoji(str(x)) for x in df['message']]
    df['emoji_count'] = emoji_count

    return df


def count_nouns(msg,noun):

    list_message = msg.split()

    c = 0
    for i in list_message:
        if i == noun:
            c += 1

    return c

def count_emoji(msg):
    count = 0

    emoticons = set(range(int('1f600', 16), int('1f650', 16)))
    for char in msg:
        if ord(char) in emoticons:
             count += 1
    return count