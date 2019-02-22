import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class GameGrapeSpider:  # 声明一个叫“GameGrapeSpider（游戏葡萄爬虫）”的类
    def start(self):  # 爬虫的启动函数
        response = requests.get('http://youxiputao.com/')
        soup = BeautifulSoup(response.text, 'html.parser')
        for li_node in soup.find('ul', {'class': 'news-list'}).find_all('li'):
            a_node = li_node.find('h4').find('a')
            href = a_node['href']
            url = urljoin(response.url, href)

            response_detail = requests.get(url)
            soup_detail = BeautifulSoup(response_detail.text, 'html.parser')
            title = soup_detail.find('h2', class_='title').text
            publish_time = soup_detail.find('div', {'class': 'pull-left'}).text.strip()
            article = soup_detail.find('div', {'class': 'info-detail'}).text.strip()
            images = []  # 用于存放文章中的图片
            for img_node in soup_detail.find('div', {'class': 'info-detail'}).find_all('img'):
                img_url = img_node['src']
                images.append(img_url)
            cover = soup_detail.find('div', class_='cover').find('img')['src']  # 封面图片
            images.append(cover)
            data = {'title': title, 'publish_time': publish_time, 'images': images, 'article': article}
            print(data)


if __name__ == '__main__':  # 表示程序入口，如果我们写的game_grape模块被其他代码导入，则不会执行if后的内容
    spider = GameGrapeSpider()  # 创建一个对象
    spider.start()  # 启动爬虫
