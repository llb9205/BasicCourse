import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


class _3dmSpider:
    def __init__(self):
        client = MongoClient(host='127.0.0.1', port=27017)
        self.coll = client.get_database('spider').get_collection('3dm')

    def start(self):
        self.crawl_index(1)

    def crawl_index(self, page):
        try:
            url = f'https://www.3dmgame.com/news_all_{page}/'
            rsp = requests.get(url)
            soup = BeautifulSoup(rsp.text, 'lxml')
            for li_node in soup.find('ul', class_='list').find_all('li'):
                a_node = li_node.find('a', class_='selectarcpost')
                self.crawl_detail(a_node['href'])

            if page == 1:
                a_node = soup.find('li', class_='last').find('a')
                max_page = int(a_node['data-page'])
                for new_page in range(2, max_page + 1):
                    self.crawl_index(new_page)
        except:
            pass

    def crawl_detail(self, url):
        try:
            rsp = requests.get(url)
            rsp.encoding = 'utf-8'
            soup = BeautifulSoup(rsp.text, 'html.parser')
            top_node = soup.find('div', class_='news_warp_top')
            title = top_node.find('h1', class_='bt').text.strip()
            time = top_node.find('div', class_='time').find('span').text.strip()
            resource = top_node.find('span', class_='weibo').text.strip()
            author = top_node.find('span', class_='name').text.strip()
            editor = top_node.find('span', class_='bianji').text.strip()

            center_node = soup.find('div', class_='news_warp_center')
            article = center_node.text.strip()
            images = []
            for img_node in center_node.find_all('img'):
                url = img_node['src']
                images.append(url)

            data = {
                'title': title,
                'time': time,
                'resource': resource,
                'author': author,
                'editor': editor,
                'article': article,
                'images': images,
            }

            self.coll.insert_one(data)
            print(data)
        except:
            pass


if __name__ == '__main__':
    _3dmSpider().start()
