import os
import uuid
from flask import Flask
from time import localtime, strftime

app = Flask(__name__)
my_uuid = str(uuid.uuid1())

html_header = """<html><head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
    <title>Pied Piper - Lab 1</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
    </head><body><div class="container center-block">"""

html_footer = """<hr><small><b>GUID: </b>{}</small></div></body></html>""".format(my_uuid,)

file = open('sessions.txt')
sessionsfile = file.readlines()
file.close()


@app.route('/')
def mainmenu():

    session = []
    
    html_body = """<div class="panel panel-primary"><div class="panel-heading"><h3 class="panel-title">Agenda</h3></div><div class="panel-body"><div class="list-group">"""

    for line in sessionsfile:
        session = line.split(';')
        html_body += """
        <a href="/details/{}" class="list-group-item">{}</a>
        """.format(session[0], session[1])

    html_body += """</div></div></div>"""

    response = html_header + html_body + html_footer

    return response

@app.route('/details/<session_id>')
def details(session_id):

    session = []
    response = ""

    for line in sessionsfile:
        session = line.split(';')
        if session[0] == session_id:
            friendly_datetime = strftime("%a %d %b %H:%M %p",localtime(int(session[2])))
            html_body = """<div class="panel panel-primary"><div class="panel-heading"><h3 class="panel-title">{}</h3></div><div class="panel-body">
            <h4 class="list-group-item-heading">{}</h4>
            <p class="list-group-item-text">{}</p><hr>
            <small>Presenter : {}</small>
            """.format(session[1], friendly_datetime, session[4], session[3])

            html_body += """</div></div>"""
            response = html_header + html_body + html_footer

    return response

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
