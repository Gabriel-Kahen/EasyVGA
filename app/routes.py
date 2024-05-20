from flask import request, render_template
from app import app
from app.utils import prepare, finish, run_c_program
import os
import numpy as np

@app.route('/', methods=['GET', 'POST'])
def index():
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

            resolution = 100
            threshold = 128
            max_range = 200

            array = prepare(os.path.join('app', 'static', uploaded_file_path), resolution, threshold)

            rows, cols = array.shape
            run_c_program(rows, cols, max_range, array)

            with open('data.txt', 'r', encoding='latin-1') as file:
                lines = file.readlines()
            os.remove("data.txt")

            data = [list(map(int, line.strip().split())) for line in lines]
            array_2d = np.array(data)
            finish(array_2d)

            output_file_path = "images/output.png"

    return render_template('index.html', uploaded_file_path=uploaded_file_path, output_file_path=output_file_path)