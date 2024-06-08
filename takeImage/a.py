from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# Ensure the upload directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400
    
    image_data = data['image']
    image_data = image_data.replace('data:image/png;base64,', '')
    try:
        image_bytes = base64.b64decode(image_data)
        image_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.png')
        with open(image_path, 'wb') as image_file:
            image_file.write(image_bytes)
        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
