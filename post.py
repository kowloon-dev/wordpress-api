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
import category

# Get configuration parameters
try:
    base_url = ci.base_url
    basic_auth = ci.basic_auth
    default_status = ci.default_status
    cat_default_id = ci.cat_default_id
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
    exit(99)

# Create instance for parsing article and execute
pa = parse_article.ParseArticle()
try:
    parse_result = pa.parse_article(file)
except:
    log_control.logging.error('Parsing file failed.')
    exit(99)

# Get article properties from result array
article_id = parse_result[0]
article_title = parse_result[1]
article_body = parse_result[2]

if article_id is not False:
    # "article_id is not False" means that this is an "update" action.
    posts_url = base_url + 'posts/' + str(article_id)
    is_update = True
else:
    # "article_id is False" means that this is an "initial" post action.
    # Show category list to users and let him chose some categories.
    posts_url = base_url + 'posts/'
    is_update = False
    
    # Create instance to handle category
    cat = category.Category()
    #  Get categories
    try:
        category_list = cat.get_category()
    except:
        log_control.logging.error('Get category list failed.')
        exit(99)
    print("Please select category id.")
    for cat in category_list:
        category_id = str(cat['id'])
        category_name = cat['name']
        print(category_id + " : " + category_name)
    category_id_chosen = input('>>> ')
    if category_id_chosen is False:
        category_id = cat_default_id

# Check status and set flag
if flag_publish == True:
    status = "publish"
elif flag_draft == True:
    status = "draft"
else:
    status = default_status

# Build request header and payload
headers = {'Content-Type': 'Application/json', 'Authorization': basic_auth}

if article_id is not False:
    payload = {"status": status, "title": article_title, "content": article_body}
else:
    payload = {"status": status, "title": article_title, "content": article_body,
               "categories": category_id_chosen}

# Execute POST request
try:
    post_response = requests.post(posts_url, data=json.dumps(payload), headers=headers)
except:
    log_control.logging.error('POST request failed.')
    exit(99)

# Parse POST response
post_response = post_response.json()
article_id = str(post_response['id'])
post_date = str(post_response['date'])
link = str(post_response['link'])

# Update 1st line in article
try:
    update_result = pa.update_article(is_update, file, article_id, post_date, link)
except:
    log_control.logging.error('Update article file failed.')
    exit(99)