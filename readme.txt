# Journal App

A terminal application to store personal journal log with user management

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.6
cryptography [Python Package]
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
1. Install Python from official python documentation.
2. Install pip if not already done.
3. Install python packages using below command:
      "pip install -r requirements.txt"
```


## Running the application

Plese execute the below command to run the application::
	python app.py


### Break down into end to end tests

********* Please dont use ctrl+c or any other terminal command to exit the application . Please use logout to logout from your account
			and then use exit command to terminate the application.
```
After execution the application will show three options : Login |register |exit

1. Exit : to exit the application.

2. Register: User will get an prompt for username and password . If the username is distinct and all the checks were 						succesful, account will be created.

3. Login: User will get an prompt for username and password . If both are correct then login will be successful . After it 				user will get an prompt.
			------> create | list | logout <----- 	

		logout: Application will logout the user.
		list : It will show the user personal journal entry.
		create : It will prompt for new entry from user . Newer entry after 50 should replace the oldest entry.

**** User will not be able to see his journal records without login[Not from any explorer] and user credenttials (username & password) since all the data will be stored in encrypted files.

```

## Codebase Intro:

	user_records.txt -> Username and hash password will be stored here.
	{username}_journal_details.txt -> This will be created after first login of user. Data will be stored encryptically .
	app.py -> This contains different functions [register,login etc.]

## Authors

* **Shubham Kumar** 


