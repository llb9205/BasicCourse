import requests


class PhoneHeavenSpider:
    def start(self):
        rsp = requests.get('https://www.xpgod.com/shouji/news/zixun.html')
        print(rsp.text)


if __name__ == '__main__':
    PhoneHeavenSpider().start()
