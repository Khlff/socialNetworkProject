## SocialNetwork
### This is an API service written in Django using the `rest_framework` library. It allows you to create new users, add other users as friends, delete, view status, and so on.

## Installation
### To install the application, you need to clone the repository:
```
git clone https://github.com/Khlff/socialNetworkProject.git
cd socialNetworkProject
```
          
* ### Launching locally:
  ```
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py runserver
  ```
  The application will be available at http://localhost:8000/api/v1/
* ### In Docker container:
  ```
  docker-compose up -d
  ```
  The application will be available at http://0.0.0.0:8000/api/v1/

###  Examples of API calls for various endpoints:
* ### 
    POST http://localhost:8080/api/v1/user
    json {
        "username": "Ivan",
        "id": 324235
    }
*  ###
    POST http://localhost:8080/api/v1/user/12345/request?recipientId=324235
* ###
    GET http://localhost:8080/api/v1/user/324235/requests
* ###
    DELETE http://localhost:8080/api/v1/user/12345/friend/67890
* ###
    PUT http://localhost:8080/api/v1/user/67890/arequest?senderId=12345&status=accepted
* ###
    GET http://localhost:8080/api/v1/user/12345/friends
* ###
    GET http://localhost:8080/api/v1/user/12345/friend?friendId=67890

###  Made by Nikita Khlopunov
