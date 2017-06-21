

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
    print(res)
    print("*********************")
    #res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/', methods=['GET'])
def web():
    
    return "WELCOME :)"


def processRequest(req):
    #if req.get("result").get("action") != "input.welcome":
    #    return {"action is empty"}
    result = req.get("result")
    
    query =result.get("resolvedQuery")
    
    #if query is None:
     #   return None
    result=search(query)
    
    #data = json.loads(req)
    res = makeWebhookResult(result)
    return res





def makeWebhookResult(data):
    
    #print("Response:")
    #print(speech)
	  return "{"+buildJson(data[0],data[1],data[2])+"}"
	  

	        

def search(query):
	query=query.strip().split()
	query="+".join(query)
	html="https://www.google.co.in/search?q="+query
	req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'})

	soup = BeautifulSoup(urlopen(req).read(),"html.parser")

	search =[]
	links = []
	titles = []
	imgs  = []


	for item in soup.find_all(attrs={'class' : '_IRj _dTj _l7n'}):
	        titles.append("".join(item.contents))

	for item in soup.find_all(attrs={'class' : '_uSj _owm _KBh'}):
	        links.append(item.a['href'])
	        try:
	            imgs.append(item.img['data-src'])
	        except:
	            imgs.append(item.img['src'])


	search.append(imgs[2:10])
	search.append(titles[2:10])
	search.append(links[2:10])
		

	return search

def buildJson(x,y,z):
    str=""
    str +="\"messages\": ["
    for i in range(len(x)):
            str +="{ \
  \"type\": 1, \
  \"title\": \""+x[i]+"\", \
  \"subtitle\": \""+x[i]+"\",\
  \"imageUrl\": \""+y[i]+"\",\
  \"buttons\": [\
    {\
      \"text\": \"\",\
      \"postback\": \""+z[i]+"\"\
    }\
  ]\
},"
    str =str[:-1]+"],\"speech\":\"str(data)\", \"displayText\": \"\",\"data\": \"data\",\"contextOut\": [],\
    \"source\": \"apiai-search-webhook\" "
    return str         
       


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5004))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

