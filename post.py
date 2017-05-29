#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import config_import as ci
import json
import requests
import log_control
import traceback
import argparse

# Get configuration parameters
try:
    posts_url = ci.posts_url
    basic_auth = ci.basic_auth
except:
    err = "Read config failed.\n"
    log_control.logging.error(traceback.format_exc())
    raise

# Create ArgumentParser object
parser = argparse.ArgumentParser(description='WordPress Post with REST API v2')

# Define parameter for Filename(Markdown textfile)
parser.add_argument('filename', \
                    action= 'store', \
                    nargs= None, \
                    default= None, \
                    type= str, \
                    help='Define your filename to be posted')

# Define option handling "published" or "draft" status
# each options are included in mutually exclusive group
mgroup = parser.add_mutually_exclusive_group(required= True)

mgroup.add_argument('-p', '--published', \
                    action= 'store_const', \
                    const= True, \
                    default= False, \
                    help='Post the article with "published" status.')

mgroup.add_argument('-d', '--draft', \
                    action='store_const', \
                    const=True, \
                    default=False, \
                    help='Post the article with "draft" status.')

# Apply parser
args = parser.parse_args()

# Get options/parameters
file = args.filename
flag_published = args.published
flag_draft = args.draft

#print(file)
#print(flag_published)
#print(flag_draft)
#print(os.getcwd())

# ファイルのパースを外だしのクラスにするか要検討
# Create instance for parsing article
#ps = ParseArticle()
#
# Execute parsing article
#ps.parse_article(file)

f = open(file, 'r', encoding='utf-8')
article_body = f.read()
print(article_body)
f.close()


# Gef filename which is used for article title on WordPress
filename = os.path.basename(file)
article_title = os.path.splitext(filename)


payload = {"status": "publish", "title": article_title, "content": article_body,}

headers = {'Content-Type': 'Application/json',
           'Authorization': basic_auth}
r = requests.post(posts_url, data=json.dumps(payload), headers=headers)

print(r.json())

