#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config_import as ci
import json
import requests
import log_control
import traceback


class Category:
    
    def __init__(self):
        try:
            self.base_url = ci.base_url
            self.basic_auth = ci.basic_auth
            self.cat_sort_key = "'" + ci.cat_sort_key + "'"
            self.cat_sort_reverse = ci.cat_sort_reverse
        except:
            err = "Read config failed.\n"
            log_control.logging.error(err + traceback.format_exc())
            raise

    def get_category(self):
        # Execute POST request to get category list
        headers = {'Content-Type': 'Application/json', 'Authorization': self.basic_auth}
        category_url = self.base_url + 'categories/'
        try:
            r = requests.get(category_url, headers=headers)
            category_list = r.json()
            return(category_list)
        except:
            err = "Get category list failed.\n"
            log_control.logging.error(err + traceback.format_exc())
            raise
