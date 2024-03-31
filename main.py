from flask import Flask, render_template

import pandas as pd
csv_file_path = 'data/qa_pairs.csv'
df = pd.read_csv(csv_file_path)
qa_pairs = list(df.itertuples(index=False, name=None))

app = Flask(__name__)

@app.route("/")
def homepage():
  return render_template("homepage.html")

@app.route("/q&aList")
def qalist():
  return render_template("qalist.html", qa_pairs=qa_pairs)

@app.route("/interactive")
def interactive():
  return render_template("interactive.html")
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug = True)