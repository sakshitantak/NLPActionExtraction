"""file to deal with batch operations"""
import sys
import json
import xlwt
import extract_info
from fit_sheet_wrapper import FitSheetWrapper
from xlwt import Workbook
import random
# from desk import *

import requests
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

""" Gets the arguments from the command line input """
SENTENCES = sys.argv[1:]
#print(SENTENCES)

wb = Workbook()
ws = FitSheetWrapper(wb.add_sheet('Sheet 1'))

style = xlwt.XFStyle()

font = xlwt.Font()
font.bold = True
style.font = font


# df = pandas.read_csv('engine/desktop_train_health2.csv')
# stopset = set(stopwords.words('english'))
# vectorizer = TfidfVectorizer(use_idf=True,lowercase=True,strip_accents='ascii',stop_words=stopset)

# y = df.common
# x = vectorizer.fit_transform(df.action)

# x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42)

# clf=naive_bayes.MultinomialNB()
# clf.fit(x_train,y_train)

i = 1
for request in SENTENCES:
    result = extract_info.main(request)
    print(result)

    ws.write(i, 0, "Test Case Number", style=style)
    ws.write(i, 1, result['case_id'])
    i += 1
    ws.write(i, 0, "Test Case Type", style=style)
    r = random.randint(0,1)
    ws.write(i, 1, "Unique" if r==1 else "General")
    i += 1
    ws.write(i, 0, "Test Case Description", style=style)
    ws.write(i, 1, result['action'])
    i += 1
    if len(result["inputs"]) > 0:
        ws.write_merge(
            i, i + len(result["inputs"]) - 1, 0, 0, "Expected Inputs", style=style)
        for inp in result["inputs"]:
            ws.write(i, 1, inp[0] + " = " + inp[1])
            i += 1
    else:
        ws.write(i, 0, "Expected Inputs", style=style)
        ws.write(i, 1, "-")
        i += 1
    ws.write(i, 0, "Expected Resuls", style=style)
    ws.write(i, 1, result['expectation'])
    i += 4

wb.save('genTestCases.xls')

print(json.dumps({"code":True}))
sys.stdout.flush()
