#!/usr/bin/python3.6

##########################################################################
# this bot currently does twitter, tumblr and pinterest
##########################################################################

import os
import shutil
import pytumblr  # https://github.com/jabbalaci/pytumblr.git
import tweepy # twitter
import ntpath
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder # pinterest
import psycopg2

SERVE_DIR = os.path.expanduser('~') + '/draws/distribute'

PG_PASSWORD = str(os.environ['NEWDRAWS_PG_PASSWORD'])
CONN_STRING = 'dbname=draws ' + \
    'user=artspambot ' + \
    'host=localhost ' + \
    f'password={PG_PASSWORD} ' + \
    'port=5432 '

############# twitter ##################

consumer_key="<YOUR_CONSUMER_KEY>"
consumer_secret="<YOUR_CONSUMER_SECRET>"
access_token="<YOUR_ACCESS_TOKEN>"
access_token_secret="<YOUR_ACCESS_TOKEN_SECRET>"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

############# tumblr ##################

client = pytumblr.TumblrRestClient(
    '<YOUR_TUMBLR_SECRETS>',
    '<YOUR_TUMBLR_SECRETS>',
    '<YOUR_TUMBLR_SECRETS>',
    '<YOUR_TUMBLR_SECRETS>'
)
 # e.g. for suchdeviant.tumblr.com, suchdeviant is the identifier
 blog_identifier = "<YOUR_BLOG_IDENTIFIER>"

############# pinterest ################

PINTEREST_API_TOKEN="<YOUR_PINTEREST_API_TOKEN>"

##################################

# script assumes CWD = the distribution dir!
rootfiles = os.listdir('.')

# 1. fetch draws that have upload_state = not_uploaded
# 2. upload the draw to that upload_domain
# 3. on success -> set draw as upload_state = uploaded

def _handler_tumblr(thefile):
    response = client.create_photo(blog_identifier,
                                   tags=["my art"],
                                   data=thefile)
    return response


def _handler_twitter(thefile):
    filename, file_extension = os.path.splitext(thefile)
    pngname = ntpath.basename(filename) + ".png"

    response = api.update_with_media(thefile, status=pngname)
    return response

def _handler_pinterest(thefile):
    urlstring = f"https://api.pinterest.com/v1/pins/?access_token={PINTEREST_API_TOKEN}&fields=id"
    filename = ntpath.basename(thefile)

    imagedata = open(thefile, 'rb')
    data = MultipartEncoder(
        fields={
            'board': '<YOUR_PINTEREST_USERNAME>/<YOUR_BOARD_NAME>',
            'note': filename,
            'image': (thefile, imagedata, 'image/x-png')
        }
    )
    response = requests.post(urlstring, data, headers={'Content-Type': data.content_type})
    return response

domain_name_handlers = {
    "tumblr.com": _handler_tumblr,
    "twitter.com": _handler_twitter,
    "pinterest.com": _handler_pinterest,
}


def _upload_to_social_media(domain_name, thefile):
    filename, file_extension = os.path.splitext(thefile)
    if file_extension not in [".png", ".jpg", ".gif"]:
        print(
            f"ERROR: the file extension: {file_extension} is not implemented!")
        return

    def _not_implemented(thefile):
        print(
            f"ERROR: uploading to the domain_name {domain_name} is not implemented!")
        raise NotImplementedError

    print("_____ UPLOADING _____")  # DEBUG
    print("DOMAIN_NAME:", domain_name)  # DEBUG
    print("FILE:", thefile)  # DEBUG

    response = None
    try:
        _set_uploading(domain_name, thefile)
        response = domain_name_handlers.get(
            domain_name,
            _not_implemented  # 'default' handler
        )(thefile)  # run handler function
    except FileNotFoundError:
        _set_not_uploaded(domain_name, thefile)
        print('FileNotFound:', thefile, "... skipping!")
    except NotImplementedError:
        _set_not_uploaded(domain_name, thefile)
        print('NotImplementedError:', domain_name, "... skipping!")

    # print("RESPONSE:", response)
    print("got response (not shown, due to size of response)")

    # the 'returnval check' section
    if domain_name == "tumblr.com":
        try: # very soft error handling... (only if they give me the status!)
            if response['meta']['status'] > 200 or response['meta']['status'] < 200:
                return
        except KeyError:
            pass
        _set_uploaded(domain_name, thefile)
    else:
        _set_uploaded(domain_name, thefile)


def _list_not_uploaded():
    cur = conn.cursor()
    # callproc no returnval? tsk tsk...
    cur.execute(
        "SELECT * FROM not_uploaded();")
    files_to_upload = cur.fetchall()
    conn.rollback()

    return files_to_upload


def _set_uploading(domain_name, thefile):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM set_uploading(%s, %s);",
        (domain_name, thefile))
    conn.commit()


def _set_uploaded(domain_name, thefile):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM set_uploaded(%s, %s);",
        (domain_name, thefile))
    conn.commit()


def _set_not_uploaded(domain_name, thefile):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM set_not_uploaded(%s, %s);",
        (domain_name, thefile))
    conn.commit()


def _main():
    print('artspambot v4') # on changes, sanity check this number in syslogs
    [_upload_to_social_media(x[0], x[1]) for x in _list_not_uploaded()]


if __name__ == '__main__':
    conn = psycopg2.connect(CONN_STRING)
    _main()
