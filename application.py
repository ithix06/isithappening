import os, boto
from boto.s3.key import Key
from flask import Flask, request, redirect, url_for, render_template
from urllib2 import Request, urlopen, URLError

#TODO: DYNAMO http://flask-dynamo.readthedocs.org/en/latest/quickstart.html

S3BUCKET = 'isithappeningpictures'

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Connect to Amazon S3
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(S3BUCKET)
        k = Key(bucket)
        data_files = request.files.getlist('file')
		
        for data_file in data_files:
            file_contents = data_file.read()
            k.key = data_file.filename
            print "Uploading some data to " + S3BUCKET + " with key: " + k.key
            k.set_contents_from_string(file_contents)

    return render_template('index.html')

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
