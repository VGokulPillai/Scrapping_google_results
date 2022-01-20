from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse
import requests
import pandas as pd
import numpy as np
import time
from urllib.parse import urlparse

features_list = ['fruitcompany'] #insert keywords here

def get_links(soup):
  
    link_list = []
    divs = soup.find_all('div', class_='kCrYT')
    for div in divs:
        anchor = div.find_all('a')
        for a in anchor:
            link = a['href']
            link_list.append(link)
    return link_list


def clean_link(link):
    url = urlparse(link)
    qs = parse_qs(url.query)
    new_link = qs['q'][0]
    return new_link


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
code = 'UK'

headers = {'User-agent': USER_AGENT}

for query in features_list:
    URL = f"https://google.com/search?q={query}&cr=country{code}&num=99" #defining url to scrape from
    next_url = URL
    pages = 0
    links = 0
    list_of_links = []
    hostname = []
    
    while True:
        time.sleep(np.random.randint(2,6)) #random delay to avoid gettig banned
        resp = requests.get(next_url, headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            
            link_list = get_links(soup)
            
            for link in link_list:
                wanted_link = clean_link(link)
                obj = urlparse(wanted_link)
                hostname.append(obj)
                list_of_links.append(wanted_link)

                links += 1
  
            
            df = pd.DataFrame(list_of_links)
            df1 = pd.DataFrame(hostname)
            df.to_csv('link_list.csv', mode='a', header=False)
            df1.to_csv('hostname_list.csv', mode='a', header=False)
            
            nexto = soup.find('a', class_="nBDE1b G5eFlf")
            
            pages += 1
            if nexto == None:
                break
            else:
                next_url = 'https://www.google.com' + nexto['href']
                print(pages)
        else:
            print('Scraping stopped / blocked!!')
            print(f"query: {query}, page number: {str(pages)}")
            break
    break
    
