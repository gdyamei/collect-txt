from lxml import etree
import time
import datetime
from datetime import datetime, timedelta  # 确保 timedelta 被导入
import concurrent.futures
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import requests
import re
import os
import threading
from queue import Queue
import queue
from datetime import datetime
import fileinput
from tqdm import tqdm
from pypinyin import lazy_pinyin
from opencc import OpenCC
import base64
import cv2
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from translate import Translator  # 导入Translator类,用于文本翻译
## 定义txt文件的URL列表
urls = [
       'https://raw.githubusercontent.com/kimwang1978/collect-txt/refs/heads/main/bbxx365.txt',
       'https://raw.githubusercontent.com/zengzifeng520/china-iptv-sources/refs/heads/main/output/live.txt'   
]

# 合并文件的函数
def merge_txt_files(urls, output_filename='汇总.txt'):
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for url in urls:
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # 确保请求成功
                    # 尝试将响应内容解码为UTF-8，如果失败则尝试其他编码
                    try:
                        content = response.content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = response.content.decode('gbk')  # 尝试GBK编码
                    outfile.write(content + '\n')
                except requests.RequestException as e:
                    print(f'Error downloading {url}: {e}')
    except IOError as e:
        print(f'Error writing to file: {e}')

# 调用函数
merge_txt_files(urls)







#简体转繁体
# 创建一个OpenCC对象,指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('汇总.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()
# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)
# 将转换后的简体字写入txt文件
with open('汇总.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)



with open('汇总.txt', 'r', encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
#定义替换规则的字典对频道名替换
replacements = {
    	"中视购物":"购物"
       "CCTV中视购物":"购物"
        "凤凰古城东关门":"东关门"
        "凤凰古城南华山":"南华山"
        "纬来体育":"体育"
       "CCTV-": "CCTV",
    	"CCTV_": "CCTV",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"CCTV4国际": "CCTV4",
    	"CCTV4中文国际": "CCTV4",
    	"CCTV4欧洲": "CCTV4",
    	"CCTV5体育": "CCTV5",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV6电影": "CCTV6",
    	"CCTV7军事": "CCTV7",
    	"CCTV7军农": "CCTV7",
    	"CCTV7农业": "CCTV7",
    	"CCTV7国防军事": "CCTV7",
    	"CCTV8电视剧": "CCTV8",
    	"CCTV8影视": "CCTV8",
    	"CCTV8纪录": "CCTV9",
    	"CCTV9记录": "CCTV9",
    	"CCTV9纪录": "CCTV9",
    	"CCTV10科教": "CCTV10",
    	"CCTV11戏曲": "CCTV11",
    	"CCTV12社会与法": "CCTV12",
    	"CCTV13新闻": "CCTV13",
    	"CCTV新闻": "CCTV13",
    	"CCTV14少儿": "CCTV14",
    	"央视14少儿": "CCTV14",
    	"CCTV少儿超": "CCTV14",
    	"CCTV15音乐": "CCTV15",
    	"CCTV音乐": "CCTV15",
    	"CCTV16奥林匹克": "CCTV16",
    	"CCTV17农业农村": "CCTV17",
    	"CCTV17军农": "CCTV17",
    	"CCTV17农业": "CCTV17",
    	"CCTV5+体育赛视": "CCTV5+",
    	"CCTV5+赛视": "CCTV5+",
    	"CCTV5+体育赛事": "CCTV5+",
    	"CCTV5+赛事": "CCTV5+",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV5赛事": "CCTV5+",
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10"
}
with open('汇总.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        # 去除行尾的换行符
        line = line.rstrip('\n')
        # 分割行，获取逗号前的字符串
        parts = line.split(',', 1)
        if len(parts) > 0:
            # 替换逗号前的字符串
            before_comma = parts[0]
            for old, new in replacements.items():
                before_comma = before_comma.replace(old, new)
            # 将替换后的逗号前部分和逗号后部分重新组合成一行，并写入新文件
            new_line = f'{before_comma},{parts[1]}\n' if len(parts) > 1 else f'{before_comma}\n'
            new_file.write(new_line)






# 打开文本文件进行读取
def read_and_process_file(input_filename, output_filename, encodings=['utf-8', 'gbk']):
    for encoding in encodings:
        try:
            with open(input_filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"Cannot decode file '{input_filename}' with any of the provided encodings")

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if '$' in line:
                processed_line = line.split('$')[0].rstrip('\n')
                outfile.write(processed_line + '\n')
            else:
                outfile.write(line)

# 调用函数
read_and_process_file('汇总.txt', '汇总.txt')  # 修改输出文件名以避免覆盖原始文件

###################################################################去重#####################################
def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'[https]?[http]?[rtsp]?[rtmp]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))
# 使用方法
remove_duplicates('汇总.txt', '2.txt')   






######################################################################################提取goodiptv
import os

# 1. 定义要排除的垃圾/无效链接关键词（统一转小写）
excluded_keywords = [
    'http://[', 'p3p://', 'rtmp://', 'http://php.j', '/kkk.jjjj.', 'stream1', 
    '61.221.215.25:8800', 'epg.pw', '4gtv.cnlive.club', '://ifeng.com',                  
    'video://https', '.xmcdn.com', 'radio', '://ohoyee.com', 'free.', '221.7.175.154', 
    'audio', '://zyrnet.com', 'satellitepull.cnr.cn/live/', 'gmxw.7766.org',
    '122.152.202.33', 'psyl11.dyndns.tv', 'youtube.com', 'xhyx.gz.cn', 'aktv-stream', 
    'api.kkitv', 'aktv.top', 'live4play.uk', 'vpstv.net', 'raw.githubusercontent',
    'tv.iill.top', 'iptv8k.top', 'douyincdn.com','myalicdn.com','yy/1354931498','体育'
]
excluded_keywords = [k.lower() for k in excluded_keywords]

# 2. 按分类定义提取关键词（用于自动分组）
categories = {
    "广东本地": ['珠江', '广东新闻', '广东民生', '广州影视', '广州新闻', '广州综合', '佛山公共', '佛山影视', '佛山综合', '东莞', '深圳财经生活', '南国都市'],
    "港澳频道": ['翡翠台', '有线新闻', '无线新闻', 'tvb', 'now', 'rthk', 'viu', '凤凰', '香港卫视', '天映', '美亚', '澳门', '澳亚', '千禧经典', '华丽台', 
                  '无线华丽','明珠台','thrill', '龙祥'],
    "台湾频道": ['tvbs', '寰宇', '台视', '东森', '東森', '公视', '华视', '中视', '中天', '民视', '龙华', '八大', '非凡', '三立', '纬来', '靖天', '大立'],
    "其他新加坡": ['新加坡','Fox新闻']
}

# 展开一个扁平化的关键词列表，方便快速匹配
all_extract_keywords = [k.lower() for sublist in categories.values() for k in sublist]

def filter_and_sort_text_playlist(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ 错误：找不到输入文件 {input_file}")
        return

    # 初始化每个分类的容器（用 dict 兼顾去重：{链接: 完整行文本}）
    classified_data = {cat: {} for cat in categories}
    classified_data["未分类其他"] = {} # 兜底分类
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line_strip = line.strip()
            if not line_strip or ',' not in line_strip: # 过滤空行或不含逗号的无效行
                continue
            
            line_lower = line_strip.lower()
            
            # 1. 排除垃圾链接
            if any(k in line_lower for k in excluded_keywords):
                continue
                
            # 2. 检查是否命中提取关键词
            if any(k in line_lower for k in all_extract_keywords):
                # 提取链接部分（通常在逗号后面）作为去重 Key
                parts = line_strip.split(',', 1)
                channel_name = parts[0].lower()
                link = parts[1]
                
                # 3. 判断属于哪个分类
                matched_cat = "未分类其他"
                for cat, keywords in categories.items():
                    if any(k.lower() in channel_name for k in keywords):
                        matched_cat = cat
                        break
                
                # 放入对应分类（自动去重相同链接）
                classified_data[matched_cat][link] = line_strip

    # 4. 写入新文件
    total_count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for cat, items in classified_data.items():
            if items: # 如果该分类下有数据
                outfile.write(f"\n{cat} ,#genre#\n") # 写入播放器识别的分组标签
                # 按频道名字排序后写入
                sorted_lines = sorted(items.values())
                for sorted_line in sorted_lines:
                    outfile.write(sorted_line + '\n')
                    total_count += 1

    print(f"💾 处理完成！已成功筛选并分类归纳 {total_count} 个频道至 {output_file}")

# 执行过滤
filter_and_sort_text_playlist('2.txt', '网络收集.txt')










