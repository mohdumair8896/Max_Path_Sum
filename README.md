
# DSA problem on Google Cloud Platform 

DSA problem on Google Cloud Platform using Docker. The problem is as follows:
- A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root. The path sum of a path is the sum of the node's values in the path. Given the root of a binary tree, return the maximum path sum of any non-empty path.

- Example 1: 
- Input: root = [1,2,3]
- Output: 6
- Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.
- Example 2:
- Input: root = [-10,9,20,null,null,15,7]
- Output: 42
- Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.


## Python program to run DSA problem

Save file as max_path_sum1.py

```class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    def helper(node):
        nonlocal max_sum
        if not node:
            return 0
        # Computing the maximum path sum with highest value on the left and right
        left = max(helper(node.left), 0)
        right = max(helper(node.right), 0)
        
        # Updating the maximum path sum at the current node
        current_sum = node.val + left + right
        max_sum = max(max_sum, current_sum)
        
        # Returing the maximum path sum including the current node and one of its subtrees
        return node.val + max(left, right)
    
    max_sum = float('-inf')
    helper(root)
    return max_sum

# Function to build the tree from a list of values
def buildTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while i < len(values):
        current = queue.pop(0)
        if values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root

# Input is taken from user
input_list = input("Enter the tree values in level order, separated by commas (use 'null' for None): ").strip()
input_list = [val.strip() for val in input_list.split(',')]
input_list = [int(val) if val.lower() != 'null' else None for val in input_list]

# Building the tree
root = buildTree(input_list)

# Computing and printing the maximum path sum
print("The maximum path sum is:", maxPathSum(root))
```

**Explanation:**
- **TreeNode Class:** Represents a node in the binary tree.
- **maxPathSum Function:** Computes the maximum path sum using a helper function.
- **helper Function:** Recursively calculates the maximum path sum at each node and updates the global maximum.
- **buildTree Function:** Constructs the binary tree from a list of values.
- **Main Block:** Takes input from the user, processes it, builds the tree, and prints the maximum path sum.
## Running Tests

To execute program, run the following command

```bash
   python3 ./max_path_sum1.py
```

## Containerization the DSA problem with Docker

Save file as Dockerfile
```bash
# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /home/umair/app

# Copy the current directory contents into the container at /home/umair/app
COPY . .

# Install any needed packages specified in requirements.txt (if any)
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements to install"

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the script
CMD ["python", "./max_path_sum1.py"]
```
**Building Docker Image**
```bash
docker build -t max-path-sum1 .
```
```bash
docker run -it max-path-sum1
```
## Multi-container deployment using Docker-Compose

Save file as docker-compose.yml
```bash
version: '3.8'

services:
  app:
    build: .
    container_name: max_path_sum1
    volumes:
      - .:/home/umair/app
    depends_on:
      - db
    environment:
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_USER=postgres
      - DATABASE_PASSWORD=example
      - DATABASE_NAME=testdb

  db:
    image: postgres:13
    container_name: max_path_sum1_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: example
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Start the Docker Containers:**
```bash
docker-compose up --build
```
**Run Docker Compose:**
```bash
docker-compose up
```
This command will build the Docker image for the Python app and start both the Python app and PostgreSQL database services, linking them together as specified.


**Verify Running Containers:**
```bash
docker postgres
```
## Create requirements.txt
```bash
psycopg2-binary
```
**Update max_path_sum1.py:**
```bash
import psycopg2
import os

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    def helper(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(helper(node.left), 0)
        right = max(helper(node.right), 0)
        current_sum = node.val + left + right
        max_sum = max(max_sum, current_sum)
        return node.val + max(left, right)
    max_sum = float('-inf')
    helper(root)
    return max_sum

def buildTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while i < len(values):
        current = queue.pop(0)
        if values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            host=os.environ.get("DATABASE_HOST"),
            port=os.environ.get("DATABASE_PORT"),
            database=os.environ.get("DATABASE_NAME")
        )
        cursor = connection.cursor()
        print("Connected to the database")
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error connecting to database: {error}")

if __name__ == "__main__":
    connect_to_db()
    input_list = input("Enter the tree values in level order, separated by commas (use 'null' for None): ").strip()
    input_list = [val.strip() for val in input_list.split(',')]
    input_list = [int(val) if val.lower() != 'null' else None for val in input_list]
    root = buildTree(input_list)
    print("The maximum path sum is:", maxPathSum(root))
```
This code ensures that the program can scale the application by adding more services and handling them efficiently using Docker Compose.

## Deployment on Google Cloud Platform (GCP)

**Step 1: Setting the Environment**
- Authenticate with GCP:
 ```bash
  gcloud auth login
  ```
- Setting the GCP Project:
 ```bash
  gcloud config set project max-path-sum1
  ```
**Step 2: Containering the Application**
```bash
# Using the official Python base image
FROM python:3.9-slim

# Setting the working directory in the container
WORKDIR /home/umair/app

# Copying the current directory contents into the container at /home/umair/app
COPY . .

# Installing any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Running the script
CMD ["python", "./max_path_sum1.py"]
```
**Step 3: Building and Pushing Docker Image to Google Container Registry (GCR)**

**Building the Docker Image**
- ```bash
  docker build -t gcr.io/max_path_sum1/max-path-sum1:latest .
  ```

**Pushing the Image to GCR**
- ```bash
   docker push gcr.io/max_path_sum1/max-path-sum1:latest
  ```

**Step 4: Setting up the Google Kubernetes Engine (GKE)**

 **Creating a GKE Cluster**
- ```bash
  gcloud container clusters create max-path-sum-cluster --zone us-west1-a
  ```

 **Getting Authentication Credentials for the Cluster**
- ```bash
  gcloud container clusters get-credentials max-path-sum-cluster --zone us-west1-a
  ```

**Step 5: Deploy to GKE**

**Creating a Kubernetes Deployment**
Saved file as deployment.yaml
- ```bash
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: max-path-sum1-deployment
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: max-path-sum1
    template:
      metadata:
        labels:
          app: max-path-sum1
      spec:
        containers:
        - name: max-path-sum1
          image: gcr.io/max-path-sum1/max-path-sum1:latest
          ports:
          - containerPort: 8080
  ``` 


**Deploy to GKE**
```bash
kubectl apply -f deployment.yaml
```
**Expose the Deployment**

Saved file as service.yaml
```bash
apiVersion: v1
kind: Service
metadata:
  name: max-path-sum1-service
spec:
  type: LoadBalancer
  selector:
    app: max-path-sum1
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```
**Apply the Service Configuration**
```bash
kubectl apply -f service.yaml
```
## Step 6: Scale Using Google Compute Engine (GCE)
- Created an Instance template
  ``` bash 
  gcloud compute instance-templates create max-path-sum1-template \
    --machine-type n1-standard-1 \
    --image-family debian-9 \
    --image-project debian-cloud \
    --metadata startup-script='#!/bin/bash
      docker run gcr.io/ma-path-sum1/max-path-sum1:latest'
  ```

- Created a Managed Instance Group
  ```bash
  gcloud compute instance-groups managed create max-path-sum1-group \
    --base-instance-name max-path-sum1 \
    --template max-path-sum1-template \
    --size 3 \
    --zone us-west1-a
  ```

- Setting Up the Autoscaling
  ```bash
  gcloud compute instance-groups managed set-autoscaling max-path-sum1-group \
    --max-num-replicas 10 \
    --min-num-replicas 3 \
    --target-cpu-utilization 0.6 \
    --zone us-west1-a
  ```


# DSA problem on Google Cloud Platform 

DSA problem on Google Cloud Platform using Docker. The problem is as follows:
- A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root. The path sum of a path is the sum of the node's values in the path. Given the root of a binary tree, return the maximum path sum of any non-empty path.

- Example 1: 
- Input: root = [1,2,3]
- Output: 6
- Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.
- Example 2:
- Input: root = [-10,9,20,null,null,15,7]
- Output: 42
- Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.


## Running Tests

To execute program, run the following command

```bash
   python3 ./max_path_sum1.py
```

## Containerization the DSA problem with Docker

Save file as Dockerfile
```bash
# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /home/umair/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt (if any)
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements to install"

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the script
CMD ["python", "./max_path_sum1.py"]
```
**Building Docker Image**
```bash
docker build -t max-path-sum1 .
```
```bash
docker run -it max-path-sum1
```
## Multi-container deployment using Docker-Compose

Save file as docker-compose.yml
```bash
version: '3.8'

services:
  app:
    build: .
    container_name: max_path_sum1
    volumes:
      - .:/home/umair/app
    depends_on:
      - db
    environment:
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_USER=postgres
      - DATABASE_PASSWORD=example
      - DATABASE_NAME=testdb

  db:
    image: postgres:13
    container_name: max_path_sum1_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: example
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Start the Docker Containers:**
```bash
docker-compose up --build
```
**Run Docker Compose:**
```bash
docker-compose up
```
This command will build the Docker image for the Python app and start both the Python app and PostgreSQL database services, linking them together as specified.


**Verify Running Containers:**
```bash
docker postgres
```
## Create requirements.txt
```bash
psycopg2-binary
```
**Update max_path_sum.py:**
```bash
import psycopg2
import os

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    def helper(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(helper(node.left), 0)
        right = max(helper(node.right), 0)
        current_sum = node.val + left + right
        max_sum = max(max_sum, current_sum)
        return node.val + max(left, right)
    max_sum = float('-inf')
    helper(root)
    return max_sum

def buildTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while i < len(values):
        current = queue.pop(0)
        if values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            host=os.environ.get("DATABASE_HOST"),
            port=os.environ.get("DATABASE_PORT"),
            database=os.environ.get("DATABASE_NAME")
        )
        cursor = connection.cursor()
        print("Connected to the database")
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error connecting to database: {error}")

if __name__ == "__main__":
    connect_to_db()
    input_list = input("Enter the tree values in level order, separated by commas (use 'null' for None): ").strip()
    input_list = [val.strip() for val in input_list.split(',')]
    input_list = [int(val) if val.lower() != 'null' else None for val in input_list]
    root = buildTree(input_list)
    print("The maximum path sum is:", maxPathSum(root))
```
This code ensures that the program can scale the application by adding more services and handling them efficiently using Docker Compose.

## Deployment on Google Cloud Platform (GCP)

**Step 1: Setting the Environment**
- Authenticate with GCP:
 ```bash
  gcloud auth login
  ```
- Setting the GCP Project:
 ```bash
  gcloud config set project max-path-sum
  ```
**Step 2: Containering the Application**
```bash
# Using the official Python base image
FROM python:3.9-slim

# Setting the working directory in the container
WORKDIR /home/umair/app

# Copying the current directory contents into the container at /home/umair/app
COPY . .

# Installing any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Running the script
CMD ["python", "./max_path_sum1.py"]
```
**Step 3: Building and Pushing Docker Image to Google Container Registry (GCR)**

**Building the Docker Image**
- ```bash
  docker build -t gcr.io/max_path_sum1/max-path-sum1:latest .
  ```

**Pushing the Image to GCR**
- ```bash
   docker push gcr.io/max_path_sum1/max-path-sum1:latest
  ```

**Step 4: Setting up the Google Kubernetes Engine (GKE)**

 **Creating a GKE Cluster**
- ```bash
  gcloud container clusters create max-path-sum-cluster --zone us-west1-a
  ```

 **Getting Authentication Credentials for the Cluster**
- ```bash
  gcloud container clusters get-credentials max-path-sum-cluster --zone us-west1-a
  ```

**Step 5: Deploy to GKE**

**Creating a Kubernetes Deployment**
Saved file as deployment.yaml
- ```bash
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: max-path-sum1-deployment
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: max-path-sum1
    template:
      metadata:
        labels:
          app: max-path-sum1
      spec:
        containers:
        - name: max-path-sum1
          image: gcr.io/max-path-sum/max-path-sum1:latest
          ports:
          - containerPort: 8080
  ``` 


**Deploy to GKE**
```bash
kubectl apply -f deployment.yaml
```
**Expose the Deployment**

Saved file as service.yaml
```bash
apiVersion: v1
kind: Service
metadata:
  name: max-path-sum1-service
spec:
  type: LoadBalancer
  selector:
    app: max-path-sum1
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```
**Apply the Service Configuration**
```bash
kubectl apply -f service.yaml
```
## Step 6: Scale Using Google Compute Engine (GCE)
- Created an Instance template
  ``` bash 
  gcloud compute instance-templates create max-path-sum1-template \
    --machine-type n1-standard-1 \
    --image-family debian-9 \
    --image-project debian-cloud \
    --metadata startup-script='#!/bin/bash
      docker run gcr.io/max-path-sum/max-path-sum1:latest'
  ```

- Created a Managed Instance Group
  ```bash
  gcloud compute instance-groups managed create max-path-sum1-group \
    --base-instance-name max-path-sum1 \
    --template max-path-sum1-template \
    --size 3 \
    --zone us-west1-a
  ```

- Setting Up the Autoscaling
  ```bash
  gcloud compute instance-groups managed set-autoscaling max-path-sum1-group \
    --max-num-replicas 10 \
    --min-num-replicas 3 \
    --target-cpu-utilization 0.6 \
    --zone us-west1-a
  ```

## Monitoring and Troubleshooting

Integrated monitoring and troubleshooting into the existing Dockerized Python application deployed on GKE and monitored using Google Cloud Monitoring

```bash
import psycopg2
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxPathSum(root):
    def helper(node):
        nonlocal max_sum
        if not node:
            return 0
        left = max(helper(node.left), 0)
        right = max(helper(node.right), 0)
        current_sum = node.val + left + right
        max_sum = max(max_sum, current_sum)
        return node.val + max(left, right)

    max_sum = float('-inf')
    helper(root)
    return max_sum

def buildTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while i < len(values):
        current = queue.pop(0)
        if values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            host=os.environ.get("DATABASE_HOST"),
            port=os.environ.get("DATABASE_PORT"),
            database=os.environ.get("DATABASE_NAME")
        )
        cursor = connection.cursor()
        logging.info("Connected to the database")
        cursor.close()
        connection.close()
    except Exception as error:
        logging.error(f"Error connecting to database: {error}")

if __name__ == "__main__":
    connect_to_db()
    
    # Example: Read tree values from user input
    input_list = input("Enter the tree values in level order, separated by commas (use 'null' for None): ").strip()
    input_list = [val.strip() for val in input_list.split(',')]
    input_list = [int(val) if val.lower() != 'null' else None for val in input_list]
    
    # Build the tree
    root = buildTree(input_list)
    
    # Calculate and log the maximum path sum
    max_sum = maxPathSum(root)
    logging.info(f"The maximum path sum is: {max_sum}")
```

## Security and Cost Optimization

**Security Enhancements**

- Implemented VPC Network Isolation for GKE clusters.
- Configured IAM roles with least privilege for application services.
- Enabled encryption at rest for persistent disks and databases.
- Integrated Container Registry Vulnerability Scanning into CI/CD pipelines.

**Cost Optimization Strategies**

- Monitored and adjusted Compute Engine instance sizes based on usage patterns.
- Utilized Horizontal Pod Autoscaler (HPA) in GKE for automated pod scaling.
- Set up budgets and alerts in Google Cloud Billing to track expenditure.

# Overview

**Efficient and secure deployment of the DSA problem solution on GCP using Docker,
resulting in robust, scalable, and cost-effective cloud solutions.**
