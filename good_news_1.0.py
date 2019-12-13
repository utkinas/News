''''
Created on November 17, 2019

@author : Svetlana Morozov

'''

import sentiment_score
import bs4
import requests
import pandas as pd
#from yahoo-finance import Share
import matplotlib.finance as fin

#import quotes_historical_yahoo, candlestick,\
#     plot_day_summary, candlestick2, fetch_historical_yahoo

from sklearn.tree import DecisionTreeRegressor

#from scikit-learn import RegressionDesicionTree

import sys
import urllib3
import html5lib
import html.parser
from html.parser import HTMLParser
import re



#BASE_URL = "https://www.google.com/finance"
#BASE_URL = "https://www.google.com/finance?tab=we&authuser=0"
BASE_URL = "https://www.sfgate.com/bayarea"


#BASE_URL = "https://www.bloomberg.com"
columns= ['title','rank','url','text']


print("BASE_URL : ",BASE_URL)

def openLink(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    return soup

def colRename(df,cols):
    for i in range(0,len(cols)):
        df.rename(columns = {i: cols[i]},inplace=True)


page = requests.get(BASE_URL)
soup = bs4.BeautifulSoup(page.content, 'html.parser')

mainPage = soup.findAll('a', {"class":"hdn-analytics"})


arrNewsLinks=[]
arrNews=[]

#Getting links from main page

print("Getting links from main page  ... ")
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

#Getting text for main articles
print("Getting text for main articles ... ")
for index, row in dfNewsLinks.iterrows():

    article=''
    content = openLink(row[1]).findAll('p')
    for item in content:
        article = article + ' ' + item.text


    arrNews.append([row[0],row[1],article])



dfNews = pd.DataFrame(arrNews).drop_duplicates()

# Read sentiment dictionary
sent_map = sentiment_score.init_sentiment()


# Running sentiment analysis (ranking stories)

print("Running sentiment analysis (ranking stories)")
finalNewsList=[]

for index, row in dfNews.iterrows():
    rank = sentiment_score.sentiment_score(row[2], sent_map)
    finalNewsList.append([row[0],rank,row[1],row[2]])



dfAllNews = pd.DataFrame(finalNewsList)
dfFinalNews = dfAllNews.drop_duplicates()

colRename(dfFinalNews,columns)
dfNegative = dfFinalNews[dfFinalNews['rank'] <0]
dfPositive = dfFinalNews[dfFinalNews['rank'] >0]
dfNeutral = dfFinalNews[dfFinalNews['rank'] ==0]

print ("="*20)
print("Ran ranking for "+ str(len(dfFinalNews))+ " articles")
print("Positive news : ", len(dfPositive))
print("Negative news : ", len(dfNegative))
print("Positive news : ", len(dfNeutral))
print ("="*20)

dfFinalNewsSorted = dfFinalNews.sort_values('rank',ascending=True)

print ("Saving the results of ranking into a file ...")
dfFinalNewsSorted.to_excel('finalNews.xlsx',sheet_name='news',index=False)

print("finished")

print ("="*20)

