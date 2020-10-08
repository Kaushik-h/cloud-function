from google.cloud import firestore
from flask import render_template_string
from datetime import datetime
from twilio.rest import Client



INDEX_TEMPLATE = """
<!DOCTYPE html>
<head>
  <title>Api gateway</title>
  <link href="https://fonts.googleapis.com/css?family=Google+Sans" rel="stylesheet">

</head>
<body>
    <br><br><br>
  <center style="font-family: 'Google Sans', sans-serif;">
  <h2>Domains expiring in less than a year</h2><br><br>
  Message sent to +918807570687<br><br><br>
  Domain:{result[0]}<br>
  <img src="https://storage.googleapis.com/favicon/{result[0]}" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/{result[0]}" style="padding: 40px;">
  <br><br><br>
  Domain:{result[1]}<br>
  <img src="https://storage.googleapis.com/favicon/{result[1]}" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/{result[1]}" style="padding: 40px;">
  <br><br><br>
  Domain:{result[2]}<br>
  <img src="https://storage.googleapis.com/favicon/{result[2]}" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/{result[2]}" style="padding: 40px;">
  <br><br><br>
  Domain:{result[3]}<br>
  <img src="https://storage.googleapis.com/favicon/{result[3]}" style="padding: 40px;">
  <img src="https://storage.googleapis.com/resize-favicon/{result[3]}" style="padding: 40px;">
  <br><br><br>

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

    result=[]
    message=""
    for l in alldomains:
        temp=l["Expires on"]
        temp=temp.split("at")[0]
        d=datetime.strptime(temp,"%B %m %Y ")
        exp=d-datetime.now()
        if exp.days<=365:
            result.append(l["Domain Name"]) 
            message += "The domain "+l["Domain Name"]+" expires in "+str(exp.days)+" days\n"
             
    client = Client("AC2973c1c7bd119b224e916fbc556eae11", "96e2c7f4030476478cd85eb512362d33")
    client.messages.create(to="+918807570687", 
                       from_="+17602845386", 
                       body=message)
    request_json = request.get_json()
    
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return INDEX_TEMPLATE.format(result=result)
