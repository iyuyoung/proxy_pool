import requests
from bs4 import BeautifulSoup
import re
from new.untils.RedisClient import r


class proxy():
    def __init__(self):
        self.key = 'proxy'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
        }

    '''
    获取网站源代码
    '''

    def getContent(self):
        url = 'http://www.goubanjia.com/'
        data = requests.get(url, headers=self.headers)
        self.parse(data.text)

    '''
    解析源代码
    '''

    def parse(self, data):
        soup = BeautifulSoup(data, 'html.parser')
        result = soup.find_all('td', class_='ip')
        for x in result:
            port = x.find(name='span', class_='port').attrs
            port = port['class'][-1]
            port = self.parse_port(port)
            data = re.compile('<p.*?/p>|<span class="port.*">.*</span>?|<.*?>', re.S)
            res = re.sub(data, '', str(x))
            r.add(self.key, res + str(port))

    '''
    解密端口号
    '''

    def parse_port(self, port):
        string = 'ABCDEFGHIZ'
        arr = list(port)
        lists = []
        for x in range(0, len(arr)):
            lists.append(string.find(arr[x]))

        ports = ''.join(str(x) for x in lists)
        return int(ports) >> 3

    '''
    随机获取代理地址
    '''

    def random(self):
        url = 'https://www.baidu.com'
        value = r.random(self.key)
        if value is None:
            self.getContent()
        proxies = {"http": "http://" + value.decode("utf-8")}
        try:
            data = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=5)
            if data.status_code is not 200:
                print('删除')
                r.delete(self.key, value)
                self.random()
            else:
                return 'http://' + value.decode("utf-8")
        except:
            print('删除')
            r.delete(self.key, value)
            self.random()


proxy = proxy()

ip=proxy.random()
print(ip)
