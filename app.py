

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


@app.route('/chatbot', methods=['POST'])
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

@app.route('/chat', methods=['GET'])
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
  \"title\": \""+y[i]+"\", \
  \"subtitle\": \""+y[i]+"\",\
  \"imageUrl\": \""+x[i]+"\",\
  \"buttons\": [\
    {\
      \"text\": \"link\",\
      \"postback\": \""+z[i]+"\"\
    }\
  ]\
},"
    str =str[:-1]+"],\"speech\": \"Here you go\",\"displayText\": \"\",\"data\": \"data\",\"contextOut\": [],\
    \"source\": \"apiai-search-webhook\" "
    return str         
       

@app.route('/travel', methods=['POST'])
def webhookTravel():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequestTravel(req)
    
    #res = json.dumps(res, indent=4)
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



def processRequestTravel(req):
    #if req.get("result").get("action") != "input.welcome":
    #    return {"action is empty"}
    result = req.get("result").get("parameters")
    statecustom=""
    citycustom=""
    countrycustom=""
    city=""
    state=""
    country=""    
    try:
        city =result.get("geo-city")
    except:
        city=" "
    try:
        country =result.get("geo-country")
    except:
        country=" "
    try:
        state =result.get("geo-state-us")
    except:
        state=" "
    try:
        statecustom=result.get("state")
    except:
        statecustom=" "
    try:
        countrycustom=result.get("country")
    except:
        countrycustom=" "
    try:
        citycustom=result.get("city")
    except:
        citycustom=" "
    #if query is None:
     #   return None
    result=searchTravel(city+" "+country+" "+state+" "+countrycustom+" "+statecustom+" ")
    
    #data = json.loads(req)
    res = makeWebhookResultTravel(result)
    return res





def makeWebhookResultTravel(data):
    
    #print("Response:")
    #print(speech)
	  return "{"+buildJsonTravel(data[0],data[1],data[2],data[3])+"}"
	  

	        

def searchTravel(query):

     query="tourists places "+query
     query=query.strip().split()
     query="+".join(query)
     html="https://www.google.co.in/search?q="+query
     req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'})
     soup = BeautifulSoup(urlopen(req).read(),"html.parser")
     #print(soup)

     title=[]
     desc=[]
     img=[]
     link=[]
     places=[]
     for item in soup.find_all( 'div', class_='title' ):
             try:
                 title.append(item.text)
             except:
                 continue
     for item in soup.find_all( 'div', class_='_Ajf' ):
             try:
                 desc.append(item.text)
             except:
                 continue
     for item in soup.find_all( 'g-img', class_='_Pkf' ):
             try:
                 img.append(item.img['data-src'])
             except:
                 continue
     for item in soup.find_all( 'a', class_='rl_item' ):
             try:
                 link.append("https://www.google.co.in"+item['href'])
             except:
                 continue
     places.append(title[:6])
     places.append(desc[:6])
     places.append(img[:6])
     places.append(link[:6])

     return places
def buildJsonTravel(w,x,y,z):
    str=""
    str +="\"messages\": ["
    for i in range(len(x)):
            str +="{ \
  \"type\": 1, \
  \"title\": \""+w[i]+"\", \
  \"subtitle\": \""+x[i]+"\",\
  \"imageUrl\": \""+y[i]+"\",\
  \"buttons\": [\
    {\
      \"text\": \"link\",\
      \"postback\": \""+z[i]+"\"\
    }\
  ]\
},"
    str =str[:-1]+"],\"speech\": \"Here you go\",\"displayText\": \"\",\"data\": \"data\",\"contextOut\": [],\
    \"source\": \"apiai-travel-webhook\" "
    return str         

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

