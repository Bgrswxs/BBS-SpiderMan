import requests
from bs4 import BeautifulSoup as bs
import socket

class SpiderMan:
    def __init__(self):
        self.requestHeaders = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
        self.postTitle = ""
        self.nextPageFlag = ""
        self.domainName = ""
        self.givenURL = ''
        self.pot = []
        self.url_pool = [] # for debug info

    def init(self, url):
        self.__init__()
        socket.setdefaulttimeout(10)
        self.givenURL = url

    def get_domain_name(self):
        domains = [".com", ".net", ".org", "edu", "cn"]
        for domain in domains:
            if domain in self.givenURL:
                self.domainName = self.givenURL[0: self.givenURL.find(domain) + len(domain)]
        if self.domainName[0:8] == "https://":
            self.domainName = self.domainName[8:]
        if self.domainName[0:7] == "http://":
            self.domainName = self.domainName[7:]

    def get_post_id(self, url):
        post_id = url
        if post_id[0:8] == "https://":
            post_id = post_id[8:]
        if post_id[0:7] == "http://":
            post_id = post_id[7:]
        if self.domainName in post_id:
            post_id = post_id.replace(self.domainName, '')
        return post_id

    def get_post_url(self, post_id):
        if post_id[0:6] == "https:" or post_id[0:5] == "http:":
            return post_id
        if post_id[0:4] == "bbs.":
            return "http://" + post_id
        while post_id[0] == '/':
            post_id = post_id[1:]
        return "http://" + self.domainName + "/" + post_id

    def download(self, post_id):
        url = self.get_post_url(post_id)
        r = requests.get(url, headers=self.requestHeaders)
        return r

    def lcs(self, s1, s2):
        m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
        nax = 0
        pos = 0
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    m[i + 1][j + 1] = m[i][j] + 1
                    if m[i + 1][j + 1] > nax:
                        nax = m[i + 1][j + 1]
                        pos = i + 1
        return nax  # 返回最长子串及其长度

    def get_first_page_url(self, soup):
        for tag in soup.find_all('a'):
            if tag and tag.text and tag.text.strip().strip('.').strip('<') in ['1', '第一页', '一页']:
                if tag.attrs.get('href') and 'javascript:' not in tag['href']:
                    post_id = self.get_post_id(self.givenURL)
                    tag_href_id = self.get_post_id(tag['href'])
                    lcs_len = self.lcs(post_id, tag_href_id)
                    if lcs_len / len(post_id) >= 0.5:
                        return tag['href']
        return self.givenURL

    def get_next_page_url(self, soup):
        if not self.nextPageFlag:
            for tag in soup.find_all('a'):
                if tag and tag.text and tag.text.strip().strip('>') in ['下一页', '下页', 'Next', 'next']:
                    if tag.attrs.get('href'):
                        self.nextPageFlag = tag.text
                        return tag['href']
        else:
            tag = soup.find('a', text=self.nextPageFlag)
            if tag and tag.attrs.get('href'):
                return tag['href']

        return None

    def get_post_title(self, soup):
        title_with_info = soup.title.text.strip()
        nax_len = len(title_with_info)
        cur_nax = -1
        self.postTitle = title_with_info
        for tag in soup.find_all(lambda t: True):
            if tag and tag.string:
                title = tag.string.strip()
                if len(title) < nax_len and title in title_with_info and cur_nax < len(title):
                    cur_nax = len(title)
                    self.postTitle = title

    def print_debug_info(self, idx):
        print("探测到 {} 页跟帖，正在生成 log 信息。。".format(len(self.pot)))
        with open('log.html', 'a+') as log:
            log.write('''<div style="font-size:130%;color:purple">{}. <a href='{}'>{}</a></div> \n'''.format(idx, self.givenURL, self.givenURL))
            log.write(''' <div style="font-size:110%;color:blue">贴名：{}</strong></div> \n'''.format(self.postTitle))
            post_idx = 1
            for url in self.url_pool:
                log.write(''' [{}]. <a href='{}'>{}</a><br> \n'''.format(post_idx, url, url))
                post_idx += 1
            log.write('<br><br>')
        print("Done.")

    def craw(self, url):
        try:
            self.init(url)
            self.get_domain_name()
            r = self.download(self.givenURL)
            soup = bs(r.content, 'html.parser')
            self.get_post_title(soup)
            url = self.get_first_page_url(soup)
            if url == self.givenURL and len(r.content) > 0:
                self.pot.append(soup)
                self.url_pool.append(self.get_post_url(url))
                url = self.get_next_page_url(soup)
            while url is not None:
                r = self.download(url)
                soup = bs(r.content, 'html.parser')
                if self.postTitle in soup.title.text.strip():
                    self.pot.append(soup)
                    self.url_pool.append(self.get_post_url(url))
                    url = self.get_next_page_url(soup)
                else:
                    break
        except BaseException as e:
            print("无法抓取{}，页面可能已被删除".format(self.givenURL))
            print(e)

