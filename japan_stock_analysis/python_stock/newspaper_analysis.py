import newspaper
import MeCab
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from lxml import html


NIKKEI_URL="http://www.nikkei.com"
NIKKEI_TECH_URL="http://www.nikkei.com/tech/"
NIKKEI_MRK_URL="http://www.nikkei.com/markets/" # for test including stock information

YAHOO_URL="http://www.yahoo.co.jp"
YAHOO_STOCK_URL="http://news.yahoo.co.jp/hl?c=biz"

SINA_URL="http://www.sina.com.cn"
SINA_FINANCE_URL="http://finance.sina.com.cn"
LANG_ENM=["zh","jp","en"]

def build_news(news_url,lang):
    print("news object building.....")
    return newspaper.build(news_url) # for test
    #return newspaper.build(news_url, language=lang)

def get_category_list(news_object):
    print("category url creating.....")
    url_list=[]
    for item in news_object.category_urls():
        url_list.append(item)

    return url_list

def get_article_list(news_object):
    print("getting article list .....")
    article_list=[]
    for item in news_object.articles:
        article_list.append(item)
    return article_list

def get_article_info_list(article_object):
    #info_list={"title":[],"article":[],"html":"","keywords":"","nlp":""}
    #info_list={}
    print("article downloading.....")
    try:
        article_object.download()
        try:
            article_object.parse()
            try:
                article_object.nlp()
            except:
                print("article nlp processing error!!")
                print("article url:",article_object.url)
        except:
            print("article parsing error!!")
            print("article url:",article_object.url)
    except:
        print("article download error!!")
        print("article url:",article_object.url)

    return article_object

def main():
    #url=YAHOO_STOCK_URL
    nikkei_focus_on_url="http://www.nikkei.com/markets/kabu/page/?uah=DF_SEC8_C1_030&n_cid=DSMMAA09"
    nikkei_kabu_new_url="http://www.nikkei.com/markets/kabu/page/?uah=DF_SEC8_C1_020&n_cid=DSMMAA09"
    url=NIKKEI_MRK_URL
    page = requests.get(nikkei_focus_on_url)
    tree = html.fromstring(page.content)
    print(tree)
    #data = tree.xpath('//div[@class="m-article line a-clr"]')
    #print(data)

    lang=None
    news_object=build_news(url,lang)
    cat_list=get_category_list(news_object)
    print("cat_list:",cat_list)
    article_object_list=get_article_list(news_object)
    print("article_object_list:",article_object_list)
    #info=get_article_info_list(article_object_list[0])
    #print(info.text)
    info_list=[]
    for data in article_object_list:
        print("downloading data.....")
        article_info=get_article_info_list(data)
        info_list.append(article_info)
        print("article title:",article_info.title)


if __name__=="__main__":
    main()
