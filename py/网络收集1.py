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
       'https://raw.githubusercontent.com/kimwang1978/collect-txt/refs/heads/main/bbxx365.txt' #,
      #' 'https://raw.githubusercontent.com/zengzifeng520/china-iptv-sources/refs/heads/main/output/live.txt'   
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


    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",

    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"熊猫影院": "熊猫电影",
    	"熊猫爱生活": "熊猫生活",
    	"爱宠宠物": "宠物生活",
    	"[ipv6]": "",
    	"专区": "",
    	"卫视超": "卫视",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",

    	"测试cctv": "CCTV",
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
    	"凤凰中文台": "凤凰中文",
    	"凤凰资讯台": "凤凰资讯",
    	"(CCTV4K测试）": "CCTV4K",
    	"上海东方卫视": "上海卫视",
    	"东方卫视": "上海卫视",
    	"内蒙卫视": "内蒙古卫视",
    	"福建东南卫视": "东南卫视",
    	"广东南方卫视": "南方卫视",
    	"湖南金鹰卡通": "金鹰卡通",
    	"炫动卡通": "哈哈炫动",
    	"卡酷卡通": "卡酷少儿",
    	"卡酷动画": "卡酷少儿",
    	"BRTVKAKU少儿": "卡酷少儿",
    	"优曼卡通": "优漫卡通",
    	"优曼卡通": "优漫卡通",
    	"嘉佳卡通": "佳嘉卡通",
    	"世界地理": "地理世界",
    	"CCTV世界地理": "地理世界",
    	"BTV北京卫视": "北京卫视",
    	"BTV冬奥纪实": "冬奥纪实",
    	"东奥纪实": "冬奥纪实",
    	"卫视台": "卫视",
    	"湖南电视台": "湖南卫视",
    	"少儿科教": "少儿",
    	"影视剧": "影视",
    	"电视剧": "影视",
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
import re
import os
# 定义一个包含所有要排除的关键词的列表
excluded_keywords = ['http://[', 'p3p://', 'rtmp://', 'http://php.j', '/kkk.jjjj.', 'stream1', '61.221.215.25:8800', 'epg.pw', '4gtv.cnlive.club', 'playtv-live.ifeng.com',                  
                     'video://https', '.xmcdn.com', 'radio', 'jnzq.ohoyee.com', 'free.', '221.7.175.154', 'audio', 'zmgd.zyrnet.com', 'satellitepull.cnr.cn/live/', 'gmxw.7766.org',
                     '122.152.202.33', 'psyl11.dyndns.tv', 'youtube.com', 'xhyx.gz.cn', 'aktv-stream', 'api.kkitv', 'aktv.top', 'live4play.uk', 'vpstv.net','raw.githubusercontent',
                     'tv.iill.top','iptv8k.top']

# 定义一个包含所有要提取的关键词的列表
extract_keywords = ['珠江', '东莞', '广州', '佛山', '广东新闻', 
                    '翡翠台','有线新闻','无线新闻','TVB翡翠','TVB明珠','NOW新闻','Now','无线华丽','TVB星河','TVB-Plus',
                     'TVBPLUS','TVB黄金翡翠','TVB千禧','TVB娱乐','TVB J2','RTHK','VIU','凤凰卫视','凤凰香港','凤凰中文',
                     '凤凰资讯','香港卫视','天映','美亚','新加坡','澳门','澳亚','千禧经典','华丽台',
                     'TVBS','寰宇','台视','东森','公视','华视','中视新闻','中天新闻','中天娱乐','中天综合',
                     '中天亚洲','民视','龙华','八大','非凡','三立','纬来育乐','靖天','大立','東森',
                     'Thrill','龙祥']


# 读取文件并处理每一行
with open('2.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

    # 创建或打开一个输出文件用于写入处理后的数据
    with open('网络收集.txt', 'w', encoding='utf-8') as outfile:
        for line in lines:
            # 首先检查行是否包含任何提取关键词
            if any(keyword in line for keyword in extract_keywords):
                # 如果包含提取关键词，进一步检查行是否不包含任何排除关键词
                if not any(keyword in line for keyword in excluded_keywords):
                    outfile.write(line)  # 写入符合条件的行到文件


###############################################################
import re
def parse_file(input_file_path, output_file_name):
    # 正则表达式匹配从'//'开始到第一个'/'或第一个'::'结束的部分
    ip_or_domain_pattern = re.compile(r'//([^/:]*:[^/:]*::[^/:]*|[^/]*)')
    # 用于存储每个IP或域名及其对应的行列表
    ip_or_domain_to_lines = {}
    # 读取原始文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # 如果行是分类标签行，则跳过
            if ",#genre#" in line:
                continue
            # 检查行是否包含IP或域名
            match = ip_or_domain_pattern.search(line)
            if match:
                # 提取匹配到的IP或域名
                matched_text = match.group(1)
                # 去除IP或域名后的剩余部分，只保留匹配到的IP或域名
                ip_or_domain = matched_text.split('://')[-1].split('/')[0].split('::')[0]
                # 将行添加到对应的IP或域名列表中
                if ip_or_domain not in ip_or_domain_to_lines:
                    ip_or_domain_to_lines[ip_or_domain] = []
                ip_or_domain_to_lines[ip_or_domain].append(line)
    ############################################################################### 过滤掉小于1500字节的IP或域名段
    filtered_ip_or_domain_to_lines = {ip_or_domain: lines for ip_or_domain, lines in ip_or_domain_to_lines.items()
                                      if sum(len(line) for line in lines) >= 300}
    # 如果没有满足条件的IP或域名段，则不生成文件
    if not filtered_ip_or_domain_to_lines:
        print("没有满足条件的IP或域名段，不生成文件。")
        return
    # 合并所有满足条件的IP或域名的行到一个文件
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        for ip_or_domain, lines in filtered_ip_or_domain_to_lines.items():
            # 写入IP或域名及其对应的行到输出文件
            output_file.write(f"频道,#genre#\n")
            for line in lines:
                output_file.write(line + '\n')
            output_file.write('\n')  # 在每个小段后添加一个空行作为分隔
# 调用函数并传入文件路径和输出文件名
parse_file('网络收集.txt', '网络收集.txt')



import cv2
import time
from tqdm import tqdm
import os

# 存储文件路径
file_path = "网络收集.txt"
output_file_path = "网络收集.txt"

def get_ip_key(url):
    """从 URL 中提取 IP 地址，并构造一个唯一的键"""
    start = url.find('://') + 3
    end = url.find('/', start)
    return url[start:end] if end!= -1 else None

def merge_and_filter():
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_lines = len(lines)

    # 处理输入文件中的数据并进行检测
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        for i, line in tqdm(enumerate(lines), total=total_lines, desc="Processing", unit='line'):
            if 'genre' in line:
                output_file.write(line)
                continue
            parts = line.split(',', 1)
            if len(parts) == 2:
                channel_name, url = parts
                channel_name = channel_name.strip()
                url = url.strip()
                ip_key = get_ip_key(url)
                if ip_key and ip_key in detected_ips:
                    if detected_ips[ip_key]['status'] == 'ok':
                        output_file.write(line)
                elif ip_key:
                    cap = cv2.VideoCapture(url)
                    start_time = time.time()
                    frame_count = 0
                    while frame_count < 30 and (time.time() - start_time) < 3:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        frame_count += 1
                    cap.release()
                    if frame_count >= 30:
                        detected_ips[ip_key] = {'status': 'ok'}
                        output_file.write(line)
                    else:
                        detected_ips[ip_key] = {'status': 'fail'}

    # 合并任意字符加上网络收集.txt 的文件
    all_files = [f for f in os.listdir(os.getcwd()) if f.endswith('网络收集.txt')]
    with open(output_file_path, 'a', encoding='utf-8') as main_output:
        for file_name in all_files:
            if file_name!= output_file_path:
                with open(file_name, 'r', encoding='utf-8') as other_file:
                    content = other_file.read()
                    if content:
                        main_output.write('\n')
                        main_output.write(content)

detected_ips = {}
merge_and_filter()

for ip_key, result in detected_ips.items():
    print(f"IP Key: {ip_key}, Status: {result['status']}")



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
            urls = re.findall(r'[https]?[http]?[P2p]?[mitv]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行,无论是否已被记录,都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))
# 使用方法
remove_duplicates('网络收集.txt', '网络收集.txt')





######################连通性检测


import requests
import time
import cv2
from urllib.parse import urlparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置常量

HTTP_TIMEOUT = 3       # HTTP 连接超时时间 (秒)
RTSP_TIMEOUT = 5       # RTSP 检测超时时间 (秒)
MAX_WORKERS = 20       # 线程池大小，根据网络状况调整

def test_http_connectivity(url, timeout=HTTP_TIMEOUT):
    """
    测试 HTTP/HTTPS 直播源连通性
    """
    try:
        # stream=True 避免下载整个文件，只获取头部和少量数据
        with requests.get(url, stream=True, timeout=timeout) as response:
            if response.status_code == 200:
                # 尝试读取一小块数据以确认流确实存在
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        return True
                    break  # 只要读到一点数据就认为连通
            else:
                return False
    except requests.RequestException:
        return False
    except Exception:
        return False

def test_rtsp_connectivity(url, timeout=RTSP_TIMEOUT):
    """
    测试 RTSP 直播源连通性
    """
    cap = None
    try:
        cap = cv2.VideoCapture(url)
        # 设置超时属性 (部分后端支持)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, timeout * 1000)
        
        if not cap.isOpened():
            return False
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret, frame = cap.read()
            if ret and frame is not None:
                return True
            # 短暂休眠，避免 CPU 空转
            time.sleep(0.1)
            
        return False
    except Exception:
        return False
    finally:
        # 确保摄像头对象被释放
        if cap is not None:
            cap.release()

def test_connectivity_and_download(url):
    """
    根据协议类型选择检测方法
    """
    if not url:
        return False
    
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme.lower()
    
    if scheme in ['http', 'https']:
        return test_http_connectivity(url)
    elif scheme == 'rtsp':
        return test_rtsp_connectivity(url)
    else:
        # 不支持的协议，视为无效
        return False

def process_line(line):
    """
    处理单行数据，返回 (name, url, is_valid) 或 None
    """
    line = line.strip()
    if not line:
        return None
    
    # 简单解析 CSV 格式: Name,URL
    # 注意：如果名称中包含逗号，这种简单 split 会出错。
    # 假设格式严格为 "名称,URL" 且 URL 中不含逗号
    parts = line.split(",", 1)  # 最多分割一次，防止 URL 中有逗号
    
    if len(parts) != 2:
        return None
        
    channel_name, channel_url = parts
    channel_name = channel_name.strip()
    channel_url = channel_url.strip()
    
    if not channel_url:
        return None
        
    # 跳过元数据行 (如 #EXTINF)，除非你想保留它们
    if channel_name.startswith('#'):
        return None

    try:
        is_valid = test_connectivity_and_download(channel_url)
    except Exception:
        is_valid = False
        
    return (channel_name, channel_url, is_valid)

def main(input_file, output_file):
    print(f"开始读取文件: {input_file}")
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 不存在")
        return

    valid_results = []
    invalid_count = 0
    total_lines = len(lines)
    
    print(f"共发现 {total_lines} 行，开始多线程检测...")
    
    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        future_to_line = {executor.submit(process_line, line): line for line in lines if line.strip()}
        
        # 使用 tqdm 显示进度
        for future in tqdm(as_completed(future_to_line), total=len(future_to_line), desc="检测进度"):
            try:
                result = future.result()
                if result:
                    name, url, is_valid = result
                    if is_valid:
                        valid_results.append((name, url))
                    else:
                        invalid_count += 1
            except Exception as e:
                # 理论上 process_line 内部已捕获异常，此处为保险
                invalid_count += 1

    # 写入有效结果
    with open(output_file, "w", encoding="utf-8") as f:
        for name, url in valid_results:
            f.write(f"{name},{url}\n")

    print("-" * 50)
    print(f"检测完成!")
    print(f"有效源数量: {len(valid_results)}")
    print(f"无效源数量: {invalid_count}")
    print(f"结果已保存至: {output_file}")

if __name__ == "__main__":
    # 请修改这里的文件名
    INPUT_FILE = "网络收集1.txt"
    OUTPUT_FILE = "网络收集1.txt"  # 不要与输入文件同名，防止数据丢失
    
    main(INPUT_FILE, OUTPUT_FILE)



############################################################################################################################################

import re
from pypinyin import lazy_pinyin
# 打开一个utf-8编码的文本文件
with open("网络收集.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')
# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))
# 将排序后的行写入新的utf-8编码的文本文件
with open("网络收集.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)




def parse_file(input_file_path, output_file_name):    #
    # 正则表达式匹配从'//'开始到第一个'/'或第一个'::'结束的部分
    ip_or_domain_pattern = re.compile(r'//([^/:]*:[^/:]*::[^/:]*|[^/]*)')
    # 用于存储每个IP或域名及其对应的行列表
    ip_or_domain_to_lines = {}
    # 用于生成分类名的字母和数字计数器
    alphabet_counter = 0  # 字母计数器，从0开始
    number_counter = 1     # 数字计数器，从1开始
    # 读取原始文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # 如果行是分类标签行，则跳过
            if ",#genre#" in line:
                continue
            # 检查行是否包含IP或域名
            match = ip_or_domain_pattern.search(line)
            if match:
                # 提取匹配到的IP或域名
                matched_text = match.group(1)
                # 去除IP或域名后的剩余部分，只保留匹配到的IP或域名
                ip_or_domain = matched_text.split('://')[-1].split('/')[0].split('::')[0]
                # 将行添加到对应的IP或域名列表中
                if ip_or_domain not in ip_or_domain_to_lines:
                    ip_or_domain_to_lines[ip_or_domain] = []
                ip_or_domain_to_lines[ip_or_domain].append(line)
    # 过滤掉小于1000字节的IP或域名段
    filtered_ip_or_domain_to_lines = {ip_or_domain: lines for ip_or_domain, lines in ip_or_domain_to_lines.items()
                                      if sum(len(line) for line in lines) >= 250}   # 过滤掉小于1000字节的IP或域名段
    # 如果没有满足条件的IP或域名段，则不生成文件
    if not filtered_ip_or_domain_to_lines:
        print("没有满足条件的IP或域名段，不生成文件。")
        return
    # 合并所有满足条件的IP或域名的行到一个文件
############################################################
    with open(output_file_name, 'w', encoding='utf-8') as output_file:   #output_
        for ip_or_domain, lines in filtered_ip_or_domain_to_lines.items():
            # 检查是否需要递增数字计数器
            if alphabet_counter >= 26:
                number_counter += 1
                alphabet_counter = 0  # 重置字母计数器          
 ######################################################              
            # 生成分类名
            genre_name = chr(65 + alphabet_counter)# + str(number_counter)
            output_file.write(f"港澳{genre_name}组,#genre#\n")
            for line in lines:
                output_file.write(line + '\n')
            output_file.write('\n')  # 在每个小段后添加一个空行作为分隔
            alphabet_counter += 1  # 递增字母计数器
# 调用函数并传入文件路径和输出文件名
parse_file('网络收集.txt', '网络收集.txt')





import datetime
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
current_time = now.strftime("%Y/%m/%d %H:%M")
# 打开文本文件并将时间添加到开头
file_path = "网络收集.txt"
with open(file_path, 'r+', encoding='utf-8') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(f'{current_time}更新,#genre#\n{content}')
   ##### f.write(f'虚情的爱,https://vd2.bdstatic.com/mda-mi1dd05gmhwejdwn/sc/cae_h264/1630576203346678103/mda-mi1dd05gmhwejdwn.mp4\n{content}')
       

################################################################################################任务结束，删除不必要的过程文件
files_to_remove = ["2.txt", "汇总.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")
print("任务运行完毕，频道列表可查看文件夹内源.txt文件！")
