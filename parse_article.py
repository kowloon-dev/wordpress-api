#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config_import as ci
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
        # TBD