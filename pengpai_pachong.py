import requests
from lxml import etree
from fake_useragent import UserAgent
import re
import time

ua = UserAgent()
# print(ua.ie) 随机输出ie浏览器的一个UserAgent
# print(ua.chrome) 随机输出chrome浏览器的一个UserAgent

class PengpaiSpider:
    def __init__(self):
        self.start_url = 'https://www.thepaper.cn/'
        self.headers = {'user-agent': ua.chrome}
        self.url_temp = 'https://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=2218110,2218366,2217315,2218351,&pageidx={}'

    def parse(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode('utf-8')

    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(100)]

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@class='news_li']")
        content_list = []
        for div in div_list:
            item = {}
            item['title'] = div.xpath("./h2/a/text()")[0] if len(div.xpath("./h2/a/text()"))>0 else None
            item['detail'] = re.sub(r'\n| ','',div.xpath("./p/text()")[0]) if len(div.xpath("./p/text()"))>0 else None
            item['author'] = div.xpath("./div[@class='pdtt_trbs']/a/text()")[0] if len(div.xpath("./div[@class='pdtt_trbs']/a/text()"))>0 else None
            item['release_time'] = div.xpath("./div[@class='pdtt_trbs']/span[1]/text()")[0] if len(div.xpath("./div[@class='pdtt_trbs']/span[1]/text()"))>0 else None
            item['comment_num'] = div.xpath("./div[@class='pdtt_trbs']/span[last()]/text()")[0] if len(div.xpath("./div[@class='pdtt_trbs']/span[last()]/text()"))>0 else None
            print(item)
            content_list.append(item)
        return content_list

    def save_content_list(self, content_list):
        pass

    def run(self):
        html_str = self.parse(self.start_url)
        content_list = self.get_content_list(html_str)
        self.save_content_list(content_list)
        url_list = self.get_url_list()
        for url in url_list:
            time.sleep(1)
            response_html = self.parse(url)
            content = self.get_content_list(response_html)
            self.save_content_list(content)



if __name__ == '__main__':
    pengpai = PengpaiSpider()
    pengpai.run()