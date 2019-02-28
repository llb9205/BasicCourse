import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class PhoneHeavenSpider:
    def start(self):
        self.crawl_index(1)

    # 抓取列表页数据，包含第一页。
    def crawl_index(self, page):
        try:
            if page == 1:
                url = 'https://www.xpgod.com/shouji/news/zixun.html'
            else:
                url = 'https://www.xpgod.com/shouji/news/zixun_{}.html'.format(page)
            rsp = requests.get(url)
            rsp.encoding = 'gbk'  # 指定编码方式

            soup = BeautifulSoup(rsp.text, 'lxml')  # 更强大的解析库lxml
            for div_node in soup.find_all('div', class_='zixun_li_title'):
                a_node = div_node.find('a')
                href = a_node['href']
                url_detail = urljoin(rsp.url, href)
                self.crawl_detail(url_detail, page)  # 抓取新闻url，抓取具体数据

            if page == 1:  # 翻页处理，只有第1页需要
                li_node = soup.find('ul', class_='fenye_ul').find_all('li')[-3]
                max_page = int(li_node.text.strip())  # 拿到的text是字符串类型，需要转为int类型
                for new_page in range(2, max_page + 1):  # 2 ~ max_page+1页，不包含第max_page+1
                    self.crawl_index(new_page)  # 继续调用自身，写上return避免迭代过多导致异常
        except:
            pass

    # 抓取新闻详情数据
    def crawl_detail(self, url, page):
        try:
            rsp = requests.get(url)
            rsp.encoding = 'gbk'

            soup = BeautifulSoup(rsp.text, 'lxml')
            title = soup.find('div', class_='youxizt_top_title').text.strip()
            info = soup.find('div', class_='top_others_lf').text.strip()  # 包含时间、作者信息
            infos = info.split('|')  # 使用split()对字符串进行切割
            publish_time = infos[0].split('：')[-1].strip()  # 发布时间
            author = infos[1].split('：')[-1].strip()  # 作者
            summary = soup.find('div', class_='zxxq_main_jianjie').text.strip()  # 简介
            article = soup.find('div', class_='zxxq_main_txt').text.strip()  # 文章
            images = []  # 图片
            for node in soup.find('div', class_='zxxq_main_txt').find_all('img'):
                src = node['src']
                img_url = urljoin(rsp.url, src)
                images.append(img_url)

            data = {
                'title': title,
                'publish_time': publish_time,
                'author': author,
                'summary': summary,
                'article': article,
                'images': images,
            }
            print('第{}页新闻：'.format(page), data)
        except:
            pass


if __name__ == '__main__':
    PhoneHeavenSpider().start()
