from flask import Flask, request , jsonify, render_template
from flask_cors import CORS
import base64, os


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods = ['POST'])
def upload():
    data = request.get_json()
    for image in data['imageList']:
        imageData = image['imgUrl'].replace('data:image/png;base64,', '')
        try:
            imageByte = base64.b64decode(imageData)
            imagePath = os.path.join('uploads', str(image['name']) + '.png')

            with open(imagePath, 'wb') as imgFile:
                imgFile.write(imageByte)
        except Exception as e:
            print('error' , e)
    return jsonify({
        "status" : "success"
    })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
