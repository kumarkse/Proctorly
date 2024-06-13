from flask import Flask,render_template,request,jsonify
import base64,os
import streamlit as st
from datetime import datetime
from face_dtect import count_faces

app  = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/proctor")
def helloproctor():
    return render_template("proctor.html")
counter=0

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    # Get JSON data from the request
    data = request.get_json()

    # Extract photo data URL from JSON
    photo_data_url = data.get('photo')
    

    # Check if photo_data_url is not None and is a base64 encoded string
    if photo_data_url and photo_data_url.startswith('data:image/jpeg;base64,'):
        # Extract base64 encoded image data
        img_data = photo_data_url.split(',')[1]

        # Decode base64 data
        try:
            img_binary = base64.b64decode(img_data)
        except Exception as e:
            return jsonify({'error': 'Failed to decode image data'}), 400
        
        if count_faces(img_binary) == 1:
            return jsonify({'message': 'Anomaly detected', }), 200

        # Specify the directory where you want to save the image
        save_dir = 'save_images'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f'uploaded_image_{timestamp}.jpg'
        # Save image file to the specified directory
        try:
            with open(os.path.join(save_dir, filename), 'wb') as f:
                f.write(img_binary)
        except Exception as e:
            return jsonify({'error': 'Failed to save image file'}), 500

        # Optionally, you can respond with a success message
        return jsonify({'message': 'Photo uploaded and saved successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid photo data URL'}), 400


if __name__ == "__main__":
    app.run(debug=True)