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
            # 详情页“分类”字段有数据缺失现象，所以在列表页就把“分类”字段采集好
            meta = {
                'url': urljoin(rsp.url, a_node['href']),
                'name': a_node.text.strip(),
                'rank': item.find('div', class_='ranknum').text.strip(),
                'category': item.find('div', class_='mjinfo').text.split('/')[0].strip()
            }
            videos.append(meta)  # 详情页没有单独的名字标签、排名信息，这里先解析出来
        for tr_node in soup.find('table', class_='latesttable').find_all('tr', class_='Scontent1'):
            a_node = tr_node.find('a')
            meta = {
                'url': urljoin(rsp.url, a_node['href']),
                'name': a_node.text.strip(),
                'rank': tr_node.find('td').text.strip(),
                'category': tr_node.find_all('td')[2].text.strip(),
            }
            videos.append(meta)
        for tr_node in soup.find('table', class_='latesttable').find_all('tr', class_='Scontent'):
            a_node = tr_node.find('a')
            meta = {
                'url': urljoin(rsp.url, a_node['href']),
                'name': a_node.text.strip(),
                'rank': tr_node.find('td').text.strip(),
                'category': tr_node.find_all('td')[2].text.strip(),
            }
            videos.append(meta)

        for video in videos:
            rsp_detail = requests.get(video['url'])
            soup_detail = BeautifulSoup(rsp_detail.text, 'html.parser')
            video['poster'] = soup_detail.find('div', class_='seedpic').find('img')['src']
            info_nodes = soup_detail.find('div', class_='seedlink').find_all('span')
            video['update_day'] = info_nodes[0].text.split('：')[-1].strip()
            video['status'] = info_nodes[1].text.split('：')[-1].strip()
            video['last_update'] = info_nodes[3].text.split('：')[-1].strip()
            video['return_date'] = info_nodes[4].text.split('：')[-1].strip()
            video['countdown'] = info_nodes[5].text.split('：')[-1].strip()
            print(video)


if __name__ == '__main__':
    spider = TianTianSpider()
    spider.start()
