import requests
import socket
from bs4 import BeautifulSoup as bs
socket.setdefaulttimeout(5)


url = "http://www.sina.com"
r = requests.get(url)
print(type(r.content))
a = bytes()
soup = bs(a, 'html.parser')
print(soup.title)
for e in soup.find_all('a'):
    print(e)