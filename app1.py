from flask import Flask, render_template, request, redirect, url_for
import os
from aadhar import process_pdf
import subprocess
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Run your Python script here with the file_path
        # Import the temp.py functions or use subprocess to run it
         # Assuming you have a function process_file in temp.py

        # Get the data from temp.py (this will vary depending on your script)
        name, father, dob, number , gen , mobile= process_pdf(file_path)
        
        # Return the data to the HTML form
        return render_template('index.html', name=name, father=father, dob=dob, number=number,gen=gen,mobile=mobile)


@app.route('/process-file', methods=['POST'])
def process_file():
    file = request.files['file']

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    # Call external_script.py with the file path
    result = process_pdf(file_path)
    # Return the raw output from external_script.py
    return result # Sends plain text to the frontend

if __name__ == '__main__':
    app.run(debug=True)
