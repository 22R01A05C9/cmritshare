from pymongo import MongoClient 
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
database = client.collegeProject 
subjects = database.subjects


def createSubject( subjectName : str, teacherId :str, teacherName : str):
    userData = {
        "subjectName": subjectName,
        "teacherIds": teacherId, 
        "teacherName": teacherName
    }

    response = subjects.insert_one(userData)
    return response 


def createAssignment():
    pass



print(createSubject( "maths",'66649305592f728b125e284f', "sravanthi"))