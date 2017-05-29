#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config_import as ci
import logging
import traceback

try:
    logging_level = ci.logging_level
    log_file = ci.log_file
except:
    logging.error(traceback.format_exc())
    raise

logging.basicConfig(
    level = logging_level,
    filename = log_file,
    format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s")
