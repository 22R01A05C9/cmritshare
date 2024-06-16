from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import models.db
import os,base64

app = Flask(__name__)
app.secret_key = 'team1project'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login_api', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        response =  models.db.getLoginUserid(email, password)
        if response:
            session['userid'] = response['id']
            session['role']= response['role']
            if response['role']=='student':
                return jsonify({'redirect': url_for('student')})
            else:
                return jsonify({'redirect':url_for('faculty')})
        else:
            return jsonify({'error': 'User is not registered'}), 401
    return jsonify({'error': 'Invalid request method'}), 405


@app.route('/student')
def student():
    if not session['userid']:
        return redirect(url_for('home'))
    userid=session['userid']
    data=models.db.getstudentdetails(userid)
    return render_template('student_profile.html', data=data)


@app.route('/student/assignments')
def stdassignments():
    if 'userid' not in session or session['userid'] == '':
        return redirect(url_for('home'))
    userid=session['userid']
    data=models.db.getstdassignments(userid)
    return render_template('stdassignments.html',data=data)


@app.route('/upload/<assid>',methods=['POST','GET'])
def upload(assid):
    if not session['userid']:
        return redirect(url_for('home'))
    data=models.db.assdata(assid)
    return render_template('uploadass.html',data=data)
    
    
@app.route('/uploadass',methods=['POST'])
def uploadass():
    if session['userid']:
        userid = session['userid']
        data= request.get_json()
        assid = int(data['assid'])
        i=1
        os.mkdir(os.path.join(os.getcwd(),"static\\assignments\\"+str(assid)+"\\"+str(userid)))
        for image in data['imageList']:
            imageData = image['imgUrl'].replace('data:image/png;base64,', '')
            try:
                imageByte = base64.b64decode(imageData)
                imagePath = os.path.join(os.getcwd(),'static','assignments',str(assid),str(userid), str(i) + '.png')
                with open(imagePath, 'wb') as imgFile:
                    imgFile.write(imageByte)
            except Exception as e:
                print('error' , e)
                return jsonify({"status":"Failed To Upload PLease Try Again Later"})
            i+=1
        if models.db.uploadass(assid,userid):
            return jsonify({"status" : "Successfully Uploaded"})
        return jsonify({"status":"Failed To Upload PLease Try Again Later"})
    return jsonify({"status":"Failed To Upload PLease Try Again Later"})

@app.route('/uploadspp',methods=['POST'])
def uploadspp():
    if session['userid']:   
        userid = session['userid']
        file = request.files['pp']
        file.save(os.path.join(os.getcwd(),f"static\\imgs\\{userid}.png"))
        res = models.db.uploadspp(userid) 
        if res==1:
            return "ok"
        else:
            return "false"   
    else:
        return "false"
    
    
@app.route('/faculty')
def faculty():
    if not session['userid']:
        return redirect(url_for('home'))
    userid=session['userid']
    data=models.db.getfacultydetails(userid)
    return render_template('teacherprofile.html',data=data)


@app.route('/faculty/assignments')
def factass():
    if not session['userid']:
        return redirect(url_for('home'))
    userid=session['userid']
    data=models.db.getfactassdtls(userid)
    return render_template('teacherass.html',data=data)


@app.route("/faculty/assignments/<assid>")
def factassdtls(assid):
    if not session['userid']:
        return redirect(url_for('home'))
    userid=session['userid']
    data=models.db.getassdtls(userid,assid)
    return render_template('factassdet.html',data=data)


@app.route("/faculty/evaluate/<assid>/<rollno>",methods=['GET'])
def facteval(assid,rollno):
    if session['userid']:
        userid=session['userid']
        res = models.db.check(assid,rollno,userid)
        if res['status']=="Matched":
            l=len(os.listdir(os.path.join(os.getcwd(),"static","assignments",str(assid),rollno)))
            return render_template("evaluate.html",assid=assid,rollno=rollno,length=l)
        else:
            if res['status'] == "Already Evaluated":
                return render_template("alreadyevaluated.html")
            return res
    return redirect(url_for('home'))


@app.route("/evaluateassignments",methods=['POST'])
def ecal():
    if session['userid']:
        userid=session['userid']  
        data=request.get_json() 
        assid = data['assid']  
        rollno = data['rollno']  
        mark = data['marks']
        res = models.db.eval(assid,rollno,mark,userid)
        return res
    else:
        return "No User Found Please Login"
    
    
@app.route('/postass',methods=['POST'])
def postass():
    if session['userid']:
        userid = session['userid']
        file = request.files['questions']
        file.save(os.path.join(os.getcwd(),"static","questions",secure_filename(file.filename)))
        data=request.form
        assname = data['name'] 
        date=data['date']
        td=date.split("-")
        date=td[2]+"-"+td[1]+"-"+td[0]
        description= data['description']
        assid = models.db.postassignment(userid,assname,date,description,secure_filename(file.filename),request.url_root)
        return jsonify({"status":"success","assid":assid})
    return jsonify({"status":"error"})
    
    
@app.route('/uploadfpp',methods=['POST'])
def uploadfpp():
    if session['userid']:  
        userid = session['userid']
        file = request.files['pp']
        file.save(os.path.join(os.getcwd(),f"static\\imgs\\{userid}.png"))
        res = models.db.uploadfpp(userid) 
        if res==1:
            return "ok"
        else:
            return "false"   
    else:
        return "false"
    

@app.route('/forgot',methods=['POST','GET'])
def forgot():
    if request.method=='GET':
        return render_template('forgotpass.html')
    if session['otp']:
        otp=session['otp']
        data=request.form
        if otp == data['otp']:
            session.pop("otp",None)
            res=models.db.forgot(data['email'],data['password'])
            if res==1:
                return jsonify({"status":"success"})
            else:
                return jsonify({"status":"some error occured"})
        else:
            return jsonify({"status":"incorrect otp"})
    return jsonify({"status":"some error occured"})
    
    
@app.route('/sendotp',methods=['POST'])
def sendotp():
    data=request.form
    email = data['email']
    res = models.db.sendotp(email)
    if res['status'] == "success":
        session['otp']=res['otp']
        return jsonify({"status":"success"})
    else:
        return res


@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('role',None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',ssl_context="adhoc")
    # app.run(debug=True,host='0.0.0.0')
