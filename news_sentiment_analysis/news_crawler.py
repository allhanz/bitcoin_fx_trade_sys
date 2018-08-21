import os
import sys
import pandas as pd
import newspaper #not support japanese parse process
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

#5 Things You Need to Know about Sentiment Analysis and Classification
#https://www.kdnuggets.com/2018/03/5-things-sentiment-analysis-classification.html

url="https://news.google.com/?hl=ja&gl=JP&ceid=JP%3Aja"
url_css="https://news.google.com/news/rss?ned=jp&gl=JP&hl=ja" # japanese version
def newspaper_test(url):
    paper=newspaper.build(url,language='jp')
    for category in paper.category_urls():
        print(category)
    articles_list=paper.articles
    if len(articles_list)>0:
        for item in articles_list:
            item.download()
            item.parse()
            print(item.text)
    else:
        print("canot find the articales....")

def test():
    Client=urlopen(url_css)
    #Client=urlopen(url)
    xml_page=Client.read()
    Client.close()

    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    # Print news title, url and publish date
    for news in news_list:
        print(news.title.text)
        print(news.link.text)
        print(news.pubDate.text)
        print("-"*60)

def main():
    print("not tested....")
    newspaper_test(url)

if __name__=="__main__":
    main()