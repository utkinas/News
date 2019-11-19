''''
Created on November 17, 2019

@author : Svetlana Morozov

'''

import sentiment_score
import sys

import urllib3
import bs4
import html5lib
import html.parser
from html.parser import HTMLParser
import requests
import pandas as pd
import re



#BASE_URL = "https://www.google.com/finance"
#BASE_URL = "https://www.google.com/finance?tab=we&authuser=0"
BASE_URL = "https://www.sfgate.com/bayarea"


def openLink(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    return soup



page = requests.get(BASE_URL)
soup = bs4.BeautifulSoup(page.content, 'html.parser')
mainPage = soup.findAll('a', {"class":"hdn-analytics"})


arrNewsLinks=[]
arrNews=[]

for item in mainPage:
    url = item.get('href')
    if "http" in url:
        link = url
    else:
        link = BASE_URL + url
    title = item.getText()
    if title.rstrip().lstrip() !="" and len(title.split(" ")) > 6 and url !="" and url !="/":
        arrNewsLinks.append([title.rstrip().lstrip(), link])


dfNewsLinks = pd.DataFrame(arrNewsLinks).drop_duplicates()
#dfNews.to_csv('news.csv')



for index, row in dfNewsLinks.iterrows():

    article=''
    content = openLink(row[1]).findAll('p')
    for item in content:
        article = article + ' ' + item.text


    arrNews.append([row[0],row[1],article])



dfNews = pd.DataFrame(arrNews).drop_duplicates()


sent_map = sentiment_score.init_sentiment()


finalNewsList=[]
for index, row in dfNews.iterrows():
    rank = sentiment_score.sentiment_score(row[2], sent_map)
    finalNewsList.append([row[0],rank,row[1],row[2]])



dfAllNews = pd.DataFrame(finalNewsList)
dfFinalNews = dfAllNews.drop_duplicates()

dfFinalNews.to_csv('finalNews.csv')

print("finished")

print ("="*20)

