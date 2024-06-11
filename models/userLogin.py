from pymongo import MongoClient 
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
database = client.maindb 
users = database.users


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

def detstdassignments(userid):
    students=database.students
    allass=students.find_one({'rollno':userid})['assignments']
    data=[]
    assignments = database.assignments
    for i in allass:
        res = assignments.find_one({'assignmentid':int(i)})
        di = {'teachername':res['teachername'], 'subject':res['subject'], 'assid':res['assignmentid'], 'date':res['date'],'submitted':allass[i]}
        data.append(di)
    return data

def uploadpp(userid):
    students = database.students
    res = students.update_one({'rollno':str(userid)},{"$set":{"image":f"/imgs/{userid}.png"}})
    return res.matched_count
    
