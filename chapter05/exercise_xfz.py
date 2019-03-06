import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from pymongo import MongoClient


class XFZSpider:
    def __init__(self):
        client = MongoClient(host='127.0.0.1', port=27017)
        self.coll = client.get_database('spider').get_collection('xfz')

    def start(self):
        try:
            rsp = requests.get('https://www.xfz.cn/', timeout=30)
            soup = BeautifulSoup(rsp.text, 'lxml')
            for a_node in soup.find('ul', class_='news-list').find_all('a', class_='li-container'):
                url_new = urljoin(rsp.url, a_node['href'])
                # self.crawl_detail(url_new)
            self.crawl_index(2)
        except:
            pass

    def crawl_index(self, page):
        try:
            url = f'https://www.xfz.cn/api/website/articles'
            params = {'p': page, 'n': 20, 'type': ''}
            rsp = requests.get(url, params=params, timeout=30)
            if 'uid' in rsp.text:
                for item in rsp.json()['data']:
                    url = f'https://www.xfz.cn/post/{item["uid"]}.html'
                    self.crawl_detail(url)
                self.crawl_index(page + 1)
        except:
            pass

    def crawl_detail(self, url):
        rsp = requests.get(url)

        soup = BeautifulSoup(rsp.text, 'lxml')
        title = soup.find('h1', class_='title').text.strip()
        author = soup.find('span', class_='author-name').text.strip()
        publish_time = soup.find('span', class_='time').text.strip()
        category = soup.find('span', class_='article-type').text.strip()
        summary = soup.find('div', class_='content-lead').text.strip()
        article = soup.find('div', class_='content-detail').text.strip()
        images = []
        for img_node in soup.find('div', class_='content-detail').find_all('img'):
            images.append(img_node['src'])

        data = {
            'title': title,
            'url': url,
            'author': author,
            'publish_time': publish_time,
            'category': category,
            'summary': summary,
            'article': article,
            'images': images,
        }

        self.coll.insert_one(data)
        print(data)


if __name__ == '__main__':
    XFZSpider().start()
