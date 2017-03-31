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
        print("[{}] {}".format(idx, url))
        print(" => 正在抓取...")
        sm.craw(url)
        sm.print_debug_info(idx)
        idx += 1
        url = f.readline().strip()

end = time.time()
print("\n耗时：{:.6} 秒".format(end-begin))

