

#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/', methods=['GET'])
def web():
    
    return "WELCOME :)"


def processRequest(req):
    if req.get("result").get("action") != "input.welcome":
        return {}
    result = req.get("result")
    
    query =result.get("resolvedQuery")
    
    if query is None:
        return None
    result=search(query)
    
    #data = json.loads(req)
    res = makeWebhookResult(result)
    return res





def makeWebhookResult(data):
    
    #print("Response:")
    #print(speech)

    return {
        "speech": str(data),
        "displayText": "",
        "imageUrl":"https://www.google.co.in/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
        # "data": data,
        # "contextOut": [],
        "source": "apiai-search-webhook"
    }

def search(query):
    query=query.strip().split()
    query="+".join(query)

    html = "https://www.google.co.in/search?site=&source=hp&q="+query+"&gws_rd=ssl"
    req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(urlopen(req).read(),"html.parser")

    #Regex
    reg=re.compile(".*&sa=")
    search =[]
    links = []
    title = []
    body  = []
    #parsing title
    for item in soup.find_all(attrs={'class' : 'r'}):
            title.append(item.a.contents)
    
    #parsing body
    for item in soup.find_all(attrs={'class' : 'st'}):
            body.append(item.contents)

    #Parsing web urls
    for item in soup.find_all('h3', attrs={'class' : 'r'}):
            line = (reg.match(item.a['href'][7:]).group())
            links.append(line[:-4])
    print(title)
    search.append(title)
    search.append(body)
    search.append(links)

    return search

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5004))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

