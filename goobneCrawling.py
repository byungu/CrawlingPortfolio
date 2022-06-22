import pandas as pd
import time
from re import findall, sub
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def goobnestore(result):
    service = Service(r"F:\bigdata\WebDriver\chromedriver.exe")
    wd = webdriver.Chrome(service=service)
    goobne_URL = "https://www.goobne.co.kr/store/search_store.jsp"
    for i in range(1, 112):
        wd.get(goobne_URL)
        time.sleep(1)
        print(i)
        wd.execute_script("store.getList('%d')"%(i))
        time.sleep(1)
        html = wd.page_source
        soupGN = BeautifulSoup(html, 'html.parser')
        tag_tbody = soupGN.find("tbody")
        for store in tag_tbody.find_all('tr'):
            if len(store) <= 3:
                break
            store_name_GN = store.select('td')
            store_name = str(store_name_GN[0])
            store_name2 = findall('d>.{,10}', store_name)
            store_name3 = [sub('[a-z]', '', text) for text in store_name2]
            store_name4 = [sub('[!></-]', '', text) for text in store_name3]
            store_name5 = [''.join(str(text)) for text in store_name4]
            store_name6 = store_name5[0]
            print(store_name6)
            store_tel_GN = store.select('td.store_phone>a')
            store_tel = store_tel_GN[0].string
            store_address_GN = store.select('td.t_left>a')
            store_address = store_address_GN[0].string
            result.append([store_name6]+[store_tel]+[store_address])
    return result

def main():
    result = []
    print('>>>>>>>>>>>>>>>>>>>> Goobne Store Crawling start<<<<<<<<<<<<<<<<<<<<<')
    goobnestore(result)
    columns = ['name', 'tel', 'address']
    GN1_df = pd.DataFrame(result, columns=columns)
    GN1_df.to_csv('./굽네치킨_매장리스트.csv', encoding='cp949', index=True, mode='w')

if __name__ == '__main__':
    main()