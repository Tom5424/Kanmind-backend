# Kanmind (backend)


## Table of Contents


1. [About the Project](#about-the-project)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [API Endpoints](#api-endpoints)


## About the Project
The Kanmind backend is a robust REST API built with Django and Django REST Framework (DRF). It supports functionalities such as user registration, login, board and task management like a kanban board.


## Technologies

- Python (Version 3.12.4)
- Django (Version 5.2.4)
- Django REST Framework (Version 3.16.0)

  
## Prerequisites

  - Python
  - Django
  - Django REST Framework
  - pip


## Installation


1 **Clone the repository:**
  ```
  git clone https://github.com/Tom5424/Kanmind-backend.git .
  ```


2 **Create a virtual environment:**
  ```
  python -m venv env
  ```
  activate the virtual environment with ``` env\Scripts\activate ```
  


3 **Install dependencies:**
  ```
  pip install -r requirements.txt
  ``` 


4 **Start the Project:**
  ```
  py manage.py runserver
  ```


## API Endpoints


#### Authentification Endpoints:


- METHOD POST ``` api/registration/ ``` Registers a new user

- METHOD POST ``` api/login/ ``` Login a user


#### Board Enpoints:


 - METHOD GET, POST ``` api/boards/ ``` Return a list of boards or creats a new board

 - METHOD GET, PATCH, DELETE ``` api/boards/{board_id}/ ``` Return a detail view from the board or updates the board or delete the board based on the id 

 - METHOD GET ``` api/email-check/ ``` Return a registered user that email exist
  

#### Task Enpoints:


 - METHOD GET ``` api/tasks/assigned-to-me/ ``` Return all tasks that assigned the current authenticated user as assignee 

 - METHOD GET ``` api/tasks/reviewing/ ``` Return all tasks that assigned the current authenticated user as reviewer 

 - METHOD POST ``` api/tasks/ ``` Creates a new task inside a board

 - METHOD PATCH, DELETE ``` /api/tasks/{task_id}/ ``` Updates or delete a existing task based on the id

 - METHOD GET, POST ``` /api/tasks/{task_id}/comments/ ``` Creates or list comments based on the id

 - METHOD DELETE ``` /api/tasks/{task_id}/comments/{comment_id}/ ``` Deletes a comment based on the task_id and comment_id
