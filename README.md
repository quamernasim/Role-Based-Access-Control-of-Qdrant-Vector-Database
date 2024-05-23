# Role-Based-Access-Control-of-Qdrant-Vector-Database

Exploring Role-Based Access Control (RBAC) in Qdrant Vector Database for granular access control of data.

## Introduction
Qdrant Vector Database has introduced a new feature called Role-Based Access Control (RBAC) in its latest release. This feature allows to limit the access of users to the data stored in the database. This feature is useful in scenarios where the data stored in the database is sensitive and should only be accessed by authorized users.

In this repository, we will explore how to set up Role-Based Access Control in Qdrant Vector Database and how to use it to limit the access of users in several security scenarios.

## Installation
```
sudo apt-get update
sudo apt install docker
docker pull qdrant/qdrant
```

The above commands will install Docker and pull the Qdrant Vector Database image from Docker Hub. We will be using Docker to run the Qdrant Vector Database in a container.

## Configuration
The configuration file for the Qdrant Vector Database is config.yaml. This file contains the configuration settings for the database, including the RBAC settings. The RBAC settings in the configuration file are as follows:
```
service:
  api_key: {your_API_key}
  jwt_rbac: true
```

## Usage
To run the Qdrant Vector Database in a container, use the following command:
```
docker run -p 6333:6333 -v /home/quamer23nasim38/Role-Based-Access-Control-of-Qdrant-Vector-Database/:/qdrant/storage -v /home/quamer23nasim38/Role-Based-Access-Control-of-Qdrant-Vector-Database/config.yaml:/qdrant/config/config.yaml qdrant/qdrant
```

The above command will run the Qdrant Vector Database in a container and expose the port 6333 for communication. It will also mount the storage and configuration files from the host machine to the container. Note that config.yaml is the configuration file for the Qdrant Vector Database and is a must-have file enabling RBAC. Without this file, the RBAC feature will not work.

## Notebooks
The notebook, named `Role-Based-Access-Control-of-Qdrant-Vector-Database.ipynb`, contains the code snippets for setting up Role-Based Access Control in Qdrant Vector Database and using it to limit the access of users in several security scenarios. The notebook is divided into several sections, each corresponding to a security scenario.

## Security Scenarios
1. **Scenario 1:** Limiting Access with JWT Tokens
2. **Scenario 2:** Limiting User Global Access to Read-Only
3. **Scenario 3:** Giving User Global Access to Manage
4. **Scenario 4:** Limiting User Access to Specific Collections With Read-Only
5. **Scenario 5:** Limiting User Access to Specific Collections With Read-Write
6. **Scenario 6:** Limiting User Access to Particular Collection With Read-Only and Another Collection With Read-Write
7. **Scenario 7:** Limiting User Access to Specific Documents in a Collection
8. **Scenario 8:** Limiting User Access to Specific Page of Specific Document in a Collection

You can add more security scenarios based on your requirements.

## Conclusion
Role-Based Access Control (RBAC) in Qdrant Vector Database is a powerful feature that allows granular access control of data. By setting up RBAC, you can limit the access of users to specific collections, documents, and even specific pages of documents. This feature is useful in scenarios where the data stored in the database is sensitive and should only be accessed by authorized users.
