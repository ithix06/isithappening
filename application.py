import os, boto
from boto.s3.key import Key
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
from urllib2 import Request, urlopen, URLError

#WIN

os.environ["AWS_ACCESS_KEY_ID"] = "face"
os.environ["AWS_SECRET_ACCESS_KEY"] = "palm"

UPLOAD_FOLDER = '/home/ec2-user/eb_flask_app/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
S3BUCKET = 'isithappeningpictures'
S3ACCESSKEY = 'AKIAIGW66S5R2QNINKXA'
S3SECRETKEY = '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'

upload_text = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

#conn = tinys3.Connection(S3ACCESSKEY,S3SECRETKEY,tls=True)

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#iapp.config['S3_BUCKET_NAME'] = S3BUCKET
#s3 = FlaskS3(application)


def sendFileToS3(filename):
    #conn.upload('some_file.zip',f,'my_bucket')
    #conn.upload(filename, file, S3BUCKET)
    #f = open('images/' + filename, 'rb')
    #conn.upload(filename, f, S3BUCKET)
    #print conn
    f = open('myfile.txt', 'rb')
    #conn.upload('myfile.txt', f, S3BUCKET)

def getHappeningData():
    #https://block.io/api/v2/get_balance/?api_key=fe8d-1449-642e-b4d7
    response = urlopen(request)
    return response.read()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def index():

    # If user has submitted the form...
    if request.method == 'POST':

        # Connect to Amazon S3
        s3 = boto.connect_s3()

        # Get a handle to the S3 bucket
        bucket_name = 'isithappeningpictures'
        bucket = s3.get_bucket(bucket_name)
        k = Key(bucket)

        # Loop over the list of files from the HTML input control
        data_files = request.files.getlist('file[]')
        for data_file in data_files:

            # Read the contents of the file
            file_contents = data_file.read()

            # Use Boto to upload the file to the S3 bucket
            k.key = data_file.filename
            print "Uploading some data to " + bucket_name + " with key: " + k.key
            k.set_contents_from_string(file_contents)

    return render_template('index.html')

@application.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            sendFileToS3(filename)
            #return redirect(url_for('uploaded_file', filename=filename))
            return 'upload complete'
    return upload_text


# add a rule for the index page.
#application.add_url_rule('/', 'index', (lambda: header_text + instructions + footer_text))

application.add_url_rule('/getHappeningData','data',(lambda: getHappeningData()))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:header_text + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0')
