import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


class TianTianSpider:
    # __init__()函数在对象初始化的时候会自动调用
    def __init__(self):
        file = open('tv_rank.csv', 'w', newline='')
        self.writer = csv.writer(file)
        self.writer.writerow(['链接', '名称', '排名', '分类', '更新日', '状态', '最后更新', '回归', '倒计时'])  # 插入表头

    def start(self):
        self.crawl_index(1)

    def crawl_index(self, page):
        try:
            if page == 1:
                url = 'http://www.ttmeiju.vip/summary.html'
            else:
                # 更强大的字符串格式化方式：f-string，仅支持python3.6及以上！！！
                url = f'http://www.ttmeiju.vip/index.php/summary/index/p/{page}.html'

            rsp = requests.get(url)
            soup = BeautifulSoup(rsp.text, 'lxml')
            videos = []
            # 只有第一页才有top3列表，但是其他页面寻找<div class="ranktop3">标签时返回空列表，不影响逻辑
            for item in soup.find_all('div', class_='ranktop3'):
                a_node = item.find('div', class_='mjtit').find('a')
                video = {
                    'url': urljoin(rsp.url, a_node['href']),
                    'name': a_node.text.strip(),
                    'rank': item.find('div', class_='ranknum').text.strip(),
                    'category': item.find('div', class_='mjinfo').text.split('/')[0].strip()
                }
                videos.append(video)
            for tr_node in soup.find('table', class_='latesttable').find_all('tr', class_='Scontent1'):
                a_node = tr_node.find('a')
                video = {
                    'url': urljoin(rsp.url, a_node['href']),
                    'name': a_node.text.strip(),
                    'rank': tr_node.find('td').text.strip(),
                    'category': tr_node.find_all('td')[2].text.strip(),
                }
                videos.append(video)
            for tr_node in soup.find('table', class_='latesttable').find_all('tr', class_='Scontent'):
                a_node = tr_node.find('a')
                video = {
                    'url': urljoin(rsp.url, a_node['href']),
                    'name': a_node.text.strip(),
                    'rank': tr_node.find('td').text.strip(),
                    'category': tr_node.find_all('td')[2].text.strip(),
                }
                videos.append(video)

            for video in videos:
                self.crawl_detail(video)

            # 分页处理
            if page == 1:
                max_page = int(soup.find('a', class_='end').text.strip())
                for new_page in range(2, max_page + 1):
                    self.crawl_index(new_page)
        except:
            pass

    def crawl_detail(self, video):
        try:
            rsp = requests.get(video['url'])
            soup = BeautifulSoup(rsp.text, 'html.parser')
            info_nodes = soup.find('div', class_='seedlink').find_all('span')
            video['update_day'] = info_nodes[0].text.split('：')[-1].strip()
            video['status'] = info_nodes[1].text.split('：')[-1].strip()
            video['last_update'] = info_nodes[3].text.split('：')[-1].strip()
            video['return_date'] = info_nodes[4].text.split('：')[-1].strip()
            video['countdown'] = info_nodes[5].text.split('：')[-1].strip()

            # csv文件写入行时接收一个列表，这里把字典的所有值写入
            self.writer.writerow(video.values())
            print(video)
        except:
            pass


if __name__ == '__main__':
    TianTianSpider().start()
