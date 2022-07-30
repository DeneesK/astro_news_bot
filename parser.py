import json
import requests
from bs4 import BeautifulSoup


url = 'https://astronomy.com/news'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

def get_news():
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        articles_dict = {}
        soup = BeautifulSoup(r.text, 'lxml')
        article_cards = soup.find_all('div', class_= 'dataSection')
        i = 0
        for article in article_cards:
            i += 1
            article_date = article.find('div', class_='dateHeader').text.strip()
            article_title = article.find('div', class_='content withImage').find("a").text
            article_descr = article.find('div', class_='snippet').text.strip()
            article_url = article.find('div', class_='content withImage').find("a").get("href")
            articles_dict[i] = {
                'Date': article_date,
                'Title': article_title,
                'Description': article_descr,
                'Link': f'https://astronomy.com/{article_url}'
            }

        with open ('news.json', 'w', encoding='UTF-8') as file:
            json.dump(articles_dict, file, indent=4, ensure_ascii=False)
    else:
        print('It is not aviable now')
