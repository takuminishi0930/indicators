from flask import Flask,render_template
import pandas as pd
import math
#Flaskオブジェクトの生成
app = Flask(__name__)

@app.route("/")
def home():
    # df = pd.read_csv('app/static/csv/indicators.csv', encoding="utf-8", na_filter=False)
    df = pd.read_csv('app/static/csv/indicators.csv', encoding="utf-8")
    header = df.fillna('').columns.tolist()
    record = df.fillna('').values.tolist()
    MAX = list(df.max())
    MIN = list(df.min())
    return render_template("index.html", header=header, record=record,MAX=MAX,MIN=MIN)

if __name__ == "__main__":
    app.run()
