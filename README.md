![Python](https://img.shields.io/badge/python-v3.13-blue.svg)
![Django](https://img.shields.io/badge/django-v5.1.4-yellow.svg)
![NGINX](https://img.shields.io/badge/NGINX-v1.27.3-default.svg)
![Docker](https://img.shields.io/badge/Docker-v27.4-00008B.svg)
![Postgres](https://img.shields.io/badge/Postgres-v17-3268a8.svg)

# Table of Contents  

1. [File Structure](#file-structure)
2. [List of Commands](#list-of-commands)  
   2.1.  [Docker](#docker)  
   2.2.  [PSQL](#psql)  
   2.3.  [Git](#git--github)  
4. [How to submit pull request](#how-to-submit-pull-request)
5. [FAQ](#faq)
   
# File Structure:

### Repository Folder:
![image](https://github.com/user-attachments/assets/2bc12f6e-45c1-443e-a1ad-3b5b4b1cd74b)
- nginx-1.27.3 [The folder that contains NGINX]
- toDo [The toDo application folder]
- toDoList [The django project folder]
- db.sqlite3 [Local database django uses]
- manage.py [file used to run the django project]
### toDo app Folder:
![image](https://github.com/user-attachments/assets/0b3b28ec-9a55-47d1-b1ce-c50221db51de)
### django Project Folder:
![image](https://github.com/user-attachments/assets/0879f96a-438c-47eb-afd2-fe38bc7f5395)


# List of Commands:

## Docker:
- **docker compose up --build** OR **docker-compose up --build**
  - Builds the containers that are in the current compose.yaml file and run the project on localhost:1337
  - Using the --build flag will create a fresh build
  - Using the optional -d flag it will run the container in the background until you use: docker-compose down -v
    
- **docker compose down -v** OR **docker-compose down -v**
  - Stops the running containers and volumes associated with them
 
**_Any docker compose exec command will not run unless the container is running_**  
**_The docker compose VS docker-compose seems to be a OS specific problem please use them interchangeably if you have issues_**

- **docker compose exec django-web python manage.py migrate --noinput**
  - Runs a migration
 
- **docker compose exec django-web python manage.py createsuperuser**
  - Prompts for a username and email to create an admin user
 
- **docker compose logs name**
  - Replace the name with the name of the service: django-web, db, nginx 
 
- **docker image ls**
  - Lists all docker images
 
- **docker exec -it django-docker bash**
  - Creates an interactive bash shell that is running in the container
  - To exit this bash terminal use the command 'exit'
![image](https://github.com/user-attachments/assets/4e614cf1-0d2e-4fcd-8e8e-adc396aea569)
 
&nbsp;

## PSQL:
- **\l**
  - Lists the databases
![image](https://github.com/user-attachments/assets/8b07c240-6f7b-41eb-9607-1d52af3a4148)

- **\c**
  - Checks the connection to the db and prints the current user
![image](https://github.com/user-attachments/assets/78fa1170-3b74-4c02-ba2a-85b5874ca399)

- **\dt**
  - Shows all relations
![image](https://github.com/user-attachments/assets/8fc36fd0-9331-47f4-a00e-aec231049369)

- **\q**
  - Quit the PSQL console
![image](https://github.com/user-attachments/assets/7a39d42f-2f36-4d3c-996b-49fbb9bb0ce9)

## Git & GitHub:

- **git config --global core.autocrlf input**
  - Sets line endings to be LF or Unix standard

- **git fetch**
  - Command to essentially "refresh" and check if there are any changes in the remote repo

- **git pull**
  - Attempts to update your local branch with what is on the remote branch, fetch to refresh and pull to update
  - If done correctly, you should receive "Already up to date." or it will pull the changes without error.
![image](https://github.com/user-attachments/assets/07808722-7b21-4ca2-bf9c-4be5b43ec1b7)

- **git branch**
  - Shows all the local branches available | ___The current branch is highlighted in green with a *___
![image](https://github.com/user-attachments/assets/7d578930-cda5-4a03-9f2b-7c6ace3b28c7)
  - Adding an -a flag will show all branches, local and remote

- **git branch name**
  - Creates a branch with the given name (on your local repo), if successful no message will popup
![image](https://github.com/user-attachments/assets/8fc28817-c3a1-4703-b3c4-79fa7301506f)

- **git checkout name**
  - This will switch to the branch with whatever name is inserted after switch.
![image](https://github.com/user-attachments/assets/ca46766a-21f0-4e54-b3ed-7a138b000496)

- **git add .**
  - Add all files in your directory to the repo (as long as they are not in .gitignore)

- **git commit -a -m "message"**
  - Create a commit that includes all your changes

- **git push**
  - Attempts to upload the code in the local branch you are in, to the remote branch associated on GitHub.
  - If successful you will get a message saying your files were pushed with no errors.

# How to run the project:

#### First, launch Docker Desktop and make sure it's running.

#### Second, go to terminal and make sure you are in the repository directory.  
![image](https://github.com/user-attachments/assets/9a385b41-01e8-4644-892c-efd8353c89d9)

#### Third run the command: docker compose up --build (or use docker-compose with the dash)
![image](https://github.com/user-attachments/assets/aeedd436-a0ec-45bd-b61f-75b82151cb08)  
![image](https://github.com/user-attachments/assets/6ca1a55f-ed52-410f-ba06-e98a97cb572e)

#### **_To stop running the project use CTRL+C (or CMD+C for Mac) then use: docker compose down -v_**  
![image](https://github.com/user-attachments/assets/17e3333b-0a9c-4a17-928d-e7d1379af5bf)


# How to submit pull request:

#### First, make sure all your files are saved.
#### Second, make sure you are in the repository directory.  
![image](https://github.com/user-attachments/assets/9a385b41-01e8-4644-892c-efd8353c89d9)

#### If you aren't already in a new branch, please create one:  
![image](https://github.com/user-attachments/assets/eabd54f5-abcb-4d0d-9ccf-c8a309ae4f4d)

#### Then switch to the new branch:  
![image](https://github.com/user-attachments/assets/51bcc6c1-267f-4d70-8a15-ec8276d5fa71)

#### Add your code, commit the changes and then push:  
![image](https://github.com/user-attachments/assets/2c605c77-e13f-464b-a802-966915a5d2ff)

#### You should see this message on the GitHub page after you push:  
![image](https://github.com/user-attachments/assets/61a61f9c-54d0-4250-b650-ecebcbb4e85b)
#### If not click on the branch selector and choose the branch you pushed to:  
![image](https://github.com/user-attachments/assets/8ac84779-21f7-4160-8bc1-f1ef72e67f7c)

#### Click on "Compare & Pull Request"
#### This will bring you to a page similar to this:  
![image](https://github.com/user-attachments/assets/c3d1e867-7001-4bf8-ad5d-58cba14308b3)

#### From here click on the reviewer's gear icon to add the Product Manager:  
![image](https://github.com/user-attachments/assets/ec2018d9-4a9c-4bdb-9564-9a2e8250a724)

#### Add a description if you'd like then hit "Create Pull Request":  
![image](https://github.com/user-attachments/assets/e70250ce-d426-499c-8c3d-f7a5ade095dc)

#### You'll see this if you have no merge conflicts:  
![image](https://github.com/user-attachments/assets/49f79afc-f35d-404e-87a7-56eb0a3d8f51)

#### Once you're done the PM will review your code and merge it to the main branch.

#### After the pull request is approved and merged, you can do
- **git switch main**
- **git pull**
#### to update your main branch with the updated code


# FAQ

If you recieve an error like this when running docker compose up --build:  
![image](https://github.com/user-attachments/assets/a9a1f501-7d66-4af8-adb4-dc1bc949d5cb)
Run:
- docker compose down -v
- docker compose up --build

If you get this:
![image](https://github.com/user-attachments/assets/e16c0c33-5f6f-4840-a414-24666a54a497)
Or this:
![image](https://github.com/user-attachments/assets/5783e301-885f-4c24-b2f4-644b63a6cd3d)

Make sure Docker Desktop is running, if it is, restart and try again.
