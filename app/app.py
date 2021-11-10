from flask import Flask,render_template,request
import pandas as pd
import datetime
#Flaskオブジェクトの生成
app = Flask(__name__)

@app.route("/")
def home():
    twoDaysAgo = datetime.date.today()-datetime.timedelta(days=2)
    df = pd.read_csv('app/static/csv/{}.csv'.format(twoDaysAgo.strftime('%Y-%m'), encoding="utf-8"))
    header = df.fillna('').columns.tolist()
    record = df.fillna('').values.tolist()
    MAX = list(df.max())
    MIN = list(df.min())
    return render_template('index.html',header=header, record=record,MAX=MAX,MIN=MIN,date=twoDaysAgo)

@app.route("/indicators",methods=["POST"])
def indicators():
    date = request.form.get("d")
    if request.form.get("b")=="":
        month = date-datetime.timedelta(month=1)
    elif request.form.get("n")=="":
        month = date+datetime.timedelta(month=1)
    df = pd.read_csv('app/static/csv/{}.csv'.format(month.strftime('%Y-%m'), encoding="utf-8"))
    header = df.fillna('').columns.tolist()
    record = df.fillna('').values.tolist()
    MAX = list(df.max())
    MIN = list(df.min())
    return render_template('index.html',header=header, record=record,MAX=MAX,MIN=MIN,date=month)

if __name__ == '__main__':
    app.run()
