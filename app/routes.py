from flask import request, render_template, jsonify
from app import app
from app.utils import prepare, finish, run_c_program
import os
import numpy as np

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded"

        file = request.files['file']
        if file.filename == '':
            return "No file selected"

        if file:
            file_path = "uploaded_image.png"
            file.save(file_path)

            resolution = 100
            threshold = 128
            max_range = 200

            array = prepare(file_path, resolution, threshold)
            os.remove(file_path)

            rows, cols = array.shape
            run_c_program(rows, cols, max_range, array)

            with open('data.txt', 'r', encoding='latin-1') as file:
                lines = file.readlines()
            os.remove("data.txt")

            data = [list(map(int, line.strip().split())) for line in lines]
            array_2d = np.array(data)
            finish(array_2d)
            return render_template('index.html', output_file_path="static/images/output.png")

    return render_template('index.html')
