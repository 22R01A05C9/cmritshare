from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import models.userLogin 
import os
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
        response = models.userLogin.getLoginUserid(email, password)
        if response:
            session['userid'] = response['id']
            session['role']= response['role']
            if response['role']=='student':
                return jsonify({'redirect': url_for('student')})
        else:
            return jsonify({'error': 'User is not registered'}), 401
    return jsonify({'error': 'Invalid request method'}), 405


@app.route('/student')
def student():
    if 'userid' not in session or session['userid'] == '':
        return redirect(url_for('home'))
    userid=session['userid']
    data=models.userLogin.getstudentdetails(userid)
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
    data=models.userLogin.detstdassignments(userid)
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
        file.save(f"{os.path.abspath(os.getcwd())}\\cmritShare\\static\\imgs\\{userid}.png")
        res = models.userLogin.uploadpp(userid) 
        if res==1:
            return "ok"
        else:
            return "false"   
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
