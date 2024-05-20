# Deploying Containerized Flask PostgreSQL App on AWS EC2

## Setup Steps

### 1. Launch an EC2 Instance

- Launch a new EC2 instance using the Ubuntu 20.04 AMI (Amazon Machine Image) with the appropriate instance type and storage options.
- Configure security groups to allow inbound traffic on ports 22 (SSH), 80 (HTTP), 443 (HTTPS), and 5001 (Flask app port).
- Create SSH key pair for accessing the EC2 instance.

### 2. Configure IAM Role

- Create an IAM role with permissions to access the S3 bucket where your images are stored.
- Attach the IAM role to the EC2 instance to grant it access to the S3 bucket.

### 3. Connect to the EC2 Instance

- Connect by click on the "Connect" button.

### 4. Install Docker and Docker Compose

- Follow the instructions in this [guide](https://tejaksha-k.medium.com/how-to-install-docker-and-docker-compose-to-ubuntu-20-04-azure-vm-and-aws-ec2-instances-72a498755c15) to install Docker and Docker Compose on the EC2 instance.

### 5. Clone the Project Repository

- Clone the repository containing the Flask PostgreSQL app onto the EC2 instance.
  ```bash
  git clone https://github.com/edenarni/FlaskDockerEC2AutoScaleLB.git
  cd FlaskDockerEC2AutoScaleLB
  ```

### 6. Run Docker Compose

- Once inside the project directory, use Docker Compose to build and run the Docker containers.
  ```bash
  sudo docker-compose up --build
  ```

### 7. Access the App

- After the Docker containers have started, you can access the Flask app by navigating to `http://your-ec2-public-ip:5001` in your web browser.


