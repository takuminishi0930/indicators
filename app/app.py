from flask import Flask,render_template
import pandas as pd
#Flaskオブジェクトの生成
app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv('app/static/csv/indicators.csv', encoding="utf-8", na_filter=False)
    header = df.columns.tolist()
    record = df.values.tolist()
    return render_template("index.html", header=header, record=record)

if __name__ == "__main__":
    app.run()
