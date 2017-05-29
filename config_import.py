#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import sep
from os.path import expanduser
import configparser
import logging
import traceback

# Construct config_file path & read config file
try:
    homedir_path = (expanduser('~'))
    config_file = homedir_path + "/wp-api.ini".replace('/', sep)
    config = configparser.ConfigParser()
    config.read(config_file)
except:
    logging.error(traceback.format_exc())
    raise

# ------------  Import parameters from config file  ------------

# [Auth]
posts_url = config.get('Auth', 'posts_url')
basic_auth = config.get('Auth', 'basic_auth')

# [Post]
default_status = config.get('Post', 'default_status')

# [Logging]
logging_level = config.get('Logging', 'logging_level')
log_file = config.get('Logging', 'log_file')
