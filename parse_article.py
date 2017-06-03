#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from os import path
import json
import linecache
import log_control
import traceback


class ParseArticle:

    def __init__(self):
        try:
            pass
        except:
            err = "Read config failed.\n"
            log_control.logging.error(err + traceback.format_exc())
            raise

    def parse_article(self,file):

        # Initialize variables
        article_title = ""
        article_body = ""
        first_line = ""

        # Try to get management information(article_id etc..) from 1st line
        try:
            first_line = json.loads(linecache.getline(file, int(1)))
            article_id = first_line['article_id']
        except:
            article_id = False

        # Gef filename which is used for article title on WordPress
        article_title, ext = path.splitext(path.basename(file))

        if article_id is False:
            f = open(file, 'r', encoding='utf-8')
            article_body = f.read()
            f.close()
        elif isinstance(article_id, int) is True:
            # In case "article_id" is already exists at 1st line in MarkDown text,
            # create "article_body" without 1st line
            linenumber = 1
            f = open(file, 'r', encoding='utf-8')
            for line in f:
                # Skipping 1st line which contains management info(article_id etc..)
                if linenumber == 1:
                    pass
                else:
                    article_body = article_body + line
                linenumber += 1
            f.close()
        else:
            log_control.logging.error('"article_id" in 1st line : ' + str(article_id) + ' is not valid.')
            raise

        return(article_id, article_title, article_body)

    def update_article(self, is_update, file, article_id, post_date, link):

        # Initialize variables
        article_body = ""
        origin_file = ""
        new_1stline = ""
        linenumber = 1

        origin_file = str(path.basename(file)) + ".org"
        try:
            os.rename(file, origin_file)
        except:
            log_control.logging.error('Making tmpfile failed. filename : ' + origin_file)
            raise

        # Create new 1st line which contains new management info (article id, post date etc...)
        new_1stline = '{"article_id": ' +  str(article_id) + \
                      ', "post_date": "' + str(post_date) + \
                      '", "link": "' + str(link) + '"}\n'

        f_origin = open(origin_file, 'r', encoding='utf-8')
        f_new = open(file, 'w', encoding='utf-8')

        if is_update is True:
            article_body = new_1stline
            for line in f_origin:
                # Skipping 1st line of origin_file because this is "update" action so
                # origin_file contains old management info.
                if linenumber == 1:
                    pass
                else:
                    article_body = article_body + line
                linenumber += 1
        elif is_update is False:
            article_body = new_1stline
            # Flag value "is_update" is False means that this is the initial post 
            # and does not need to skip 1st line of original file.
            for line in f_origin:
                article_body = article_body + line
        else:
            log_control.logging.error('Cannot identify whether this is an "update" or not.')
            raise

        try:
            f_new.write(article_body)
        except:
            log_control.logging.error('Write new article_body to ' + str(path(file)) + 'failed.')
            raise

        f_origin.close()
        f_new.close()
        try:
            os.remove(origin_file)
        except:
            log_control.logging.error('Removing tmpfile failed. filename : ' + 
                                      str(path(origin_file)))
            raise
