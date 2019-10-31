import requests,json,webbrowser,lxml
from datetime import datetime
import bs4
from bs4 import BeautifulSoup
import HTMLParser
from lxml import etree
import re

def SupremeURL(keyword, color, catagory):
    startlink = 'http://www.supremenewyork.com/shop/all/{}'.format(catagory)
    r= requests.get(startlink)
    test = bs4.BeautifulSoup(r.text,'lxml')
    wordlist=[]
    url = ""
    for a in test.find_all('a',href=True):
        b = str(a)
        if color in b.lower() or keyword in b.lower():
            word = b.split('"')[3]
            if word not in wordlist:
                wordlist.append(word)
            else:
                url='http://www.supremenewyork.com' + str(word)
                break
    return url

def SupremeData(size,url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text,'html.parser')
    fourth = soup.find(id = 'cctrl')
    fourthy = str(fourth)
    st = ''
    s = ''
    check =fourthy.split(' ')
    #print(fourth.prettify())
    for x in check:
        x = x.lower()
        if size.lower() == "one size":
            if 'value' in x and "/><a" in x:
                test = x.split('"')
                s = test[1]
        if size in x and 'value' in x:
            truesize = x.split(">")
            secondtruesize = truesize[1].split('<')
            if len(secondtruesize[0]) == len(size):
                test = x.split('"')
                s = test[1]
        if '/><fieldset><input' in x or '/><fieldset><select' in x:
            test = x.split('"')
            st = test[1]
    action = (soup.find('form',{'class':'add'})['action'])
    #stag = (soup.find('form',{'id':'s'})['value']) #Work on Here
    action = str(action)
    #stag = str(stag)
    #print(stag)
    return([s,st,action])

#print(SupremeURL("boxer","white","accessories"))
