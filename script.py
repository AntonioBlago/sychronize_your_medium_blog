from bs4 import BeautifulSoup
import urllib.request
import re
from linkpreview import link_preview
import pandas as pd


def fetch(url):
    url = "http://" + str(url)
    req = urllib.request.Request(url, headers = {'User-agent': 'your bot 0.1'})
    response = urllib.request.urlopen(req)
    html = response.read()
    # Parsing response
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find_all("a")
    list_urls = []
    for item in text:
        item = str(item)
        pos = item.find('href="/')
        if pos is not None:
            if pos > 0 and item.find("user_profile")>0:
                result = re.search(r'href="\/+([a-z])\w+', item)
                if result:
                    try:
                        start = result.start()
                        end_item = item[start:]
                        end = re.search(r'-"', end_item).end()
    
                        url_extract_pos = item[start:start+end]
                        url_final = str(url) + url_extract_pos[6:-1]
    
                        if url_final not in list_urls:
                            list_urls.append(url_final)
                            print(url_final)
                    except:
                        print("error")
                        
    return list_urls

def get_previews(list_urls):

    list_of_links = []
    for i in list_urls:
        preview = link_preview(i)
    
        dic_preview = {"title": preview.title,
                       "description": preview.description,
                       "image": preview.image,
                       "force_title": preview.force_title,
                       "absolute_image": preview.absolute_image,
                       "url": i}
        list_of_links.append(dic_preview)
    
    return pd.DataFrame(list_of_links)

def upload(df):
    
    ## define your upload function for your database here
    return df


if __name__ == '__main__':
    list_urls = fetch("antonioblago.medium.com")
    df = get_previews(list_urls)
    upload(df)
    print(df.head())
