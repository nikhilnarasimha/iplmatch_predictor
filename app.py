# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:47:04 2020

@author: malat
"""

from flask import Flask , render_template , request

import pickle

import pymysql

app = Flask(__name__)

de = open("team_decoder.pkl", "rb")

team_decoder = pickle.load(de)

de = open("toss_decoder.pkl", "rb")

toss_decoder = pickle.load(de)

model = open("model.pkl", "rb")

model = pickle.load(model)


def insert(name_of_person,team1, team2, toss_winner,toss_decision,winner):
    conn = pymysql.connect(host='database2.cvz9y3wumtvk.us-east-2.rds.amazonaws.com',port=int(3306),user="admin",passwd="akhil12345",db="system",charset='utf8mb4')
    cur = conn.cursor()
    sql = "INSERT INTO ipl_match_predict (name_of_person,team1, team2, toss_winner,toss_decision,winner) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name_of_person,team1, team2, toss_winner,toss_decision,winner)
    cur.execute(sql, val)
    conn.commit()
    conn.close()
    
    
@app.route("/", methods=['GET', 'POST'])
def home():
    winner = "Please enter correct info"
    check = " "
    if request.method == "POST":     
         name = str(request.form.get("name"))
         team1 = str(request.form.get("team1"))
         team2 = str(request.form.get("team2"))
         toss_winner = str(request.form.get("toss_winner"))
         toss_decision = str(request.form.get("toss_decision"))
         if team1 != team2 and (team1 == toss_winner or team2 == toss_winner) and ((toss_decision == "bat" and toss_winner == team1)or (toss_decision == "field" and toss_winner == team2)) :
             team1_d = team_decoder.transform([team1])
             team2_d = team_decoder.transform([team2])
             toss_winner_d = team_decoder.transform([toss_winner])
             toss_decision_d = toss_decoder.transform([toss_decision])
             y = model.predict([[team1_d[0],team2_d[0],toss_winner_d[0],toss_decision_d[0]]])
             result = team_decoder.inverse_transform([y[0]])
             winner = result[0]
             insert(name,team1, team2, toss_winner,toss_decision,winner)
             return render_template("index.html", bmi = winner)
    return render_template("index.html", bmi = winner)
         



         
@app.errorhandler(ValueError)
def page(e):
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)