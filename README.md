# Flask App with PostgreSQL, Docker, AWS EC2 and AWS S3 Integration

# Quick Start Guide: Running Dockerized Application with Docker Compose (localy)

1. **Clone the Repository**: Clone the repository to your local machine using 
```
git clone [<repository-url>](https://github.com/edenarni/FlaskDockerEC2AutoScaleLB.git)
```

2. **Navigate to the Repository Directory**: Move into the cloned repository's directory with 
```
cd FlaskDockerEC2AutoScaleLB
```

3. **Install Requirements**: Run the following command to install the dependencies listed in the requirements.txt file:
```
pip install -r requirements.txt
``` 

4. **Create Environment Variables File**: Duplicate the provided `.env.example` file and rename it to `.env`. This file will contain your environment variables needed for the application to run.
Open the `.env` file in a text editor and set the necessary environment variables

5. **Run Docker Compose**: To start the application defined in the `docker-compose.yml` file, execute 
```
docker-compose up --build -d
```

6. **Access the Application**: Once the containers are up, access the application through `http://localhost:5001` in your web browser.

7. **Stopping the Application**: to remove the containers and associated resources run
```
docker-compose down
``` 

With these steps, you'll have your application running locally using Docker Compose, with the necessary environment variables configured and requirements installed for its operation.


# Quick Deployment Guide: Deploying Your Dockerized Application to an EC2 Instance
## Overview
This is a simple Flask application that allows users to register and then redirects them to a page displaying a constant image from an private AWS S3 bucket. The application is containerized using Docker and can be deployed on an AWS EC2 instance. The project uses PostgreSQL as the database and utilizes environment variables for configuration.

The deployment also includes auto scaling and load balancing to ensure high availability and scalability. Auto scaling dynamically adjusts the number of EC2 instances based on the application's load, while the load balancer distributes incoming traffic across multiple instances to ensure even load distribution and high availability.

## Features
- **Flask Application:** A lightweight web application framework.
- **PostgreSQL:** A robust and reliable relational database.
- **Docker:** Containerization of the application for consistency across environments.
- **AWS EC2:** Scalable compute capacity in the cloud.
- **AWS S3:** Secure, durable, and scalable object storage.
- **Auto Scaling:** Automatically adjusts the number of EC2 instances to handle the load.
- **Load Balancing:** Distributes incoming application traffic across multiple EC2 instances.


## Setup Steps

### 1. Create an S3 Private Bucket:

<img src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/30c2ab1f-abf8-4f30-ae75-f1ebcd8312c8" width="700"><br>
<img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/42fba9b6-86ba-40ea-bdff-86e2bb2df5a5"><br>

make sure you block all public access: <br>
<img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/79619281-7872-4b77-9751-36c009a6b5f1"><br>

This is our bucket:<br>
<img src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/b2548742-1bd8-482c-9bce-9bd2d7413608" width="900"><br>

upload some objects to you s3 bucket.
<img width="1380" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/4768b046-aafe-41f7-afaf-9cb5dee8460d"><br>


We can see that the bucket is private in the Permissions section:
<img width="1380" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/52ae6950-5ce6-49c5-adac-da1df583fc75">

and when trying to access an object from the bucket, by entering its url to a web browser we get access denied response:
<img width="1380" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/f619ee51-b335-4eb2-b4de-4e2119e331b3">



### 2. Create an EC2 Launch Template
Create an EC2 launch template with the following instance properties:
- AMI (Amazon Machine Image): Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2024-04-11. <br>
  <img width="600" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/ff1b006f-cdc4-4b92-bf27-05f335c61b44">
  
- Instance type: t2.micro. <br>
  <img width="600" alt="image" src=https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/9a0d66b4-b2ec-45a7-8633-15ccc6f2f5b0>
  
- Key pair: create or attach existing SSH key pair for accessing the EC2 instance. <br>
  <img width="600" alt="image" src=https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/6a7b42fc-a722-4f6b-839e-2c710248d2c0>
  
- Network settings: 
  Create security groups that allow inbound and outbound traffic on ports 22 (SSH), 80 (HTTP), 443 (HTTPS), and 5001 (Flask app port). <br>
  <img src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/f501dd2f-58db-4b08-9267-cb3fb1a1e59f" width="600" height="150"><br>
  <img src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/906ff969-8648-4f7a-9ec8-051c34831a7d" width="600" height="200"><br>
  Then Attach the security group to the EC2 instance template. <br>
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/1f5885eb-b8c7-4d6f-8f88-f04fbbb9047d">
  
- Storage (Volume): keep the default settings unchange <br>
  <img width="633" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/017a2627-85cb-4bd9-8ced-805e08ad7d47">
  
- Advanced details:
  In the User data section:
  add the commands that will run when an instance is lunched:
  change the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY enviroment variables to your credentials.
  change the S3_BUCKET_NAME, S3_IMAGE_KEY enviroment variables to fit the names you choose.
  ```
  #!/bin/bash
  sudo apt-get update
  sudo apt-get install docker.io -y
  
  sudo systemctl start docker
  sudo systemctl enable docker
  
  git clone https://github.com/edenarni/FlaskDockerEC2AutoScaleLB.git
  
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  
  sudo chmod +x /usr/local/bin/docker-compose
  
  cd FlaskDockerEC2AutoScaleLB
  
  # Create a .env file 
  cat <<EOL > .env
  # Database configuration
  DATABASE_URL=postgresql://eden:1234@postgres-db-container:5432/postgres_db
  
  # AWS S3 configuration
  AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
  AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
  S3_BUCKET_NAME=<YOUR_S3_BUCKET_NAME>
  S3_IMAGE_KEY=<YOUR_S3_IMAGE_KEY>
  
  # Flask configuration
  FLASK_APP=app.py
  FLASK_ENV=development
  EOL
  
  sudo docker-compose up --build -d
  ```
- In the IAM instance profile section:
  Create an IAM role with full access permission the S3 bucket where the image is stored.
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/38a49ed9-895a-48af-83a0-59977adee69e"> <br>

  Then Attach the IAM role to the EC2 instance template to grant the instance created from it access to the S3 bucket. <br>
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/b9969a0b-a136-4c1b-a9db-74a78713a3d5"> <br>
  This will allow the EC2 instance which the flask app is running on to access the S3 bucket.

  
- Finally, this is the template instance we created: <br>
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/467802c4-fc06-4894-9f6b-083f4c05a24e"> <br>
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/7d56690b-5694-426a-9cca-098c05959e1e">
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/5e3e7188-6b7c-4b54-a02a-a008f7d5d83d">
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/629da3e4-1430-4be9-bf55-eae1134be917">
  <img width="700" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/1bfccac2-9cb0-46c6-a21b-9400b5c292f2">

  
  
### 3. Create an Application Load Balancer
before creating the load balancer we will create a target group that the traffic will be send to, with the following configurations:

see that the Protocol:Port is HTTP:5001, this corresponds to the port that the Load Balancer will route traffic to it.

<img width="1259" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/caa395f5-0fdb-46f5-ac8c-ccceaaa0a654">

now create an application load balancer with the following configurations, and set the listenrs to listen on port 80 and route the traffic to the traget group:
<img width="1307" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/90e995fb-a084-4064-89e9-e2c44a41b4fe">
<img width="1306" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/0dfcdb1e-1312-4f03-aef2-5b8ecd17f167">
<img width="1260" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/ebcaa707-dcec-4147-87ba-a2658689e9eb">
<img width="1295" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/0fbe5822-6f8d-40fd-aa22-ffef11f2f2ca">


### 4. Create Auto Scaling Group
Specify the launch template to be the EC2 template instance we created earlier.
In the "Network" section, select the same availability zones and subnets (e.g., us-west-2a, us-west-2b, us-west-2c) you choose when creating the load balancer.
Attach the Load balancer you created.
Set the target group to the one you created earlier.
Turn on Elastic Load Balancing health checks, and set the grace health check time to 300.
set Desired capacity:2, Min desired capacity:1 , Max desired capacity:3 .
in the Automatic scaling, choose Target tracking scaling policy, we will configure the scaling policy to be based on 'Application Load Balancer request count per target', where the target group is the ones we created. 
your summry configuration should look like that:
<img width="558" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/d42ee0e6-7d12-49bd-b5cb-a4dd449acf5d">
<img width="545" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/c8e003f7-905d-42f5-9382-4f83a0df9b17">
<img width="547" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/6818d3ec-e48e-4bc3-8334-5fdd8088e138">
<img width="544" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/c7a49822-a46b-439d-8c09-fc97c1d01b09">
<img width="1423" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/5fb211ce-b661-41ae-9fc8-c6186c280f72">

we can see that 2 instances have been launched:
<img width="1509" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/7e35a65d-00fc-41e2-a652-b298803b4055">

and are healthy:
![image](https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/16a462f0-ac79-4295-b815-087841aa2afb)
<img width="1509" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/dd566aa9-f0fc-42c6-b336-ce66b87df2ae">


### 5. Access the App
Now, using the url of the load balancer we can now access our app:
![image](https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/e4a4f99b-2e98-4ed1-8111-87de0857c037)
 
![image](https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/e9c87a09-bfa4-4bf0-afb6-17694288b98d)
<img width="1482" alt="image" src="https://github.com/edenarni/FlaskDockerEC2AutoScaleLB/assets/123691333/01298e63-c411-4a3c-93cb-b8e2c165b5a5">



