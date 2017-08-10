# artspambot

## READ THIS FIRST (important tidbits)
- when things go wrong, the artspambot may very well _spam_ your social media outlets. If you have no fans & followers however, you have nothing to lose! (or rather, no followers to disappoint / spam)
- when I made this, i made it for myself... so it's not guaranteed to work for others, and I _know_ there's work to be done before this becomes user friendly!... the code comes as-is.
- swapping out postgres for sqlite is currently an exercise to the reader! (note. it's _most_ likely easier to swap out postgres than to do the whole postgres + flyway setup described here... YMMV).

## how to run the bot!

1. replace all the <YOUR_*> strings in artspambot.py with your appropriate keys, usernames, secrets...
1. ensure postgres backend database is running & available
    - download flyway https://flywaydb.org/
    - download postgres
    - copy `flyway.conf.template` into `flyway.conf`, and fill in passwords, secrets...etc
    - run `flyway migrate` inside the postgres directory ()
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
1. sqlite db maybe? so 'setting up the db' becomes less of a hassle for most
1. requirements.txt or some vendoring + virtualenv for python (or docker?)
