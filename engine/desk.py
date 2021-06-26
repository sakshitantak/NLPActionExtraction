import requests
import sys
import pandas as pd
import numpy as np
import nltk
import json
import csv
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes
from sklearn.metrics import roc_auc_score
import pandas 
df = pandas.read_csv('desktop_train_health2.csv')

stopset = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(use_idf=True,lowercase=True,strip_accents='ascii',stop_words=stopset)

y = df.common
x = vectorizer.fit_transform(df.action)

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42)

clf=naive_bayes.MultinomialNB()
clf.fit(x_train,y_train)

def main2():
    df = pandas.read_csv('desktop_health_test.csv',usecols=['expectation'])
    next(df.iterrows())
    label2 = []
    for c in df.iterrows():
        #print(c[1])
        review_vector = vectorizer.transform(c[1])
        if clf.predict(review_vector) == 0:
            common= "UNIQUE"
        else:
            common = "GENERIC"
        label2.append(common)
    d_f = pd.read_csv('desktop_health_test.csv')
    d_f['Label'] = label2
    d_f.to_csv('desktop_health_test2.csv')
    with open("desktop_health_test2.csv", newline = "") as file:
        l=[]
        reader = csv.reader(file)
        for col in reader:
            l.append(' '.join(col))
        return l 
if __name__ == '__main__':
    """ Gets the first argument from the command line input """
    FIN_RES = main2()
    print(json.dumps(FIN_RES))
    sys.stdout.flush()