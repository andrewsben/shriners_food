#!/usr/bin/env python

import datetime
import glob
import json
import MySQLdb
import os


from cgi import escape
from git import Repo


def database():
    db = MySQLdb.connect(host="localhost", user="root",
                         passwd="password", db="shriners_food")
    conn = db.cursor()
    return db, conn


def not_found(environ, start_response):
    status = '200 OK'
    output = return_generics()
    output += ('<div class="container-fluid"><center><img src="'
               'http://25.media.tumblr.com/tumblr_m3fndvf5l61rocz98o1_500.jpg'
               '"></center><br/><center>No... No... Your page no here'
               '</center>')
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]


def return_generics():
    url = 'http://getbootstrap.com/2.3.2/assets/css/bootstrap.css'
    return_value = """<html><head>
<link href="%s" rel="stylesheet">
<style type="text/css"> body { width: 1920px; height: 1080px; color: #ddd;
background-color: #161616; }</style>
<meta http-equiv="refresh" content="300">
</head>""" % url
    return return_value

def return_generic_ending():
    return "</html>"

