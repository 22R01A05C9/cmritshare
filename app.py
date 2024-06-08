from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from models.userLogin import getLoginUserid, getUserDetails

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
        response = getLoginUserid(email, password)
        if response:
            session['userid'] = response
            print(response)
            return jsonify({'redirect': url_for('profile')})
        else:
            return jsonify({'error': 'User is not registered'}), 401
    return jsonify({'error': 'Invalid request method'}), 405


@app.route('/profile')
def profile():
    if 'userid' not in session or session['userid'] == '':
        return redirect(url_for('home'))
    userid = session['userid']
    data = getUserDetails(userid)
    return render_template('profile.html', data=data)


@app.route('/logout')
def logout():
    session['userid'] = ''
    return redirect(url_for('home'))


@app.route('/assignments')
def assignments():
    if 'userid' not in session or session['userid'] == '':
        return redirect(url_for('home'))
    return render_template('assignments.html')

if __name__ == '__main__':
    app.run(debug=True)
