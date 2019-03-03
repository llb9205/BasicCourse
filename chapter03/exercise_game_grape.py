import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class GameGrapeSpider:
    def start(self):
        self.crawl_index(1)

    def crawl_index(self, page):
        try:
            url = 'http://youxiputao.com/index/page/{}'.format(page)
            rsp = requests.get(url)
            soup = BeautifulSoup(rsp.text, 'lxml')
            for h4_node in soup.find('div', class_='news-box').find_all('h4'):
                a_node = h4_node.find('a')
                url_detail = urljoin(rsp.url, a_node['href'])
                self.crawl_detail(url_detail, page)

            # 分页操作
            if page == 1:
                li_node = soup.find('ul', class_='pagination hidden-xs').find_all('li')[-1]
                page_node = li_node.find('a')
                max_page = int(page_node['href'].split('/')[-1])
                for page in range(2, max_page + 1):
                    self.crawl_index(page)
        except:
            pass

    def crawl_detail(self, url, page):
        try:
            rsp = requests.get(url)
            soup = BeautifulSoup(rsp.text, 'lxml')
            title = soup.find('div', class_='title-box').find('h2', class_='title').text.strip()
            publish_time = soup.find('div', class_='title-box').find('div', class_='time').text.strip()
            article = soup.find('div', class_='info-box col-sm-12').text.strip()
            images = []
            images.append(soup.find('div', class_='cover').find('img')['src'])
            for img_node in soup.find('div', class_='info-box col-sm-12').find_all('img'):
                images.append(img_node['src'])
            data = {
                'title': title,
                'publish_time': publish_time,
                'article': article,
                'images': images,
            }
            print('第{}页新闻：'.format(page), data)
        except:
            pass


if __name__ == '__main__':
    GameGrapeSpider().start()
