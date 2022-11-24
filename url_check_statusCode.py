import sys
import requests
import urllib3
import threading
import optparse
import queue
import time 

urllib3.disable_warnings()


class URLScaner(threading.Thread):
    def __init__(self, urlqueue,active_queue,fail_queue):
        threading.Thread.__init__(self)
        self._urlqueue = urlqueue
        self._active_queue = active_queue
        self._fail_queue = fail_queue
    
    def run(self):
        # print(self._portqueue.queue)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        while True:
            if self._urlqueue.empty():
            #判断队列为空，说明扫描完毕，跳出循环
                break
            #从url列表中取出端口，超时时间未1s
            url = self._urlqueue.get(timeout=0.5)

            # print("当前检测:%s" % url)
            now_time = time.strftime("%H:%M:%S", time.localtime())
            try:
                try:
                    r = requests.get(url,headers=headers,timeout=3,verify=False)
                    self._active_queue.put(url)
                    status_code = r.status_code
                    self.res_output(now_time,url,status_code)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    # [13:11]http:xxx.com[status code]200   200绿色
                    # sys.stdout.write("不存活: %s" % url)
                    self.res_output(now_time,url,'died')
                    self._fail_queue.put(url)
                    pass
            except Exception as e:
                print(e)

    def res_output(self,now_time,url,status_code):
        status_code_colour = 37
        if status_code == "died":
            status_code_colour = 31
        elif status_code >= 200 and status_code < 300:
            status_code_colour = 32  #绿色
        elif status_code >= 300 and status_code < 400:
            status_code_colour = 34    #黄色
        elif status_code >= 400 and status_code < 500:
            status_code_colour = 33 #蓝色
        elif status_code == 500:
            status_code_colour = 35  # 紫红色
        else:
            status_code_colour = 37 # 白色
        print("[\033[1;34;40m%s\033[0m] [\033[1;32;40m%s\033[0m] [\033[1;34;40mstatusCode\033[0m] [\033[1;%d;40m%s\033[0m]" %(now_time,url,status_code_colour,status_code))

def put_file_res(activeQueue,failQueue):
    with open('./active.txt','w') as f:
        while True:
            if activeQueue.empty():
                    break
            f.write(activeQueue.get() + '\r')

    with open('./fail.txt','w') as f:
        while True:
            if failQueue.empty():
                    break
            f.write(failQueue.get() + '\r') 
    print("结果输出完毕！！！")

def StartScan(urlsFilePath,threadNum):
    urlQueue = queue.Queue()
    threads = []
    activeQueue = queue.Queue()
    failQueue = queue.Queue()

    with open(urlsFilePath,"r",encoding='UTF-8') as urls:
        for url in urls.readlines():
            url = url.replace('\n','')
            if 'http' not in url:
                urlQueue.put('http://' + url)
                # urlQueue.put('https://' + url)
            else:
                urlQueue.put(url)
    # print(urlQueue.queue)
    for t in range(threadNum):
        threads.append(URLScaner(urlQueue,activeQueue,failQueue))

    #启动线程
    for thread in threads:
        thread.start()
    #阻塞线程
    for thread in threads:
        thread.join()

    put_file_res(activeQueue,failQueue)

if __name__ == '__main__':
    # parser = optparse.OptionParser('Example: python %prog -f urls.txt -t 5 \n')
    # #url文件
    # parser.add_option('-f','--file',dest='urlsFilePath',type='string',help='your urls file')
    # #线程数量
    # parser.add_option('-t','--thread',dest='threadNum',default=10,type='int',help='scanning thread number')

    # (options, args) = parser.parse_args()

    # StartScan(options.urlsFilePath,options.threadNum)
    StartScan("./urls.txt",2)
