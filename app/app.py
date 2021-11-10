from flask import Flask,render_template
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
    return render_template('index.html', header=header, record=record,MAX=MAX,MIN=MIN)

if __name__ == '__main__':
    app.run()
