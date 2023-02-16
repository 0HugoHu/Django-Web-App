# Django Web-App
Duke ECE 568: Engineering Robust Server Software HW1. It can be used as a template for Django web project.

⛳ This web-app assembles Uber, which lets users request, drive for, and join rides. It has three roles: Passenger, Driver, and Manager. The functionalities include:

- **Create Account**
- **Login/Logout**
- **Driver Registration**
- **Ride Selection**
- **Ride Requesting**
- **Ride Request Editing (Owner)**
- **Ride Request Viewing (Owner / Sharer)**
- **Ride Status Viewing (Driver)**
- **Ride Searching (Driver)**
- **Ride Searching (Sharer) (⚠Not yet implemented!)**
- **And some other unlist features...**

**🆒 See all Demos [here](#demo).**

![](assets/img/demo%20(6).png)

## Before All
🚫 This is my first Django project, and just for learning purpose, I did not correctly use the ```Django Authentication``` feature. **I store all passwords in PLAIN TEXT.** Please fix it yourself in ```world/models.py```:
```python
user = self.model(
            email=MyCustomUserManager.normalize_email(email_id),
            ...
            password=password,
            ...
        )
```

## Installation
### 1. Prerequisites
Install following packages and dependencies in order:
```bash
sudo apt-get install gcc g++ make valgrind
sudo apt-get install emacs screen
sudo apt-get install postgresql
sudo apt-get install python python3-pip
sudo apt-get install libpq-dev
sudo pip3 install django psycopg2 
```

Test your Django version:
```bash
$ django-admin --version
4.1.5
```

You need ```Django>4.0``` for some new features in Django. Then install these libraries:

```bash
sudo apt-get install libssl-dev libxerces-c-dev libpqxx-dev
sudo apt-get install manpages-posix-dev
```

### 2. Clone Project
Git clone my repository:
```bash
git clone https://github.com/0HugoHu/Django-web-app.git
```

Install all project-specific requirements:
```bash
cd Django-web-app/
pip3 install -r requirements.txt
```

### 3. Configure Local Database
Setup your local ```postgresql``` database:
```bash
sudo su - postgres
psql
```
Create a user, for convenience, I suggest you to choose the name of your linux logged-in username (e.g., ```abc@dce:~$```: then choose ```abc``` as your name):
```sql
CREATE abc;
ALTER USER abc CREATEDB WITH PASSWORD '$PWD'; ## replace $PWD with your password
--  exit postgres (by pressing Ctrl+D)
--  exit the su'ed shell
```
```bash
createdb $nameOfDB # replace $nameOfDB with a meaningful name for your project
```

### 4. Configure APIs and Local Variables
Edit project setting file:
```bash
cd ridesharing
emacs settings.py # or use any editor you want
```

If you want to use docker and deploy this project on web services (e.g., ```AWS EC2``` or ```AWS ECR```), add ```'*'``` to allow all hosts:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*',]
```

Change your default database to ```postgresql```:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$nameOfDB',
        'USER': '$USER',
        'PASSWORD': '$PWD',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# replace $nameOfDB with your database name, 
# $USER with your username, 
# and $PWD with your password
```

Change your timezone if you are not in Eastern Standard Time:
```python
TIME_ZONE = 'America/New_York'
```

Configure email sending service API. I'm using the ```SendGrid``` API: [SendGrid.com](https://sendgrid.com/)

You must first register your personal information on that website, and bind your sender email address. Then use the API Key generator to get your own ```$KEY```. This step is very time-consuming, please refer to other tutorials for help.
```python
SENDGRID_API_KEY = '$KEY'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

Add your sender email address:
```python
# The email you'll be sending emails from
DEFAULT_FROM_EMAIL = '$EMAIL'
# replace $EMAIL with your registered and confirmed email address
```

## Run the Server
### 1. Database Model Integrations
Django will automatically create the new table for you based on the ```world/models.py``` file. Apply this creation by:
```bash
python3 manage.py makemigrations
# or try with python3 manage.py makemigrations ridesharing
# and python3 manage.py makemigrations world
python3 manage.py migrate
```

🟥 If you have any problems creating the tables, you can do it manually by:
```bash
python3 manage.py sqlmigrate world 0001
```

This will generate ```Postgresql schema```, e.g.:
```sql
BEGIN;
##
## Create model Question
##
CREATE TABLE "polls_question" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);

COMMIT;
```
Copy and execute this schema in ```psql```, and you can check your database by (**Remember you must start your ```postgresql``` service first**):
```sql
\l ## to list all databases
\c user_info ## switch to your database
\dt ## show all tables
SELECT * from world_user; ## see all records in world_user table
q ## quit
```
### 2. Start Postgresql Service
```bash
sudo service postgresql start
```

### 3. Run Your Website Locally
```bash
python3 manage.py runserver 0:8080
```

**💠 Now enjoy this project!**

## Demo
### 1. Register
![](assets/img/demo%20(2).png)
![](assets/img/demo%20(3).png)

### 2. Login
![](assets/img/demo%20(1).png)

### 3. Home Page
![](assets/img/demo%20(4).png)

### 4. Search
![](assets/img/demo%20(5).png)
![](assets/img/demo%20(6).png)

### 5. Edit Profile
![](assets/img/demo%20(7).png)

### 6. Edit Vehicle Info
![](assets/img/demo%20(8).png)

### 7. View My Ride
![](assets/img/demo%20(11).png)

### 8. Search for Ride (Driver)
![](assets/img/demo%20(12).png)
![](assets/img/demo%20(13).png)

### 9. View Ride
![](assets/img/demo%20(14).png)
![](assets/img/demo%20(15).png)

### 10. Emails (OTP and Ride Confirmation)
![](assets/img/demo%20(16).png)
![](assets/img/demo%20(17).png)


## Contribution
**🔱 Developed by Hugo.**

Since I didn't really enroll in this course, this project is only used for self-learning. Some of this project requirements are meaningless and time-consuming for me, so I have not implemented (or just leave the interface) yet.

**Due to the limited time, I did not clean up the code. I would be glad if someone can further improve this project**

📧 If you have any questions, feel free to contact me through:
![](assets/img/demo%20(9).png)
