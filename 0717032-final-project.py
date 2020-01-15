import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import socket
import urllib
import json
from urllib import request
import datetime
import random
from googletrans import Translator
# open cwb  get data
def cwb(sdate,edate):
    x = datetime.datetime.now()
    now = x.hour
    if(now>18 or now<6):
        sdate=sdate*2-1
        edate=edate*2
    else:
        sdate=sdate*2-2
        edate=edate*2
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-3C35B6B0-2806-41DB-A401-E68DD6822651"
    data = request.urlopen(url).read().decode("utf-8")
    data = json.loads(data)
    location=[]
    rain=[]
    maxtemp=[]
    mintemp=[]
    for l in range(0,22):
        location.append(data['records']['locations'][0]['location'][l]['locationName'])
        p=1
        mint=100
        maxt=-100
        for t in range(sdate,edate):
            for i in data['records']['locations'][0]['location'][l]['weatherElement'][0]['time'][t]['elementValue']:
                if(int(data['records']['locations'][0]['location'][l]['weatherElement'][12]['time'][t]['elementValue'][0]['value'])>maxt):
                    maxt=int(data['records']['locations'][0]['location'][l]['weatherElement'][12]['time'][t]['elementValue'][0]['value'])
                if(int(data['records']['locations'][0]['location'][l]['weatherElement'][8]['time'][t]['elementValue'][0]['value'])<mint):
                    mint=int(data['records']['locations'][0]['location'][l]['weatherElement'][8]['time'][t]['elementValue'][0]['value'])
                p*=1-(float(i['value'])/100)          
        rain.append(p)
        maxtemp.append(maxt)
        mintemp.append(mint)
    zipped=sorted(zip(location,rain,maxtemp,mintemp), key=lambda x: x[1],reverse=1)
    i=0
    print("No. Location No rain MAXT MINT")
    dict={}
    for a,b,c,d in zipped:
        i+=1
        b=int(b*100)
        print(" %2d   %3s   %2d%%   %2d°C %2d°C"%(i,a,b,c,d))
        dict[i]=a
    print("\n")
    return dict

def tb(location):
    no={'屏東縣': '0001122','高雄市': '0001121','臺南市': '0001119','雲林縣': '0001115','嘉義縣': '0001116','嘉義市': '0001117','南投縣': '0001114','澎湖縣': '0001125','臺東縣': '0001123','彰化縣': '0001113', '臺中市': '0001112','苗栗縣': '0001110','花蓮縣': '0001124','宜蘭縣': '0001106','臺北市': '0001090','連江縣': '0001127','新北市': '0001091','桃園市': '0001107','新竹縣': '0001108','新竹市': '0001109','基隆市': '0001105','金門縣': '0001126'}
    url='https://www.taiwan.net.tw/m1.aspx?sNo='+str(no[location])
    f=requests.get(url)
    f.encoding='utf-8'
    soup=BeautifulSoup(f.text,'html.parser')
    spot=[]
    for i in range(1,9):
        s="#form1 > div.main > div.content > div.wrap > ul > li:nth-child("+str(i)+") > div > div > div > div.card-title"
        t=soup.select(s)
        t=str(t)
        temp=t[t.find(">")+1:t.find("</")]
        spot.append(temp)
    return(spot)
#google map api key = 'AIzaSyBJhlhzPGHpdM3Pr5rOBCAWpxkt_7GC27A'
def map(placeid,spot):
    for i in range(len(placeid)):
        print(spot[i])
        url='https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyBJhlhzPGHpdM3Pr5rOBCAWpxkt_7GC27A&place_id='
        url=url+str(placeid[i])
        data = request.urlopen(url).read().decode("utf-8")
        data = json.loads(data)
        try:
            print(data['result']['rating'])
        except:
            print('',end='')
        try:
            print(data['result']['formatted_phone_number'])
        except:
            print('',end='')
        try:
            print(data['result']['formatted_address'])
        except:
            print('',end='')
        try:
            print(data['result']['opening_hours']['weekday_text'])
        except:
            print('',end='')
        print("\n")

def getid(localist,spot,numberlist):
    ans=[]
    ans2=[]
    ans3=[]
    for i in range(len(localist)):
        n=0
        for j in range(8):
            translator = Translator()
            name=translator.translate(spot[int(i)-1][j],dest='en').text
            name=name.replace(' ','%20')
            url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=AIzaSyBJhlhzPGHpdM3Pr5rOBCAWpxkt_7GC27A&inputtype=textquery&language=zh-TW&input="+str(name)
            #print(url)
            data = request.urlopen(url).read().decode("utf-8")
            data = json.loads(data)
            if(data['status']=='OK'):
                #print(data["candidates"][0]["place_id"])
                url='https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyBJhlhzPGHpdM3Pr5rOBCAWpxkt_7GC27A&place_id='
                url=url+str(data["candidates"][0]["place_id"])
                data2 = request.urlopen(url).read().decode("utf-8")
                data2 = json.loads(data2)
                lat=float(data2['result']['geometry']['location']['lat'])
                lng=float(data2['result']['geometry']['location']['lng'])
                if(lng>118 and lng<122 and lat>21 and lat<27):
                    ans.append(data["candidates"][0]["place_id"])
                    n+=1
                    ans2.append(spot[i-1][j])
                    ans3.append(data2['result']['name'])
            if(n==8 or n==numberlist[i-1]):
                break
    return ans,ans2,ans3

def plan(placeid,ename):
    url='https://www.google.com/maps/dir/?api=1&travelmode=driving&origin=Hsinchu'
    if(len(placeid)>1):
        url=url+'&waypoints='+ename[0]
        for i in range(1,len(ename)-1):
            url=url+'%7C'+ename[i]
    url=url+'&destination='+ename[len(ename)-1]
    url=url.replace(' ','%20')
    return url
#input
weather=cwb(1,3)
location=input("Choose location(MIN:1)")
number=input("Number of tourist destinations(1~8)")

localist=location.split()
numberlist=number.split()
numberint=[]
localint=[]
for i in localist:
    if(int(i)>22 or int(i)<1):
        print('local error')
    localint.append(int(i))
for i in numberlist:
    if(int(i)>8 or int(i)<1):
        print('num error')
    numberint.append(int(i))

#localist=[1,2,3,4,5,6,7,8,9,10]
#numberlist=[5,5,5,5,5,5,5,5,5,5]
spot=[]
placeid=[]
ename=[]
for i in localint:
    spot.append(tb(weather[i]))
for i in spot:
    random.shuffle(i)
#print(spot)
placeid,spot,ename=getid(localint,spot,numberint)
#print(spot)
print("The number of destination is: %d"%len(placeid))
print("\n")
map(placeid,spot)
print(plan(placeid,ename))