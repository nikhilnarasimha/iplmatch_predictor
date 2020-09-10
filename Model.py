# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 19:58:27 2020

"""

# Modules import
import pandas as pd

import pickle

da = pd.read_csv("data.csv")

#label encoding

de = open("team_decoder.pkl", "rb")

team_decoder = pickle.load(de)

df["winner"] = team_decoder.transform(df["winner"])

de = open("toss_decoder.pkl", "rb")

toss_decoder = pickle.load(de)

df["toss_decision"] = toss_decoder.transform(df["toss_decision"])

team_decoder.inverse_transform([2])

x = df.drop(columns = ["winner"])
y = df["winner"]


from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

model = Pipeline([("ht", OneHotEncoder()),("clf", RandomForestClassifier(n_estimators = 120, max_depth = 50))])

model.fit(x,y)

a = model.predict([[0,2,2,1]])


saver = open("model.pkl", "wb")
pickle.dump(model, saver)
saver.close()




