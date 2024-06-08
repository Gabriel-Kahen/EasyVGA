from flask import request, render_template
from app import app
from app.utils import prepare, finish, run_c_program
import os
import numpy as np

# Declare the global variable
image_width = 1  # Initial default value
range = None
threshold = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global image_width  # Access the global variable
    uploaded_file_path = None
    output_file_path = None
    

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded"

        file = request.files['file']
        if file.filename == '':
            return "No file selected"

        if file:
            uploaded_file_path = os.path.join('images', 'uploaded_image.png')
            file.save(os.path.join('app', 'static', uploaded_file_path))

            threshold = 128
            range = 200

            array = prepare(os.path.join('app', 'static', uploaded_file_path), image_width, threshold)

            rows, cols = array.shape
            run_c_program(rows, cols, range, array)

            with open('data.txt', 'r', encoding='latin-1') as file:
                lines = file.readlines()
            os.remove("data.txt")

            data = [list(map(int, line.strip().split())) for line in lines]
            array_2d = np.array(data)
            finish(array_2d)

            output_file_path = "images/output.png"

    return render_template('index.html', uploaded_file_path=uploaded_file_path, output_file_path=output_file_path)

@app.route('/set_width', methods=['POST'])
def set_width():
    global image_width  # Access the global variable
    image_width = request.form.get('image_width')
    if image_width:
        image_width = int(image_width)
    return '', 204  # No content response