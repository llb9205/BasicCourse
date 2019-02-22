import requests
from bs4 import BeautifulSoup


class GameResSpider:
    def start(self):
        rsp = requests.get('https://www.3dmgame.com/news/')
        soup = BeautifulSoup(rsp.text, 'html.parser')
        for li_node in soup.find('ul', class_='list').find_all('li'):
            a_node = li_node.find('a', class_='selectarcpost')
            url = a_node['href']
            rsp_detail = requests.get(url)  # 要设置编码格式为utf-8，否则出现乱码。
            rsp_detail.encoding = 'utf-8'
            soup_detail = BeautifulSoup(rsp_detail.text, 'html.parser')
            top_node = soup_detail.find('div', class_='news_warp_top')  # 网页源码为“ news_warp_top”，需要把第一个空格去掉
            title = top_node.find('h1', class_='bt').text.strip()
            time = top_node.find('div', class_='time').find('span').text.strip()
            resource = top_node.find('span', class_='weibo').text.strip()
            author = top_node.find('span', class_='name').text.strip()
            editor = top_node.find('span', class_='bianji').text.strip()

            center_node = soup_detail.find('div', class_='news_warp_center')
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
            print(data)


if __name__ == '__main__':
    spider = GameResSpider()
    spider.start()
