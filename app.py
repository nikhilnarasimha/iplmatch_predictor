# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:47:04 2020

@author: malat
"""

from flask import Flask , render_template , request

import pickle

app = Flask(__name__)

de = open("team_decoder.pkl", "rb")

team_decoder = pickle.load(de)

de = open("toss_decoder.pkl", "rb")

toss_decoder = pickle.load(de)

model = open("model.pkl", "rb")

model = pickle.load(model)

    
    
@app.route("/", methods=['GET', 'POST'])
def home():
    winner = ""
    if request.method == "POST":
        team1 = str(request.form.get("team1"))
        team2 = str(request.form.get("team2"))
        toss_winner = str(request.form.get("toss_winner"))
        toss_decision = str(request.form.get("toss_decision"))
        team1 = team_decoder.transform([team1])
        team2 = team_decoder.transform([team2])
        toss_winner = team_decoder.transform([toss_winner])
        toss_decision = toss_decoder.transform([toss_decision])
        y = model.predict([[team1[0],team2[0],toss_winner[0],toss_decision[0]]])
        result = team_decoder.inverse_transform([y[0]])
        winner = result[0]
    return render_template("index.html", bmi = winner,)

if __name__ == '__main__':
    app.run(debug=True)