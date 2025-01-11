![Python](https://img.shields.io/badge/python-v3.13-blue.svg)
![Django](https://img.shields.io/badge/django-v5.1.4-yellow.svg)
![NGINX](https://img.shields.io/badge/NGINX-v1.27.3-default.svg)
![Docker](https://img.shields.io/badge/Docker-v27.4-00008B.svg)
![Postgres](https://img.shields.io/badge/Postgres-v17-3268a8.svg)

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
- **docker compose up -d --build**
  - Builds the containers that are in the current compose.yaml file and run the project on localhost:1337
  - Using the optional -d flag it will run the container in the background until you use: docker compose down -v.
    
- **docker compose down -v**
  - Stops the running containers and volumes associated with them

- **docker compose exec django-web python manage.py migrate --noinput**
  - Runs a migration
 
- **docker compose exec django-web python manage.py createsuperuser**
  - Prompts for a username and email to create a admin user
 
- **docker compose logs name**
  - Replace name with the name of the service: django-web, db, nginx 
 
- **docker image ls**
  - Lists all docker images
&nbsp;

## Git & GitHub:
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

- **git switch name**
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

# How to submit Pull Request:

# FAQ

