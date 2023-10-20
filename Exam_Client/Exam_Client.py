import requests
import json

base_url = "http://10.127.142.56:5000"
headers = {"Content-Type": "application/json"}
header_null ={}
payload={}

name = input("Enter your name: ")
inst = input("Enter your university: ")


student_info= json.dumps({"name":name, "university":inst})

response = requests.request("POST",base_url+"/exam/create_student", headers=headers, data=student_info)
print(response.status_code)
print(response.text)

if(response.status_code !=201):
    exit()

questions = requests.request("GET",base_url+"/exam/get_questions", headers=header_null,data=payload)
print(questions.status_code)
if(questions.status_code !=200):
    exit()

questions = json.loads(questions.text)

answers = {}

for ques in questions.values():
    print(ques["Q"])
    for optn in ques["O"]:
        print(optn)
    ans = input("Enter your answer: ")
    answers[ques["Q"]] = ans

answer_info = json.dumps(answers)

response = requests.request("POST",base_url+"/exam/validate/"+name,headers=headers, data=answer_info)
print(response.status_code)
print(response.text)
if(response.status_code !=201):
    exit()
    
marks = json.loads(response.text)

for each in marks.items():
    print(each[0], each[1])