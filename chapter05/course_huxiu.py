import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time


class HuXiuSpider:
    def __init__(self):
        client = MongoClient(host='127.0.0.1', port=27017)
        self.coll = client.get_database('spider').get_collection('huxiu')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

    # 抓取首页html
    def start(self):
        try:
            url = 'https://www.huxiu.com/'
            rsp = requests.get(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(rsp.text, 'lxml')
            for h2_node in soup.find('div', class_='mod-info-flow').find_all('h2'):
                href = h2_node.find('a')['href']
                url_news = urljoin(rsp.url, href)
                self.crawl_detail(url_news)

            # 使用正则表达式匹配字符串，(.*？)就是想要匹配的部分，带上问号表示只匹配一次
            regex_res = re.findall(r'huxiu_hash_code=\'(.*?)\'', rsp.text)
            if regex_res is not None:
                self.hash_code = regex_res[0]
                self.crawl_index_ajax(2)
        except:
            pass

    # 抓取ajax页面
    def crawl_index_ajax(self, page):
        try:
            req_data = {
                'huxiu_hash_code': self.hash_code,
                'page': page,
                'last_dateline': int(time.time()),  # 10位时间戳。以后看到15开头、10位或13位整数，就要注意这是不是时间戳
            }
            url = 'https://www.huxiu.com/v2_action/article_list'
            rsp = requests.post(url=url, data=req_data, headers=self.headers, timeout=30)  # 发送post请求，带上表单数据
            html = rsp.json()['data']  # requsts返回的对象内置了json()函数，可以方便的转成字典
            soup = BeautifulSoup(html, 'lxml')
            for h2_node in soup.find_all('h2'):
                href = h2_node.find('a')['href']
                url_news = urljoin(rsp.url, href)
                self.crawl_detail(url_news)

            if page == 2:
                # 这里可以拿到total_page进行分页
                max_page = int(rsp.json()['total_page'])
                for new_page in range(3, max_page + 1):
                    self.crawl_index_ajax(new_page)
        except:
            pass

    # 抓取新闻详情
    def crawl_detail(self, url):
        try:
            rsp = requests.get(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(rsp.text, 'lxml')
            title = soup.find('div', class_='article-wrap').find('h1', class_='t-h1').text.strip()
            author = soup.find('span', class_='author-name').text.strip()
            try:
                publish_time = soup.find('span', class_='article-time pull-left').text.strip()
                collect = soup.find('span', class_='article-share pull-left').text.strip()
                comment = soup.find('span', class_='article-pl pull-left').text.strip()
                category = soup.find('a', class_='column-link').text.strip()
            except AttributeError:
                # 解析不同页面结构
                publish_time = soup.find('span', class_='article-time').text.strip()
                collect = soup.find('span', class_='article-share').text.strip()
                comment = soup.find('span', class_='article-pl').text.strip()
                category = ''
            article = soup.find('div', class_='article-content-wrap').text.strip()
            images = []
            images.append(soup.find('div', class_='article-img-box').find('img')['src'])  # 文章头图
            for img_node in soup.find('div', class_='article-content-wrap').find_all('img'):
                images.append(img_node['src'])

            data = {
                'title': title,
                'author': author,
                'publish_time': publish_time,
                'collect': collect,
                'comment': comment,
                'category': category,
                'article': article,
                'images': images,
                'url': url
            }

            self.coll.insert_one(data)
            print(data)
        except:
            pass


if __name__ == '__main__':
    HuXiuSpider().start()
