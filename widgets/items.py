#!/usr/bin/env python

from common import *
from cgi import parse_qs, escape

db, conn = database()


def handle_form(form_data):
    success = False
    action = form_data['action'][0]
    if action == 'item_add':
        sql = "INSERT into items (name, price) VALUES ('%s', %s)" % (form_data['name'][0], form_data['price'][0])
        print sql
        conn.execute(sql)
        db.commit()
        success = True

    if action == 'item_edit':
        sql = "UPDATE items set name = '%s', price = %s where id = %s" % (form_data['name'][0], form_data['price'][0], form_data['item_id'][0])
        conn.execute(sql)
        db.commit()
        success = True

    if action == 'item_del':
        sql = "delete from items where id = '%s'" % form_data['item_id'][0]
        conn.execute(sql)
        db.commit()
        success = True

    if success:
        return ""
    else:
        return "<div class='error span6'>Failure<div>"


def items(environ, start_response):
    args = environ['myapp.url_args']

    status = '200 OK'
    output = return_generics()
    output += '<div class="container-fluid">'

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    form_data = parse_qs(request_body)

    output += """
<div class="row-fluid">"""
    if form_data:
        output += handle_form(form_data)
    output += """
    <div class="span6">
        <a class="btn-inverse btn-large" href=/items/add>
            New Item
        </a>
    </div>
</div>"""

    conn.execute("SELECT id, name, price from items order by id asc")
    rows = conn.fetchall()

    if len(rows):
        output += """
<div class="row-fluid">
    <div class="span6">
        <table class="table table-striped table-bordered span6" style="color:black">
            <tr style="width:100%">
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Edit</th>
                <th>Delete</th>
            </tr>"""
        for item in rows:
            id = item[0]
            name = item[1]
            price = item[2]
            output += """
            <tr class='success'>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="/items/edit/%s">Edit</a></td>
                <td>
                  <form method="post" action="/items">
                    <input type="hidden" name="action" value="item_del">
                    <input type="hidden" name="item_id" value="%s">
                    <input type="submit" value="Delete">
                  </form>
                </td>
            </tr>""" % (id,name,price,id,id)
        output += """
         </div>
    </div>"""


    
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


def item_add(environ, start_response):
    args = environ['myapp.url_args']

    status = '200 OK'
    output = return_generics()
    output += '<div class="container-fluid">'

    output += """
<div class="row-fluid">
  <div class="span6">
    <form method="post" action="/items">
      <input type="hidden" name="action" value="item_add">
      <p>    
        Name: <input type="text" name="name">
      </p>
      <p>
        Price: <input name="price" type="text">
      </p>
        <input class="btn-inverse btn-large" type="submit" value="Submit">
      </p>
    </form>
  </div>
</div>"""

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


def item_edit(environ, start_response):
    args = environ['myapp.url_args']
    item_id = args[0]

    conn.execute('select id, name, price from items where id = %s' % (item_id))
    item_info = conn.fetchall()[0]
    item_name = item_info[1]
    item_price = item_info[2]

    status = '200 OK'
    output = return_generics()
    output += '<div class="container-fluid">'

    output += """
<div class="row-fluid">
  <div class="span6">
    <form method="post" action="/items">
      <input type="hidden" name="action" value="item_edit">
      <input type="hidden" name="item_id" value="%s">
      <p>    
        Name: <input type="text" name="name" value="%s">
      </p>
      <p>
        Price: <input name="price" type="text" value="%s">
      </p>
        <input class="btn-inverse btn-large" type="submit" value="Submit">
      </p>
    </form>
  </div>
</div>""" % (item_id, item_name, item_price)

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
