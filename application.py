import os, boto, random, string, datetime
from datetime import datetime
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

dynamo = Dynamo(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Connect to Amazon S3
        data_files = request.files.getlist('file')
		location = request.form['location']
		now = datetime.now().strftime("%Y-%m-%d%H-%M-%S")
		
		fileName = UploadFileToS3(data_files, now)
		CreateLocationFileEntry(location)
		CreatePictureEntry(fileName, now, location);

	locationPictureData = getLocationPictureData()
    return render_template('index.html',locationPictureData=locationPictureData)

def UploadFileToS3(data_files, now):
    s3 = boto.connect_s3()
    bucket = s3.get_bucket(S3BUCKET)
    k = Key(bucket)
		
	for data_file in data_files:
		file_contents = data_file.read()
		k.key = now + data_file.filename
		print "Uploading some data to " + S3BUCKET + " with key: " + k.key
		k.set_contents_from_string(file_contents)
	return k.key
		
def CreateLocationFileEntry(location):
    randomStr = ''.join(random.choice(string.lowercase) for i in range(7))
    dynamo.Locations.put_item(data={
        'LocationName': location,
        'Address': '123 cap hill' + randomStr,
    })

def CreatePictureEntry(fileName, now, location):
    dynamo.Pictures.put_item(data={
        'PictureId': fileName,
		'Date': now,
        'LocationName': location,
		'PictureURL': 'https://s3-us-west-2.amazonaws.com/isithappeningpictures/'+ fileName,
    })

def getLocationPictureData():
    pictures = dynamo.Pictures.scan()
    allPictures = list(pictures)
	return allPictures

    #locationData = {
	#	"LocationName": "the location name",
	#	"PictureURL": "www.google.com",    
	#}
	
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
