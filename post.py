#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import config_import as ci
import json
import requests
import log_control
import traceback
import argparse
import parse_article

# Get configuration parameters
try:
    posts_url = ci.posts_url
    basic_auth = ci.basic_auth
    default_status = ci.default_status
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

# Define option handling "publish" or "draft" status
# each options are included in mutually exclusive group
mgroup = parser.add_mutually_exclusive_group(required= False)

mgroup.add_argument('-p', '--publish', \
                    action= 'store_const', \
                    const= True, \
                    default= False, \
                    help='Post the article with "publish" status.')

mgroup.add_argument('-d', '--draft', \
                    action='store_const', \
                    const=True, \
                    default=False, \
                    help='Post the article with "draft" status.')

# Apply parser
args = parser.parse_args()

# Get option and parameters
file = args.filename
flag_publish = args.publish
flag_draft = args.draft

# Check the existence of file
if os.path.exists(file) is False:
    log_control.logging.error('Filename "' + file + '" does not exist.\
    Please verify filename and existence.')
    raise

# Create instance for parsing article and execute
pa = parse_article.ParseArticle()
try:
    parse_result = pa.parse_article(file)
except:
    log_control.logging.error('Parsing file failed.')
    raise

article_id = parse_result[0]
article_title = parse_result[1]
article_body = parse_result[2]

if flag_publish == True:
    status = "publish"
elif flag_draft == True:
    status = "draft"
else:
    status = default_status

# Build request payload
payload_str = '{"status": "' + status + '"'
payload_str = payload_str + ', "title": "' + article_title + '"'
payload_str = payload_str + ', "content": ' + article_body

if article_id is not False:
    payload_str = payload_str + ', "id": ' + str(article_id)

payload_str = payload_str + '}'

print(payload_str)

exit()

payload = {"status": "publish", "title": article_title, "content": article_body,}

headers = {'Content-Type': 'Application/json',
           'Authorization': basic_auth}

r = requests.post(posts_url, data=json.dumps(payload), headers=headers)

print(r.json())

