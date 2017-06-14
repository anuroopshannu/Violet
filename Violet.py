import speech_recognition as sr
from gtts import gTTS
import subprocess
import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pyowm
import urllib2
import json
import gnp
import requests
import httplib, urllib, base64
from pyshorteners import Shortener
import webbrowser
import googlemaps
import unirest

def background():
    os.system("gnome-terminal --disable-factory -e python pi2.py")

def split_line(text):
    words=text.split()
    return words

def say(tex):
    tts=gTTS(text=tex,lang='hi')
    tts.save("hello.mp3")
    subprocess.Popen(['mpg321','-q','hello.mp3']).wait()

def understand(audio):
    words=[]
    try:
        text=r.recognize_google(audio)
        words=split_line(text)
    except sr.UnknownValueError:
        print("\n")
    except sr.RequestError as e:
        print("Error; {0}".format(e))
    return words


def short(url1):
    api_key = 'AIzaSyA35OD1fMj7nwWGrxzGDjkx9_Qo6Khci5g'
    shortener = Shortener('Google', api_key=api_key)
    url=format(shortener.short(url1))
    return(url)



    
def sendlink(url,name):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "recipient":{
            "id":"1219955768022769"
        }, 
        "message":{
            "text":"Here is your "+name+" link sir."+"\n"+url
        }
    }

    res=requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=EAAWW5k7XzMUBAGX35kBfC3QJanNH0PT7owkLuBFfp3ZCx43wvS7noQ0ZBGe2NgU4wjul97RTYDPqkIZC2Hb78rlEsuJZCYygSD0BSLcYsnFnVcsJxZCc2EBZCIKW3k1YHZCC9zgN0FvM7Qtov0qsglM2SwBSZCZB4fObmEzSxUiW8FQZDZD', headers=headers, data=str(data))
    print(res)

def sendinfo(img,msg,head,url):    
        headers = {
        'Content-Type': 'application/json',
        }

        data = {
          "recipient":{
            "id":"1219955768022769"
              },
          "message":{
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"generic",
                "elements":[
                  {
                    "title":str(head),
                    "image_url":str(img),
                    "subtitle":str(msg),
                    "buttons":[
                      {
                        "type":"web_url",
                        "url":str(url),
                        "title":"Details"
                      }      
                    ]
                  }
                ]     
              }
            }
          }
        }
        response=requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=EAAWW5k7XzMUBAGX35kBfC3QJanNH0PT7owkLuBFfp3ZCx43wvS7noQ0ZBGe2NgU4wjul97RTYDPqkIZC2Hb78rlEsuJZCYygSD0BSLcYsnFnVcsJxZCc2EBZCIKW3k1YHZCC9zgN0FvM7Qtov0qsglM2SwBSZCZB4fObmEzSxUiW8FQZDZD', headers=headers, data=str(data))
        print(response)


def weather(when,rain):
    if(when=='today' and rain==False):   
        f = urllib2.urlopen('http://api.wunderground.com/api/163116335516fb9a/conditions/q/India/Hyderabad.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        location = parsed_json['current_observation']['display_location']['city']
        weather = parsed_json['current_observation']['weather']
        temp_c = parsed_json['current_observation']['temp_c']
        humidity=parsed_json['current_observation']['relative_humidity']
        wind=parsed_json['current_observation']['wind_string']
        ppt=parsed_json['current_observation']['precip_today_metric']
        f.close()
        say("location."+location) 
        say("weather."+weather)
        say("temperature,"+str(temp_c)+"degree celsius")
        say("Humidity."+str(humidity))
        say("Wind."+wind)
        if(ppt!="0"):
            say("Precipitation."+"rain")
        else:
            say("Precipitation."+"No precipitation")

    elif(when=='today' and rain==True):
        f = urllib2.urlopen('http://api.wunderground.com/api/163116335516fb9a/conditions/q/India/Hyderabad.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        ppt=parsed_json['current_observation']['precip_today_metric']
        weather = parsed_json['current_observation']['weather']
        humidity=parsed_json['current_observation']['relative_humidity']
        f.close()
        if(ppt!="0.0"):
            say("Yes sir,It is going to rain today.")
            say("precipitation"+ppt+"mm")
            say("climate."+weather) 
            say("Humidity."+str(humidity))
        else:
            say("No sir,I don't think It's going to rain today sir.")
            say("precipitation"+ppt+"mm")
            say("climate."+weather) 
            say("Humidity."+str(humidity))

    elif(when=='tomorrow' and rain==False):
        f = urllib2.urlopen('http://api.wunderground.com/api/163116335516fb9a/forecast/q/India/Hyderabad.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        weather = parsed_json['forecast']['simpleforecast']['forecastday'][0]['conditions']
        ppt=parsed_json['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm']
        humidity=parsed_json['forecast']['simpleforecast']['forecastday'][1]['avehumidity']
        f.close()
        say("Tommorow's climate."+weather)
        say("precipitation"+str(ppt)+"mm")
        say("humidity."+str(humidity)+"percent")
    elif(when=='tomorrow' and rain==True):
        f = urllib2.urlopen('http://api.wunderground.com/api/163116335516fb9a/forecast/q/India/Hyderabad.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        weather = parsed_json['forecast']['simpleforecast']['forecastday'][0]['conditions']
        ppt=parsed_json['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm']
        ppt=str(ppt)
        humidity=parsed_json['forecast']['simpleforecast']['forecastday'][1]['avehumidity']
        f.close()
        if(ppt!="0"):
            say("it is going to rain tomorrow sir.")
            say("Tomorrow's climate."+weather)
            say("precipitation"+str(ppt)+"mm")
            say("humidity."+str(humidity)+"percent")
        else:
            say("No sir.I don't see any chances of rain tomorrow")
            say("Tomorrow's climate."+weather)
            say("precipitation"+str(ppt)+"mm")
            say("humidity."+str(humidity)+"percent") 




def goodmorn():
    now=datetime.datetime.now()
    say("A Very Good Morning Sir.")
    say(now.strftime("The time is %I %M %p.%A %x"))
    say("weather Report:")
    weather('today',False)


def news(category):
    a=gnp.get_google_news(gnp.EDITION_ENGLISH_INDIA)
    url=a['meta']['url']
    sendlink(url,(category+" news"))
    i=0
    if(category=="local"):
        while((a['stories'][i]['category'])!='Secunderabad, Telangana'):
            i+=1
        say("Fetching Local News")
        while((a['stories'][i]['category'])!='India'):
            
            if((a['stories'][i]['category'])=='Secunderabad, Telangana'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="national"):
        while((a['stories'][i]['category'])!='India'):
            i+=1
        say("fetching national News")
        while((a['stories'][i]['category'])!='World'):
            
            if((a['stories'][i]['category'])=='India'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="world"):
        while((a['stories'][i]['category'])!='World'):
            i+=1
        say("fetching international News")
        while((a['stories'][i]['category'])!='Business'):
            
            if((a['stories'][i]['category'])=='World'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="business"):
        while((a['stories'][i]['category'])!='Business'):
            i+=1
        say("fetching Business News")
        while((a['stories'][i]['category'])!='Technology'):
            
            if((a['stories'][i]['category'])=='Business'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="tech"):
        while((a['stories'][i]['category'])!='Technology'):
            i+=1
        say("fetching Technology News")
        while((a['stories'][i]['category'])!='Entertainment'):
            
            if((a['stories'][i]['category'])=='Technology'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="entertainment"):
        while((a['stories'][i]['category'])!='Entertainment'):
            i+=1
        say("fetching Entertainment News")
        while((a['stories'][i]['category'])!='Sports'):
            
            if((a['stories'][i]['category'])=='Entertainment'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="sports"):
        while((a['stories'][i]['category'])!='Sports'):
            i+=1
        say("fetching Sports News")
        while((a['stories'][i]['category'])!='Science'):
            
            if((a['stories'][i]['category'])=='Sports'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="science"):
        while((a['stories'][i]['category'])!='Science'):
            i+=1
        say("fetching Science News")
        while((a['stories'][i]['category'])!='Health'):
            
            if((a['stories'][i]['category'])=='Science'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="health"):
        while((a['stories'][i]['category'])!='Health'):
            i+=1
        say("fetching Health News")
        while((a['stories'][i]['category'])!='More Top Stories'):
            
            if((a['stories'][i]['category'])=='Health'):
                say(a['stories'][i]['title'])
            i+=1
    elif(category=="all"):
        say("Fetching News")
        while((a['stories'][i]['category'])!='More Top Stories'):
                i+=1
        while i in range(len(a['stories'])):
            say(a['stories'][i]['title'])
            i+=1
    

def hello():
    say("Hello Sir")


def search(query):

    img="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcR-J0-UsNmqZCjylhJ3so2BtSaaywBEkXLFD6U7I-JyrQvXFZOUqg"
    img=short(img)
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '86f683b677644f41ac474908c8a9b0d0',
    }

    params = urllib.urlencode({
        # Request parameters
        'q': str(query),
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safesearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    data=str(data)
    i=data.find("\"snippet\":")
    i=i+12
    j=data.find(".",i)
    info=data[i:j]
    i=data.find("\"webSearchUrl\":")
    i=i+17
    j=data.find(",",i)
    j=j-1
    url=data[i:j]
    url=url.replace("\\/","/")
    url=short(url)
    i=data.find("\"thumbnailUrl\":")
    if(i!=-1):
        j=data.find(",",i)
        i=i+17
        j=j-1
        img=data[i:j]
        img=img.replace("\\/","/")
        img=short(img)
    print(info)
    print(img)
    print(url)
    say(info)
    sendinfo(img,info,query,url)

 
def play(query):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b888454b8303481f8761e9dd6cdf7047',
    }

    params = urllib.urlencode({
        # Request parameters
        'q': str(query),
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/videos/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    data=str(data)
    play=""
    j=0
    while(play.find("youtube")==-1):
        i=data.find("\"contentUrl\":",j)
        i=i+15
        j=data.find(",",i)
        j=j-1
        play=data[i:j]
    print(play)
    webbrowser.open_new(play)



def getpic(query):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b6d5c07bb56349f3a6fa659946db0c9d',
    }

    params = urllib.urlencode({
        # Request parameters
        'q': str(query),
        'count': '1',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    data=str(data)
    i=data.find("\"thumbnailUrl\":")
    j=data.find(",",i)
    i=i+17
    j=j-1
    url=data[i:j]
    return(url)

def loc():
    say("fetching your current location sir")
    res=unirest.post("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDvIDIFzVoVMZVntp9Zsno5zi8H0h89EFE")
    data=dict(res.body)
    lat=data['location']['lat']
    lon=data['location']['lng']
    url="https://www.google.co.in/maps/place/"+str(lat)+","+str(lon)
    print(url)
    webbrowser.open_new(url)

def dir(src,dest):
    say("preparing and plotting map sir")
    url="https://www.google.co.in/maps/dir/"+src+"/"+dest
    webbrowser.open_new(url)
    img="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSetG_TaaOIYAplUP8EyqQHn2co291jooG3PR-Q3_z1C_imtpXO"
    head="Directions from "+src+" to "+dest
    msg="powered by Googlemaps."
    sendinfo(img,msg,head,url)



def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.dynamic_energy_adjustment_ratio=2.5
        r.adjust_for_ambient_noise(source,duration=1)
        audio=r.listen(source)
        words=understand(audio)
        return(words)

sched=BackgroundScheduler()
sched.add_job(goodmorn,'cron',day_of_week='mon-sat',hour=07)
sched.start()
while(1):
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.dynamic_energy_adjustment_ratio=2.5
        r.adjust_for_ambient_noise(source,duration=1)
        audio=r.listen(source)
        words=understand(audio)
        
        for i in words:
            print(i)
        if('violet' in words or 'pilot' in words):
            if ('hello' in words):
                hello()
            elif('weather' in words or "rain" in words):
                if('today' in words or "today's" in words):
                    say("Fetching Today's forecast")
                    if ('rain' in words):
                        weather('today',True)
                    else:
                        weather('today',False)
                elif('tomorrow' in words or "tomorrow's" in words): 
                    say("Fetching Tomorrow's forecast")
                    if ('rain' in words):
                        weather('tomorrow',True)
                    else:
                        weather('tomorrow',False)
                else:
                    say("Sorry sir.I don't think I can forecast That weather")     
            elif('news' in words or "headlines" in words):
                say("please give me a moment before i send the link to you sir.") 
                if('local' in words or 'city' in words):
                    news('local')
                elif('national' in words or 'country' in words):
                    news('national')
                elif('world' in words or 'international' in words):
                    news('world')
                elif('business' in words or 'finance' in words or 'financial' in words):
                    news('business')
                elif('technology' in words or 'tech' in words or 'geek' in words or 'favourite' in words):
                    news('tech')
                elif('entertainment' in words or 'movie' in words):
                    news('entertainment')
                elif('sports' in words):
                    news('sports')
                elif('science' in words or 'scientific' in words):
                    news('science')
                elif('health' in words or 'medical' in words):
                    news('health')
                else:
                    news("all")
            elif ('music' in words or 'songs' in words or 'trailer' in words or 'song' in words or 'video' in words):
                say("which one do you want me to play sir?")
                words=listen()
                query=""
                for i in words:
                    query=query+" "+i
                print(query)
                play(query)
            elif ('location' in words):
                loc()
            elif('directions' in words or 'navigate' in words):
                for i in range(1,len(words)):
                    if(words[i]=="from"):
                        src=words[i+1]
                    elif(words[i]=='to'):
                        dest=words[i+1]
                dir(src,dest)
            else:
                query=""
                for i in range(1,len(words)):
                    query=query+" "+words[i]
                search(query)
     
                

