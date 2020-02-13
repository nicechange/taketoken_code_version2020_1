#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    commontools
    ~~~~~

    :copyright: (c) 2014 by Muneeb Ali <http://muneebali.com>
    :license: MIT, see LICENSE for more details.
"""

import os 
import sys
import json
import logging
import logging.config

#-------------------------
def setup_logging(
    file_name='logging.json', 
    default_level=logging.INFO,
):
    """
        Setup logging configuration
    """

    current_dir =  os.path.abspath(os.path.dirname(__file__))
    
    file_path = current_dir + '/' + file_name 

    if os.path.exists(file_path):
        with open(file_path, 'rt') as f:
            data = f.read()
            config = json.loads(data)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    #stop logs from requests
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

#-------------------------
def pretty_dump(input):

    return json.dumps(input, sort_keys=False, indent=4, separators=(',', ': '))

#-------------------------
def pretty_print(input):

    log = logging.getLogger()
    log.debug(pretty_dump(input))

#-----------------------------------
def utf8len(s):

    if type(s) == unicode:
        return len(s)
    else:
        return len(s.encode('utf-8'))

#-----------------------------------------
def get_json(data):

    if isinstance(data,dict):
        pass 
    else:
        try:
            data = json.loads(data)
        except:
            return error_reply("input data is not JSON")
        
    return data

#-----------------------------------------
def get_string(data):

    if isinstance(data,dict):
        data = json.dumps(data) 
    else:
        pass
        
    return data

#---------------------------------
def error_reply(msg, code = -1):
    reply = {}
    reply['status'] = code
    reply['error'] = msg
    return reply