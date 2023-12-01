
# Vendor Management System

Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.



## How to Install and Run the Project

### System Requirements -

[Python 3.10.12](https://www.python.org/downloads/) or greater should be installed in your system for running python files.

If you are working on ubuntu then there is no need to install python explicitly. Python is already installed in ubuntu.

Open Terminal / Command Prompt in your system after that make a new directory in your desired location using the command -

```bash
$ mkdir Fatmug_Designs
$ cd Fatmug_Designs
```

In Fatmug_Designs directory create a Python Virtual Environment.

Run the below command to install, create and activate python virtual environment.

#### For Windows operating system -
```bash
$ pip install virtualenv
$ virtualenv venv
$ .\venv\Scripts\activate
```

#### For Ubuntu (Linux) operating system -
```bash
$ pip install virtualenv
$ python3 -m venv venv
$ source venv/bin/activate
```
Where, venv is the name of virtual environment created.

After that, a namespace _(venv)_ is shown in the beginning of command line denoting that your virtual environment is activated successfully.
```bash
(venv) <YOUR_SYSTEM_NAME> :~
```

Clone the project's repository in your local system by running the command-
```bash
$ git clone https://github.com/KrishnakantSinghal/fatmug-designs.git
```

Jump into the directory of the cloned project by running the following commands-
```bash
$ cd fatmug-designs/
$ cd fatmug_designs/
```

Now, install the requirements for the project by running the following command -
```bash
$ pip install -r requirements.txt
```

All the requirements are installing for the project, it will take __15 to 30 seconds__ to install all the requirements, depends on the internet connection speed and system hardware.

After successfully installation of the requirements run the below command to create database and tables structure to store vendor's information -

```bash
$ python3 manage.py migrate
```

It will take __5 to 10 seconds__ for complete execution, depends on system hardware.

After successfully running the migrations, create an Admin User / Super User to manage the platform by running the below command -
```bash
$ python3 manage.py createsuperuser
```

Enter the required details to create admin -
```bash
Username: admin
Email address: admin@admin.com
Password: admin
Password (again): admin
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
```

Press Enter after entering one detail at a time.

Email is not compulsary, you can leave this blank by pressing enter.

Password may not visible by entering because this is a crucial detail. Enter the password carefully, it should match Password (again).

Project set up completed !!

Now, import the collection file in postman for managing APIs endpoints.
Collection file is - _fatmug_Designs.postman_collection.json_.

