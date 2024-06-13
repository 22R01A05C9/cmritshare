from pymongo import MongoClient 
from datetime import datetime
import random
from threading import Thread
from smtplib import SMTP

client = MongoClient('mongodb://localhost:27017/')
database = client.maindb 
users = database.users


def postass(userid,assname,date,assid):
    server = SMTP("smtp-mail.outlook.com",587)
    assignments = database.assignments
    teachers=database.teachers
    students=database.students
    td=teachers.find_one({"teacherid":int(userid)})
    data={
        "assignmentid":assid,
        "teacherid":int(userid),
        "date":date,
        "subject": td['subject'],
        "assname":assname,
        "teachername":td['name']
    }
    assignments.insert_one(data)
    asarr=td['assignments']
    asarr.append(assid)
    teachers.update_one({"teacherid":userid},{"$set":{"assignments":asarr}})
    server.starttls()
    server.login("cmritshare@outlook.com","S@iteja2005")
    for i in td['students']:
        sd=students.find_one({"rollno":i})
        sd['assignments'][str(assid)]=0
        students.update_one({"rollno":i},{"$set":{"assignments":sd['assignments']}})
        message=f"Subject:New Assignment Posted\n\nHello {sd['firstname']} {sd['lastname']} Your Faculy Mr/Ms/Mrs {td['name']} Has Posted A New Assignment, Here Are The Details\nName: {assname}\nAssignment ID: {assid}\nDeadline: {date}\n Please Visit The Website For More Information"
        server.sendmail("cmritshare@outlook.com",sd['email'],message)
        
        
    


def createUser( userData : dict):
    response = users.insert_one(userData)
    return response 

def getLoginUserid(email, password):
    response = users.find_one({'email': email ,'pass' : password})
    return response


def getstudentdetails(userid):
    students = database.students
    data = students.find_one( {'rollno' : userid})
    return data

def getstdassignments(userid):
    students=database.students
    assignments = database.assignments
    allass=students.find_one({'rollno':userid})['assignments']
    for i in allass:
        if allass[i]==0:
            res = list(map(int,str(assignments.find_one({'assignmentid':int(i)})['date']).split('-')))
            date=datetime(res[2],res[1],res[0]+1)
            cd=datetime.now()
            if cd>date:
                allass[i]=2
    students.update_one({'rollno':userid},{"$set":{"assignments":allass}}) 
    data=[]
    for i in allass:
        res = assignments.find_one({'assignmentid':int(i)})
        di = {'teachername':res['teachername'], 'subject':res['subject'], 'assid':res['assignmentid'], 'date':res['date'],'status':allass[i],'assname':res['assname']}
        data.append(di)
    return data
  

def uploadpp(userid):
    students = database.students
    res = students.update_one({'rollno':str(userid)},{"$set":{"image":f"/imgs/{userid}.png"}})
    return res.matched_count
    
    
def uploadass(assid,userid):
    students = database.students
    data=students.find_one({'rollno':str(userid)})['assignments']
    for i in data:
        if i == str(assid):
            data[i]=True
            break
    res = students.update_one({'rollno':str(userid)},{"$set":{"assignments":data}})
    return res.modified_count


def postassignment(userid,assname,date):
    assignments = database.assignments
    ids=[]
    for i in assignments.find():
        ids.append(i['assignmentid'])
    assid=ids[0]
    while(assid in ids):
        assid=random.randint(1111,9999)
    Thread(target=postass,args=(userid,assname,date,assid,)).start()
    return assid

