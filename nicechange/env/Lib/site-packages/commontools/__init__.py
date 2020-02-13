#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	commontools
	~~~~~

	:copyright: (c) 2014 by Muneeb Ali <http://muneebali.com>
	:license: MIT, see LICENSE for more details.
"""

__version__ = '0.1.0'

from .commontools import setup_logging
from .commontools import pretty_dump, pretty_print
from .commontools import utf8len
from .commontools import get_json, get_string
from .commontools import error_reply

import logging
setup_logging()
log = logging.getLogger()
