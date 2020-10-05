from google.cloud import firestore
from flask import render_template_string

INDEX_TEMPLATE = """
<!DOCTYPE html>
<head>
  <title>Api gateway</title>
</head>
<body>
    <br><br><br>
  <center>
  <img src="https://storage.googleapis.com/favicon/GOOGLE.COM" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/GOOGLE.COM" style="padding: 40px;">
  <br><br><br>
  <img src="https://storage.googleapis.com/favicon/AMAZON.COM" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/AMAZON.COM" style="padding: 40px;">
  <br><br><br>
  <img src="https://storage.googleapis.com/favicon/COURSERA.ORG" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/COURSERA.ORG" style="padding: 40px;">
  <br><br><br>
  <img src="https://storage.googleapis.com/favicon/INSTAGRAM.COM" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/INSTAGRAM.COM" style="padding: 40px;">
  </center>
</body>
"""


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    
    alldomains=[]
    db = firestore.Client()
    domains = db.collection('domain').stream()
    for d in domains:
        alldomains.append(d.to_dict())

    request_json = request.get_json()
    
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return INDEX_TEMPLATE

