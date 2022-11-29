import optparse
import os
import re

def output(ip_dict):
    with open("./res/fscan_res.md", "w", encoding="utf8") as f:
        for k,v in ip_dict.items():
            f.write("## %s \r" % k)
            for i in v:
                f.write(i + "\r")

def get_all_ip(datalist):
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ip_dict = {}
    for line in datalist:
        res = re.findall(pattern, line)
        if res and (res[0] not in ip_dict):
            ip_dict[res[0]] = []
            continue
        if res and (res[0] in ip_dict):
            ip_dict[res[0]].append(line)
    output(ip_dict)

    # print(ip_dict)

def Start(filepath):
    if not os.path.exists(filepath):
        print("文件不存在")
        exit()
    datalist = []
    with open(filepath, "r", encoding="utf8") as f:
        for i in f.readlines():
            datalist.append(i.strip())
    # 获取所有ip 去重整理成字典？
    get_all_ip(datalist)


if __name__ == '__main__':
    parser = optparse.OptionParser('Example: python %prog -f urls.txt -t 5 \n')
    #url文件
    parser.add_option('-f','--file',dest='FilePath',type='string',help='your urls file')

    (options, args) = parser.parse_args()

    Start(options.FilePath)
    # l = ['asdsad192.134.33.11asdsa','asdsads33.33.22.33','asdasdasasdasdaa12321']
    # get_all_ip(l)
