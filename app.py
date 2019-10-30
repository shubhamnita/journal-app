# Import modules
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import datetime
import getpass
import hashlib
import json
import os
import sys
import time


user_credentials = 'user_records.txt'
journal_content_file = "journal_details.txt"

admin_password = "paSS!#2019admin" # This is input in the form of a string
password = admin_password.encode() # Convert to type bytes
salt = b'\x1eC\xcdm\xb9\x06\xfbK\x8an&\xe6\x98\x1cx\xf4' 
kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=salt,
	iterations=100000,
	backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))    # Key used for journal content encryption

def encrypt_content(journal_content_file):
	with open(journal_content_file, 'rb') as f:
		data = f.read()
		
	if len(data)>0:
		fernet = Fernet(key)
		encrypted = fernet.encrypt(data)
		with open(journal_content_file, 'wb') as f:
			f.write(encrypted)
	

def decrypt_content(journal_content_file):
	with open(journal_content_file, 'rb') as f:
		data = f.read()
		
	if len(data)>0:
		#encrypt_content(journal_content_file)	
		fernet = Fernet(key)
		encrypted = fernet.decrypt(data)
		with open(journal_content_file, 'wb') as f:
			f.write(encrypted)
	

def process_file():
	user_names = []
	passwords = []
	
	try:
		file_conn = open(user_credentials)
		data = file_conn.readlines()

		for i in range(len(data)): 
			if i%2 == 0:
				user_names.append(data[i][:-1])
			else:
				passwords.append(data[i][:-1])
			
		file_conn.close()
	except:
		sys.exit('An internal error occured ! There was a problem reading the file!')
		
	return user_names, passwords


def login():
	user_names,passwords = process_file()
	user_try =0
	y=5
	while user_try < y:
		username = input("Username: ")
		if not len(username) > 0:
			print("Username can't be blank")
			user_try +=1
		elif username not in user_names:
			print("Invalid username !")
			user_try +=1
		else:
			break
	if user_try == y:
		print("Options: register | login | exit")
		return
	pass_try = 0 
	x = 3
	
	while pass_try < x:
		password = getpass.getpass('Please Enter Password: ')
		if not len(password) > 0:
			print("Password can't be blank")
		salt = b'\x94\x06\\6>AY\xfa\x0b\x80\x97\x98%>\xcd\xf2'
		user_input = hashlib.sha224(salt + password.encode()).hexdigest()
		if user_input != passwords[user_names.index(username)]:		
			pass_try += 1
			print('Incorrect Password, ' + str(x-pass_try) + ' more attemts left\n')
		else:
			session(username)
			pass_try = x+1
			
	if pass_try == x:
		print('Incorrect Password \n Options: register | login | exit')



# Register
def register():
	user_names,passwords = process_file()
	while True:
		username = input("New username: ")
		if not len(username) > 0:
			print("Username can't be blank")
			continue
		elif username in user_names:
			print("Username already taken")
		else:
			break
	while True:
		password = getpass.getpass('New Password: ')
		if not len(password) > 0:
			print("Password can't be blank")
			continue
		else:
			break
	print("Creating account...")
	salt = b'\x94\x06\\6>AY\xfa\x0b\x80\x97\x98%>\xcd\xf2' 
	password = hashlib.sha224(salt + password.encode()).hexdigest()
	try:
		file_conn = open(user_credentials, 'a')
		file_conn.write(username + '\n' + password + '\n')
		file_conn.close()
	except:
		sys.exit('An internal error occured ! There was a problem reading the file!')
	print("Account has been created \n Options: register | login | exit")


def editJournal(username):
	journal_content_file = username + "_journal_details.txt"
	entry = input(username + " > Enter new entry: ")
	data ={}
	if os.path.isfile(journal_content_file) ==False:
		open(journal_content_file,'a').close()

	with open(journal_content_file, 'r+') as f:
		f.seek(0,os.SEEK_END)    #Go to the end of file
		if f.tell():             #Check if file is not empty
			f.seek(0, 0)
			data = json.load(f)
		else:
			f.write(json.dumps(data))

	with open(journal_content_file,'w') as f:	
		if username not in data:		
			data[username] = []
		if len(data[username]) >50 :
			data[username].remove(data[username][0])
		data[username].append(str(datetime.datetime.now()) + ' - ' + entry) 
		json.dump(data,f)			 
	print("New Entry created \n Options: list | create | logout")


def viewJournal(username):
	journal_content_file = username + "_journal_details.txt"
	if os.path.isfile(journal_content_file) ==False:
		open(journal_content_file,'a').close()
	data={}
	with open(journal_content_file, 'r+') as f:
		f.seek(0,os.SEEK_END)    #Go to the end of file
		if f.tell():             #Check if file is not empty
			f.seek(0, 0)
			data = json.load(f)
		else:
			f.write(json.dumps(data))

	if username in data:
		for entry in data[username]:	
			print(str(entry))
	else:
		print("Empty journal")
	
	print("Options: list | create | logout")


def session(username):
	print("Welcome to your account " + username)
	
	journal_content_file = username + "_journal_details.txt"
	if os.path.isfile(journal_content_file) ==False:
		open(journal_content_file,'a').close()

	decrypt_content(journal_content_file)
	
	print("Options: list | create | logout")
	while True:
		option = input(username + " > ")
		if option == "logout":
			print("Logging out...\n Options: register | login | exit")
			encrypt_content(journal_content_file)
			break
		elif option == "create":
			editJournal(username)
		elif option == "list":
			viewJournal(username)
		else:
			print(option + " is not an option")


if __name__ == "__main__":
# On start
	print("Welcome to the system. Please register or login.")
	print("Options: register | login | exit")
	while True:
		option = input("> ")
		if option == "login":
			login()
		elif option == "register":
			register()
		elif option == "exit":
			break
		else:
			print(option + " is not an option")

	# On exit
	print("Shutting down...")
	time.sleep(1)
