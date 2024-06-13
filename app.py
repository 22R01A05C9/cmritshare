from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import models.db
import os,base64
from datetime import datetime
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


@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('role',None)
    return redirect(url_for('home'))


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
    return render_template('uploadass.html',assid=assid)


@app.route('/uploadpp',methods=['POST'])
def uploadpp():
    userid=session['userid']
    if userid:   
        file = request.files['pp']
        file.save(f"D:\\bunny\\coding\\app_development\\flask\\assignment\\main\\cmritShare\\static\\imgs\\{userid}.png")
        res = models.db.uploadpp(userid) 
        if res==1:
            return "ok"
        else:
            return "false"   
    else:
        return "false"
    
@app.route('/uploadass',methods=['POST'])
def uploadass():
    userid = session['userid']
    if userid:
        data= request.get_json()
        assid = int(data['assid'])
        i=1
        os.mkdir("D:\\bunny\\coding\\app_development\\flask\\assignment\\main\\cmritShare\\static\\assignments\\"+str(assid)+"\\"+str(userid)+"\\")
        for image in data['imageList']:
            imageData = image['imgUrl'].replace('data:image/png;base64,', '')
            try:
                imageByte = base64.b64decode(imageData)
                imagePath = os.path.join("D:\\bunny\\coding\\app_development\\flask\\assignment\\main\\cmritShare",'static','assignments',str(assid),str(userid), str(i) + '.png')
                with open(imagePath, 'wb') as imgFile:
                    imgFile.write(imageByte)
            except Exception as e:
                print('error' , e)
                return jsonify({"status":"fail"})
            i+=1
        if models.db.uploadass(assid,userid):
            return jsonify({"status" : "success"})
        return jsonify({"status":"fail"})
    return jsonify({"status":"fail"})


@app.route('/postass',methods=['POST'])
def postass():
    userid = session['userid']
    if userid:
        assname = "mid-2" #get the assignment name from request
        date="15-06-2024" #also get the assignment last date to submit from request
        dl=date.split('-')
        ad = datetime(dl[2],dl[1],dl[0])
        cd = datetime().now()
        if cd <ad:
            return jsonify({"status":"error invalid date"})
        assid = models.db.postassignment(userid,assname,date)
        return jsonify({"status":"success","assid":assid})
    return jsonify({"status":"error"})


if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',ssl_context="adhoc")
    app.run(debug=True,host='0.0.0.0')
