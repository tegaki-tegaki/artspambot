# artspambot

1. replace all the <YOUR_*> strings in artspambot.py with your appropriate keys, usernames, secrets...
1. ensure postgres backend database is running & available
  - create database `draws`
  - role `artspambot` exists, also set password in Makefile env
1. ensure your python is set up
  - python version 3.5 or above
  - all the required libraries installed:
    - shutil
    - pytumblr # https://github.com/jabbalaci/pytumblr.git
    - tweepy
    - ntpath
    - requests
    - requests_toolbelt
    - psycopg2
1. run make

## optional
install the systemd service & timer
1. make -C systemd

## todo
1. move all the <YOUR_*> strings into a single place... configuration file?
1. sqllite db maybe? so 'setting up the db' becomes less of a hassle for most
1. requirements.txt or some vendoring + virtualenv for python (or docker?)
