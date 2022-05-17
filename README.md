# Fuel Tracking and Monitoring Application (FTMA)


## Description
Welcome to this FTMA. FTMA is a web-based application that can be used to automate fuel record keeping at all the DEFCO fuelling points. It will enable DEFCO fuel point attendants to easily verify ownership of the vehicles drawing fuel. 
The application is able to generate relevant fuelling records for both client and management. This way, fuelling points that require replenishment can be identified on time. Additionally, FTMA offers an engagement platform whereby clients can offer reviews on various aspects. 
Ultimately, FTMA will enable DEFCO management to make more timely decisions based on information acquired through the application and therefore assist in real-time management of the fuelling points.

## Author
- [Kenneth Thumi](https://github.com/KenThumi)

## Contact
Email:kenthumi@gmail.com

## Responsiveness
The website is adaptable to any screen size.

## API Endpoints
1. https://ken-capstone.herokuapp.com/api/tasks/ :This endpoint returns all tasks details

## Mock Up Design
Mock up [link](https://www.figma.com/file/ukZI7jUQzfQIzQjFHViQMu/Capstone?node-id=0%3A1)


## Setup instructions
Below are steps to follow:
1. Open cli, navigate to your project folder and clone the project: <br/>
         `git clone https://github.com/KenThumi/tasking.git`
2. Install python, preferably python3.
3. Create a virtual environment: <br/>
         `python3 -m venv virtual`
4. To activate the virtual environment run:<br/>
         `source virtual/bin/activate`
5. Now, in the virtual environment, install Flask to the project using the following command:<br/>
         `pip install django`
6. Install dependencies that dont come with flask above:<br/>
         `pip install -r requirements.txt` 
7. Install postgres (Linux-Ubuntu).  
        `sudo apt-get update` <br/>
        `sudo apt-get install postgresql postgresql-contrib libpq-dev` <br>  
 Create our own superuser role to connect to the server. <br>
        `sudo service postgresql start` <br>
        `sudo -u postgres createuser --superuser $USER` <br>
        `sudo -u postgres createdb $USER` <br>  
 To save your history, navigate to your home directory and enter the following command to create the .psql_history  <br>
        `touch .psql_history`  <br>
 Connect to the postgres server by typing <br>
        `psql` <br>  
 Create your db. <br>
        `#  CREATE DATABASE your_db;` <br>  
 In your `setting.py` file edit `DATABASE` as below:<br>
            `DATABASES = {`   
                        `'default': {`  
                            `'ENGINE': 'django.db.backends.postgresql',`  
                            `'NAME': 'your_db',`  
                            `'USER': 'username',`  
                            `'PASSWORD':'password',`  
                        `}`  
                    `}`
        <br>  
 Put your role `username` (computer account name in this case) , role `password `and `your_db`.  
 Run below cli command, inside project folder, to set up the db with our tables: <br/>
            `python3 manage.py migrate`  
8. Set up email configurations inside `setting.py`:   
                `EMAIL_USE_TLS = True`  
                `EMAIL_HOST = 'smtp.gmail.com'`  
                `EMAIL_PORT = 587`  
                `EMAIL_HOST_USER = 'your email'`  
                `EMAIL_HOST_PASSWORD = 'your pwd' `  
    

9. Inside the same folder,  type following commands to start the application:<br/>
            `python3 manage.py runserver`  
10. Open browser and input `http://127.0.0.1:8000`
11. To edit, use IDE of your choice to work with the project, e.g VsCode, Sublime text ,etc.

## Technologies Used
In this project, below is a list of technologies used:
- [Python version 3](https://www.python.org/)
- Django
- HTML
- CSS

## Dependencies
Below are all dependencies for this application: <br>
asgiref==3.3.4  
beautifulsoup4==4.9.3  
certifi==2020.12.5  
Django==3.2.3  
django-bootstrap4==3.0.1  
django-mathfilters==1.0.0  
djangorestframework==3.12.4  
psycopg2==2.8.6  
python-decouple==3.4  
pytz==2021.1  
six==1.16.0  
soupsieve==2.2.1  
sqlparse==0.4.1  
urllib3==1.26.5  

## License info
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2021 © Tasking Application
