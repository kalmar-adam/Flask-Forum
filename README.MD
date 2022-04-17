# Flask-Forum

This is a simple forum made with Python Flask and it uses SQLite3.

## Install

You need install Python from python.org first. Then clone this repository to your computer. Navigate to the source files and install depencies with these commands.:

You will need pipenv module to install depencies:
- pip install pipenv

Now depencies can be installed with this command:
- pipenv install

## Start Forum

Before you start the webserver, you have to create the database:
- pipenv run _createDB.py

IMPORTANT: _createDB.py will create database only. It will not reset its content. If you would like to reset, delete the database file and run pipenv run _createDB.py again.

After creating database the server is ready to start:
- pipenv run app.py

## What can you do on this?

- Registration and login

As a (logged in) simple user you can.:

- Write comment in topics
- Change your password

As an admin you can.:

- What simple users can do
- Ban users (they will unable to comment) and unban them
- Create, delete and renaming topics (cascade relationship between comment and topic table)
