from flask import Flask, render_template, request, send_from_directory
import boto3
import os
from io import StringIO

app = Flask(__name__)

# Configuring AWS credentials
AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
S3_BUCKET_NAME = 'your_s3_bucket_name'
S3_BUCKET_REGION = 'your_s3_bucket_region'

# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=S3_BUCKET_REGION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    name = request.form['name']
    address = request.form['address']
    email = request.form['email']
    phone_number = request.form['phone_number']
    academic_qualification = request.form['academic_qualification']
    projects = request.form['projects']
    tech_skills = request.form['tech_skills']
    soft_skills = request.form['soft_skills']
    areas_of_interest = request.form['areas_of_interest']
    hobbies = request.form['hobbies']

    # Prepare data to write to file
    file_content = f"Name: {name}\nAddress: {address}\nEmail: {email}\nPhone Number: {phone_number}\n\n"
    file_content += f"Academic Qualifications:\n{academic_qualification}\n\n"
    file_content += f"Projects:\n{projects}\n\n"
    file_content += f"Technical Skills:\n{tech_skills}\n\n"
    file_content += f"Soft Skills:\n{soft_skills}\n\n"
    file_content += f"Areas of Interest:\n{areas_of_interest}\n\n"
    file_content += f"Hobbies:\n{hobbies}\n"

    # Upload file to S3 bucket
    s3.put_object(Bucket=S3_BUCKET_NAME, Key='user_info.txt', Body=file_content)

    return render_template('submission.html')

@app.route('/download')
def download():
    # Generate download link for the file
    download_url = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': S3_BUCKET_NAME,
                                                     'Key': 'user_info.txt'},
                                             ExpiresIn=3600)  # Link valid for 1 hour

    return render_template('download.html', download_url=download_url)

if __name__ == '__main__':
    app.run(debug=True)
