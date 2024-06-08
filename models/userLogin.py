from pymongo import MongoClient 
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
database = client.collegeProject 
users = database.users


def createUser( userData : dict):
    response = users.insert_one(userData)
    return response 

def getLoginUserid(email, password):
    try:
        response = users.find_one({
            '$and' : [
                {'email'    : email },
                {'password' : password}
            ]
        })
        if(response):
            return str(response['_id'])
        return ''
    except Exception as e:
        return (e)


def getUserDetails(userid):
    try:
        userObjectID = ObjectId(userid)
        user = users.find_one( {'_id' : userObjectID})
        return user
    except Exception as e:
        return { 'status' : 'error', 'msg' : str(e)}
    

