from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import boto3


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db" # DB CONFIGURATION
# todo: save the details of the container in variabels?
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://eden:1234@postgres-db-container:5432/postgres_db"

db = SQLAlchemy(app)
migrate = Migrate(app, db) # DB CONFIGURATION

# connect to s3 bucket
s3_client = boto3.client('s3')


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
    # todo: change s3 bucket to private and use s3.getObjects instead

    s3_bucket = "eden-project-images-bucket-1605"
    image_key = "Screenshot 2024-05-16 at 11.08.54.png"

    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': s3_bucket, 'Key': image_key},
        ExpiresIn=3600  # URL expiration time in seconds
    )
    print(image_url)

    # image_url = f"https://{s3_bucket}.s3.amazonaws.com/{image_key}"


    return render_template('show_image.html', image_url=image_url, user_name=user_name)



if __name__ == "__main__":
    # host - This parameter specifies the hostname or IP address on which the server will listen for incoming connections.
    # port - This parameter specifies the port number on which the server will listen for incoming connections.
    # You can access your Flask application by navigating to
    # http://localhost:5555 in your web browser
    # or by using the IP address of the host machine running the Flask application followed by port 5555.
    # app.run(host='0.0.0.0', port=5555)
    app.run(host='0.0.0.0', port=5001, debug=True)
