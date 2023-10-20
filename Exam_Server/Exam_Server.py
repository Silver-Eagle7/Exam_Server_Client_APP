import sqlite3

from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def welcome():
    return jsonify({'msg': "Welcome to Python"})


@app.route('/exam/create_student', methods=['POST'])  # end point1 ( Display all)
@cross_origin()
def create_student():
    if not request.json:
        abort(400)
    con = sqlite3.connect("exam.db")
    con.execute("insert into student values('{}','{}',{})".format(request.json.get('student'),
                                                                  request.json.get('university'),
                                                                  0))
    con.commit()
    con.close()
    return jsonify(request.json), 201


@app.route('/exam/get_questions', methods=['GET'])
@cross_origin()
def get_questions():
    con = sqlite3.connect("exam.db")
    questions = {}
    index = 1
    for ques in con.execute("select * from questions").fetchall():
        print(ques)
        question = {'Q': str(list(ques)[0]), 'O': list(ques)[1:5]}
        questions["{}".format(index)] = question
        index += 1
    print(questions)
    con.close()
    return jsonify(questions), 200


@app.route('/exam/validate/<student_name>', methods=['POST'])
@cross_origin()
def validate_marks(student_name):
    if not request.json:
        abort(400)
    con = sqlite3.connect("exam.db")
    result = con.execute("select question, correct from questions").fetchall()
    answers = dict(request.json)
    marks = 0
    print(answers)
    for ques in result:
        if str(answers[ques[0]]) == str(ques[1]):
            marks += 1
    con.execute("UPDATE student SET marks={} WHERE name='{}'".format(marks, student_name))
    con.commit()
    con.close()
    return jsonify({'score': marks}), 201


@app.route('/exam/get_marks/<student_name>', methods=['GET'])
@cross_origin()
def get_marks(student_name):
    if not request.json:
        abort(400)
    con = sqlite3.connect("exam.db")
    result = con.execute("select name, marks from student where name='{}'".format(student_name)).fetchall()
    msg = {}
    for ques in result:
        msg = {'name': ques[0], 'marks': ques[1]}
    con.close()
    return jsonify(msg), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
