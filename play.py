import SpiderMan
import time

begin = time.time()
url = 'http://bbs.csdn.net/forums/JavaScript'
sm = SpiderMan.SpiderMan()
sm.craw(url)
end = time.time()
print("\n耗时：{:.6} 秒".format(end-begin))