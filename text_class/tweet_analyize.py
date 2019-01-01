import sqlite3
import json
import time
def get_connection():
    db_path = 'tweetdata.db'
    return sqlite3.connect(db_path)


def get_data():
    connection = get_connection()
    c = connection.cursor()
    c.execute("SELECT * FROM 'user'")

    tweet_data = []
    for row in c:
        user = {
            'name': row[0],
            'text': row[1],
            'id': row[2],
            'nltk': row[3],
            'pol': row[4],
            'subj': row[5],
        }
        tweet_data.append(user)

    connection.close()
    return tweet_data


def get_tb_avg():
    data = get_data()
    pol_avg = []
    subj_avg = []
    for i in range(len(data)):
        pol = data[i]['pol']
        subj = data[i]['subj']
        pol_avg.append(int(pol))
        subj_avg.append(int(subj))
    pol_avg_int = sum(pol_avg) / len(pol_avg)
    subj_avg_int = sum(subj_avg) / len(subj_avg)
    return pol_avg_int, subj_avg_int


def get_nltk_avg():
    data = get_data()
    nltk_avg = []
    for i in range(len(data)):
        nltk = data[i]['nltk']
        if nltk == 'positive':
            nltk_avg.append(1)
        else:
            nltk_avg.append(-1)
    nltk_avg = sum(nltk_avg) / len(nltk_avg)
    if nltk_avg > 0:
        return 'Positive'
    else:
        return 'Negative'
    return nltk_avg

def get_all_ana():
    while True:
        pol, subj = get_tb_avg()
        nltk = get_nltk_avg()
        print(pol, subj, nltk)
        time.sleep(5)

get_all_ana()
