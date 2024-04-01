from flask import Flask, render_template, request, flash, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = '398f0f8f2e664dbcafd8e70ef92386d9'

csv_file_path = 'data/qa_pairs.csv'
df = pd.read_csv(csv_file_path)
qa_pairs = list(df.itertuples(index=False, name=None))

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/qa_list")
def qa_list():
    return render_template("qalist.html", qa_pairs=qa_pairs)

@app.route("/interactive", methods=['GET', 'POST'])
def interactive():
    if request.method == 'POST':
        user_question = request.form['question'].lower().strip()
        user_question_set = set(user_question.split())

        found_answer = ""  
        max_keyword_matches = 0

        for qa_pair in qa_pairs:
            stored_question, stored_answer = qa_pair
            question_set = set(stored_question.lower().strip().split())
            keyword_matches = user_question_set.intersection(question_set)

            if len(keyword_matches) > max_keyword_matches:
                max_keyword_matches = len(keyword_matches)
                found_answer = stored_answer  

        if found_answer:
            session['answer'] = found_answer
            print("Answer saved to session:", found_answer) 
        else:
            flash("Sorry, I couldn't find an answer to your question.")

        return redirect(url_for('interactive'))
    
    answer = session.pop('answer', None) if 'answer' in session else None
    print("Answer retrieved from session:", answer)

    return render_template("interactive.html", answer=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
