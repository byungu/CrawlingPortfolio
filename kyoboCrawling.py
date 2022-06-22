import pandas as pd
import time
from re import findall, sub
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(r"F:\bigdata\WebDriver\chromedriver.exe")
wd = webdriver.Chrome(service=service)
kyobo_URL = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=D0a"
ran = ['A', 'B', 'C', '08']  # , 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Q', 'R', 'S', 'T', 'U', 'V', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', '08']

def controller(result):
    html = wd.page_source
    soupKB = BeautifulSoup(html, 'html.parser')
    kyobo_cate_KB = soupKB.select('ul.list_sub_category>li>a>strong')
    kyobo_cate = kyobo_cate_KB[0].string
    tag_ul = soupKB.find("ul", attrs={'class': 'list_type01'})
    for store in tag_ul.select('li>div.detail'):
        kyobo_name_KB = store.select('div.detail>div.title>a>strong')
        kyobo_name = kyobo_name_KB[0].string
        kyobo_author_KB = store.select('li>div.detail>div.author')
        kyobo_author1 = str(kyobo_author_KB[0])
        kyobo_author2 = findall('\w.{1,}', kyobo_author1)
        kyobo_author = kyobo_author2[1]
        kyobo_publisher1 = kyobo_author2[-3].split()
        del kyobo_publisher1[0]
        del kyobo_publisher1[0]
        kyobo_publisher = ''.join(s for s in kyobo_publisher1)
        print(kyobo_publisher)
        kyobo_price_KB = store.select('li>div.detail>div.price>strong')
        kyobo_price = kyobo_price_KB[0].string
        result.append([kyobo_cate] + [kyobo_name] + [kyobo_author] + [kyobo_publisher] + [kyobo_price])


def kyobobestseller(result):

    for sell in ran:
        wd.get(kyobo_URL)
        time.sleep(1)
        if (sell == 'A'):
            wd.execute_script("goCateList('KOR', '%s', 'DAa')" % (sell))
            time.sleep(1)
            controller(result)

        elif (sell == '08'):
            wd.execute_script("goCateList('EBK', '%s', 'DBk')" % (sell))
            time.sleep(1)
            controller(result)

        elif (sell != 'A' and sell != '08' ):
            wd.execute_script("goCateList('KOR', '%s', 'DAb')" % (sell))
            time.sleep(1)
            controller(result)

    return result


def savecsv(result):
    columns = ['cate', 'name', 'author', 'publisher', 'price']
    KB_df = pd.DataFrame(result, columns=columns)
    KB_df.to_csv('./교보문고_베스트셀러_목록.csv', encoding='cp949', index=True, mode='w')


def main():
    result = []
    print('>>>>>>>>>>>>>>>>KYOBO BEST Seller Crawling start <<<<<<<<<<<<<<<<<')
    kyobobestseller(result)
    savecsv(result)
    wd.quit()

if __name__ == '__main__':
    main()

