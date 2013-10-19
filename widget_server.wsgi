#!/usr/bin/env python

import datetime
import glob
import json
import MySQLdb
import os
import random
import re
import string
import sys

from cgi import parse_qs, escape
from dateutil import parser
from git import Repo
from wsgiref.simple_server import make_server

from widgets.common import *
from widgets.views import *

os.chdir(os.path.dirname(sys.argv[0]))


def index(environ, start_response):
    status = '200 OK'
    output = return_generics()
    output += """
<div class="span12">
    <h3 style="align: center">Available Pages</h3>
</div>
<table class="table table-striped table-bordered span12" style="color:black">
    <tr style="width:100%">
        <th>Link</th>
    </tr>"""

    for item in urls:
        regex = item[0]
        regex = regex.replace('/?$','')
        regex_haxed = regex.replace('^','').replace('$','')
        if regex.replace('^','').replace('$','') == '':
            continue
        if '/' in regex.replace('/?','') or 'newgraph' in regex:
            continue
        output += """
<tr class='success' onmouseover=\"this.style.cursor='pointer'\"
                       onclick=\"window.location ='/%s'\">
    <td>%s</td>
</tr>""" %  (regex_haxed, regex_haxed)
    output += "</table>"
    output += return_generic_ending()

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


urls = [
    (r'^order$', order),
    (r'^order/add$', order_add),
#    (r'^order/edit/(.+)$', order_edit),
#    (r'^order/view/(.+)$', view),
    (r'^items$', items),
    (r'^items/edit/(.+)$', item_edit),
    (r'^items/add$', item_add),
    (r'^/?$', index)
]


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)


if __name__ == '__main__':
    httpd = make_server('', 8051, application)
    httpd.serve_forever()
