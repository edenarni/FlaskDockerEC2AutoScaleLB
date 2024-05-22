from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import boto3
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use environment variables for database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Use environment variables for AWS credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# DB CONFIGURATION
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def index():
    return "main page"

@app.route('/show_users/')
def show_users():
    users = User.query.all()
    return " ".join([str((cur_user.id,cur_user.name)) for cur_user in users])

@app.route("/add_user/", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        new_user = User(name=user_name, email=user_email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('show_image', user_name=user_name))
    return render_template('add_user.html')

@app.route("/show_image/")
def show_image():
    user_name = request.args.get('user_name', 'Guest')

    s3_bucket = os.getenv('S3_BUCKET_NAME')
    image_key = os.getenv('S3_IMAGE_KEY')

    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': s3_bucket, 'Key': image_key},
        ExpiresIn=3600  # URL expiration time in seconds
    )
    print(image_url)

    return render_template('show_image.html', image_url=image_url, user_name=user_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)