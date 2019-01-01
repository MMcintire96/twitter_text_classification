import nltk

def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})


pos = []
with open('pos_tweets.txt') as f:
          for i in f:
            pos.append([format_sentence(i), 'positive'])
neg = []
with open('neg_tweets.txt') as f:
          for i in f:
            neg.append([format_sentence(i), 'negative'])

training = pos[:int((.8)*len(pos))] + neg[:int((.8)*len(neg))]
test = pos[int((.8)*len(pos)):] + neg[int((.8)*len(neg)):]

from nltk.classify import NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(training)


def get_nltk_data(text):
    return classifier.classify(format_sentence(text))
