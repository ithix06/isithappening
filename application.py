import os, boto
from boto.s3.key import Key
from flask import Flask, request, redirect, url_for, render_template
from flask.ext.dynamo import Dynamo
from urllib2 import Request, urlopen, URLError
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table

#TODO: DYNAMO http://flask-dynamo.readthedocs.org/en/latest/quickstart.html

S3BUCKET = 'isithappeningpictures'

app = Flask(__name__)
app.config['DYNAMO_TABLES'] = [
    Table('Locations', schema=[HashKey('LocationName')]),
    Table('Pictures', schema=[HashKey('PictureId')]),
]

@app.route('/', methods=['GET', 'POST'])
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
	
@app.route('/create_location')
def create_location():
    dynamo.Locations.put_item(data={
        'LocationName': 'unicorn',
        'Address': '123 cap hill',
    })

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
