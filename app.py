import json

from flask import Flask, request, render_template

from service import get_score_detail, get_gpa_info, beautify_msg

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/score', methods=["POST"])
def get_score():
    username = request.form['username']
    password = request.form['password']
    year = request.form['year']
    term = request.form['term']
    config = [username, password, year, term]
    score_list = beautify_msg(get_gpa_info(config, get_score_detail(config)))
    return json.dumps(score_list)


if __name__ == '__main__':
    app.run()
