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

## Setup instructions
Below are steps to follow:
1. Open cli, navigate to your project folder and clone the project: <br/>
         `git clone https://github.com/KenThumi/defco_fuelling.git`
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
asgiref==3.4.1<br>
backports.zoneinfo==0.2.1<br>
certifi==2021.10.8<br>
cloudinary==1.28.0<br>
config==0.5.1<br>
Deprecated==1.2.13<br>
dj-database-url==0.5.0<br>
Django==4.0.1<br>
django-appconf==1.0.5<br>
django-heroku==0.3.1<br>
django-redis==5.2.0<br>
django-select2==7.10.0<br>
django-simple-autocomplete==1.11<br>
gunicorn==20.1.0<br>
packaging==21.3<br>
Pillow==9.0.1<br>
psycopg2==2.9.3<br>
pyparsing==3.0.7<br>
python-decouple==3.5<br>
pytz==2022.1<br>
qrcode==7.3.1<br>
redis==4.1.4<br>
six==1.16.0<br>
sqlparse==0.4.2<br>
urllib3==1.26.8<br>
whitenoise==6.1.0<br>
wrapt==1.13.3
 

## License info
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2022 © Fuel Tracking and Monitoring Application
