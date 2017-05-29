#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config_import as ci
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
            # article_idがあり、かつ整数である場合は更新なので
            # このブロックで1行目を除外したarticle_bodyを再構成して返す必要がある
            # 
            pass
        else:
            log_control.logging.error('"article_id" in 1st line : ' + str(article_id) + ' is not valid.')
            raise
        
        return(article_id, article_title, article_body)