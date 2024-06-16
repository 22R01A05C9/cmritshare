from pymongo import MongoClient 
from datetime import datetime
import random
from threading import Thread
from smtplib import SMTP
import os

client = MongoClient('mongodb://localhost:27017/')
database = client.maindb 
users = database.users


def postass(userid,assname,date,assid,description,filename,rooturl):
    os.mkdir(os.path.join(os.getcwd(),"static","assignments",str(assid)))
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
        "teachername":td['firstname']+" "+td['lastname'],
        "description":description,
        "questions": filename
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
        message=f"Subject:New Assignment Posted\n\nHello {sd['firstname']} {sd['lastname']} Your Faculy Mr/Ms/Mrs {td['firstname']+' '+td['lastname']} Has Posted A New Assignment, Here Are The Details\nName: {assname}\nAssignment ID: {assid}\nDeadline: {date}\nQuestions: {rooturl}static/questions/{filename} \nPlease Visit The Website For More Information"
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
    marks = database.marks
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
        res2=marks.find_one({"userid":userid,"assid":int(i)})
        mark=0
        if res2:
            mark=res2['marks']
        else:
            mark = "Didn't Evaluate"
        di = {'teachername':res['teachername'], 'subject':res['subject'], 'assid':res['assignmentid'], 'date':res['date'],'status':allass[i],'assname':res['assname'],'marks':mark,'questions':res['questions']}
        data.append(di)
    return data
  

def uploadspp(userid):
    students = database.students
    res = students.update_one({'rollno':str(userid)},{"$set":{"image":f"/imgs/{userid}.png"}})
    return res.matched_count
    
def uploadfpp(userid):
    teachers = database.teachers
    res = teachers.update_one({'teacherid':int(userid)},{"$set":{"image":f"/imgs/{userid}.png"}})
    return res.matched_count
    
def uploadass(assid,userid):
    students = database.students
    data=students.find_one({'rollno':str(userid)})['assignments']
    for i in data:
        if i == str(assid):
            data[i]=1
            break
    res = students.update_one({'rollno':str(userid)},{"$set":{"assignments":data}})
    return res.modified_count


def postassignment(userid,assname,date,description,filename,rooturl):
    assignments = database.assignments
    ids=[]
    for i in assignments.find():
        ids.append(i['assignmentid'])
    assid=ids[0]
    while(assid in ids):
        assid=random.randint(1111,9999)
    Thread(target=postass,args=(userid,assname,date,assid,description,filename,rooturl)).start()
    return assid



def sendotp(email):
    users=database.users
    res = users.find_one({"email":email})
    if res:
        server = SMTP("smtp-mail.outlook.com",587)
        server.starttls()
        server.login("cmritshare@outlook.com","S@iteja2005")
        otp = random.randint(1111,9999)
        message= f"Subject:Password Reset OTP\n\nHello {email} Your OTP For Password Reset Of CMRITShare Is {otp}"
        server.sendmail("cmritshare@outlook.com",email,message)
        return {"status":"success","otp":str(otp)}
    else:
        return {"status":"no user found"}
    
sendotp("22r01a05c9@crithyderabad.edu.in")
    
    
def forgot(email,password):
    users = database.users
    res = users.update_one({"email":email},{"$set":{"password":password}})
    return res.modified_count

def getfacultydetails(userid):
    teachers = database.teachers
    res = teachers.find_one({"teacherid":int(userid)})
    res['role']="Faculty"
    return res

def getfactassdtls(userid):
    teachers = database.teachers
    assignmetns = database.assignments
    assids = teachers.find_one({"teacherid":int(userid)})['assignments']
    data=[]
    for i in assids:
        ts=assignmetns.find_one({"assignmentid":int(i)})
        td={"assid":i,"assname":ts['assname'],"date":ts['date'],"view":f"/faculty/assignments/{i}"}
        data.append(td)
    return data
    
    
def getassdtls(userid,assid):
    students = database.students
    marks = database.marks
    teachers = database.teachers
    data=[]
    td=teachers.find_one({"teacherid":int(userid)})
    stds=td['students']
    for i in stds:
        sd=students.find_one({"rollno":i})
        m=marks.find_one({"assid":int(assid),"userid":i})
        if not m:
            m="Didn't Evaluate"
        else:
            m=m['marks']
        td={"assid":assid,"rollno":i,"stdname":sd['firstname']+" "+sd['lastname'],"status":sd['assignments'][str(assid)],"marks":m}
        data.append(td)
    return data
        

def eval(assid,rollno,mark,userid):
    students = database.students
    teachers = database.teachers
    marks = database.marks
    if str(assid) in students.find_one({"rollno":rollno})['assignments']:
        if int(assid) in teachers.find_one({"teacherid":int(userid)})['assignments']:
            marks.insert_one({"marks":int(mark),"assid":int(assid),"userid":rollno})
            return {"status":"Evaluated Successfull"}
        else:
            return {"status":"Faculty Not Assigned With The Assignment"}
    else:
        return {"status":"Student Not Assigned With This Assignment"}
    
        
    
def check(assid,rollno,userid):
    students = database.students
    teachers = database.teachers
    marks = database.marks
    assmts = students.find_one({"rollno":rollno})['assignments']
    if assmts and str(assid) in assmts:
        tass= teachers.find_one({"teacherid":int(userid)})['assignments']
        if tass and int(assid) in tass:
            mark = marks.find_one({"assid":int(assid),"userid":rollno})
            if mark:
                return {"status":"Already Evaluated"}
            return {"status":"Matched"}
        else:
            return {"status":"Faculty Not Assigned With The Assignment"}
    else:
        return {"status":"Student Not Assigned With This Assignment"}
    

def assdata(assid):
    assignments=database.assignments
    return assignments.find_one({"assignmentid":int(assid)})