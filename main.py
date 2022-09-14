# 导入数据请求模块
import requests
# 导入数据解析模块
import parsel
# 导入正则表达式模块
import re
# 导入pandas
import pandas as pd
# 导入进度条显示模块
from tqdm import tqdm

# 电子书目录地址
dir_url = f'xxxxxxx'  # 例如：https://www.xslc.net/girl/191497.html'
# 电子书具体内容的url前缀
text_url = 'xxxxxx'  # 例如：'https://www.xslc.net'


def gethtml(url):
    try:
        html = requests.get(url, timeout=5)
        if html.status_code == 200:
            html.encoding = html.apparent_encoding
            return html.text
        else:
            return 0
    except requests.exceptions.RequestException:
        return 0


while True:
    response = gethtml(dir_url)
    if response == 0:
        continue
    else:
        # print(response.text)  # 正则表达式提取出来数据返回列表 ['天道修改器']
        novel_name = re.findall('<h1>(.*?)</h1>', response)[0]
        # print(novel_name)
        novel_info = re.findall(
            '<dd><a href="(.*?)">(.*?)</a></dd>', response)
        # print(novel_info)
        for novel_url, novel_title in tqdm(novel_info):
            novel_url = text_url + novel_url
            print(novel_url, novel_title)
            # 1\. 发送请求, 对于刚刚分析得到的url地址发送请求
            while True:
                response = gethtml(novel_url)
                if response == 0:
                    continue
                else:
                    # <Response [200]> 返回response响应对象, 200表示请求成功
                    # 2\. 获取数据, 获取服务器返回的response响应数据
                    # response.text 获取响应体返回文本数据(网页源代码)
                    # print(response.text)
                    # 3\. 解析数据, 提取我们想要的数据内容 小说章节名字 以及小说内容
                    # 提取数据方式: xpath css re 这三种方式都是可以提取数据
                    # 把获取到的response.text 转换成 selector 对象
                    selector = parsel.Selector(response)
                    # novel_title = selector.css('.bookname h1::text').get()  # get获取第一个标签数据 返回字符串数据
                    # novel_title_1 = selector.xpath('//*[@class="bookname"]/h1/text()').get()  # get获取第一个标签数据 返回字符串数据
                    novel_content_list = selector.css(
                        '#content::text').getall()  # getall 获取所有标签内容, 返回列表数据
                    # 需要把列表转成字符串数据 join  \n换行符
                    novel_content = '\n'.join(novel_content_list)
                    # print(novel_title)
                    # print(novel_title_1)
                    # print(novel_content_list)
                    # print(novel_content)
                    # 4\. 保存数据
                    # w写入数据但是覆盖 a写入追加写入, 写入文件末尾 b 二进制模式
                    with open(novel_name + '.txt', mode='a', encoding='utf-8') as f:
                        f.write(novel_title)
                        f.write('\n')
                        f.write(novel_content)
                        f.write('\n')
                        # print('正在保存', novel_title)
                    break
        break
