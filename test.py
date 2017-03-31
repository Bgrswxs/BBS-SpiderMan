import requests
import re
from bs4 import BeautifulSoup as bs
import SpiderMan
import time

begin = time.time()
idx = 1
sm = SpiderMan.SpiderMan()
with open('log.html', 'w') as log:
    log.write('')

with open("urls.txt", "r") as f:
    url = f.readline().strip()
    while url and url != "DEBUG":
        print("[{}].正在抓取 {}....".format(idx, url))
        sm.craw(url)
        sm.print_debug_info(idx)
        idx += 1
        url = f.readline().strip()

end = time.time()
print(end-begin)






# txt = r.text
# # txt = re.sub(r'<!DOCTYPE.*?>', '', txt)
# # txt = re.sub(r'<!--.*?-->', '', txt)
# txt = re.sub(r'<script.*?>.*?</script>', '', txt, flags=re.DOTALL)
# txt = re.sub(r'<style.*?>.*?</style>', '', txt, flags=re.DOTALL)
# txt = re.sub(r'<.*?>', '', txt, flags=re.DOTALL)
# ans = txt.split('\n')
# print(len(ans))
# for e in ans:
#     if len(e.strip()) > 0:
#         print(e.strip())
