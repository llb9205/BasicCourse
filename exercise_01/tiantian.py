import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class TianTianSpider:
    def start(self):
        rsp = requests.get('http://www.ttmeiju.vip/summary.html')
        soup = BeautifulSoup(rsp.text, 'lxml')
        videos = []  # url列表，包含三部分：top3列表、<tr class="Scontent1">列表、<tr class="Scontent">列表
        for item in soup.find_all('div', class_='ranktop3'):
            a_node = item.find('div', class_='mjtit').find('a')
            meta = {
                'url': urljoin(rsp.url, a_node['href']),
                'name': a_node.text.strip(),
                'rank': item.find('div', class_='ranknum').text.strip(),
            }
            videos.append(meta)  # 详情页没有单独的名字标签、排名信息，这里先解析出来
        for tr_node in soup.find('table', class_='latesttable').find_all('tr', class_='Scontent1'):
            a_node = tr_node.find('a')
            meta = {
                'url': urljoin(rsp.url, a_node['href']),
                'name': a_node.text.strip(),
                'rank': tr_node.find('td').text.strip()
            }
            videos.append(meta)
        for tr_node in soup.find('table', class_='latesttable').find_all('tr', class_='Scontent'):
            a_node = tr_node.find('a')
            meta = {
                'url': urljoin(rsp.url, a_node['href']),
                'name': a_node.text.strip(),
                'rank': tr_node.find('td').text.strip()
            }
            videos.append(meta)

        for video in videos:
            rsp_detail = requests.get(video['url'])
            soup_detail = BeautifulSoup(rsp_detail.text, 'html.parser')
            video['poster'] = soup_detail.find('div', class_='seedpic').find('img')['src']
            info_nodes = soup_detail.find('div', class_='seedlink').find_all('span')
            video['update_day'] = info_nodes[0]
            video['status'] = info_nodes[1]
            video['category'] = info_nodes[2]
            video['last_update'] = info_nodes[3]
            video['return_date'] = info_nodes[4]
            video['countdown'] = info_nodes[5]
            print(video)


if __name__ == '__main__':
    spider = TianTianSpider()
    spider.start()
