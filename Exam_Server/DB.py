import sqlite3

def create_db():
    print("creating db")
    con = sqlite3.connect("exam.db")
    con.execute('''create table if not exists student(name string, university string, marks integer)''')
    con.execute('''create table if not exists questions
                (question string, op1 string, op2 string, op3 string, op4 string, correct string)''')

    con.execute("insert into student values ('munivara', 'cisco', 0)")

    questions = {
        "Which is the Capital city of Karnataka?": ["blr", "chn", "mum", "tpuram", "blr"],
        "10+20 = ?": ["10", "20", "30", "40", "30"],
        "1+2 = ?": ["1", "2", "3", "4", "3"],
        "Which is the national animal of India?": ["Monkey", "Giraffe", "Human", "Tiger", "Tiger"],
        "When is Republic Day of India celebrated?": ["Today", "Yesterday", "Jan 26", "Aug 15", "Jan 26"]
    }
    for que in questions.keys():
        con.execute("insert into questions values('{}', '{}', '{}', '{}', '{}', '{}')".
                    format(que, questions[que][0], questions[que][1], questions[que][2], questions[que][3],
                           questions[que][4]))

    for stu in con.execute("select * from student").fetchall():
        print(stu)

    questions = {}
    index = 1
    for ques in con.execute("select * from questions").fetchall():
        question = {'Q': str(list(ques)[0]), 'O': list(ques)[1:5]}
        questions["{}".format(index)] = question
        index += 1

    print(questions)
    con.commit()
    con.close()
    print("closing db")

def display():
    print("display")
    con = sqlite3.connect("exam.db")
    for stu in con.execute("select * from student").fetchall():
        print(stu)
    con.close()
    print("close dis")

if __name__ == "__main__":
    create_db()
    display()

