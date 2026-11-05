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
    	"中视购物":"购物",
       "CCTV中视购物":"购物",
        "凤凰古城东关门":"东关门",
        "凤凰古城南华山":"南华山",
        "纬来体育":"体育",
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
    'tv.iill.top', 'iptv8k.top', 'douyincdn.com','myalicdn.com','yy/1354931498','体育','zhibo.hkstv.tv'
]
excluded_keywords = [k.lower() for k in excluded_keywords]

# 2. 按分类定义提取关键词（用于自动分组）
categories = {
    "广东本地": ['珠江', '广东新闻', '广东民生', '广州影视', '广州新闻', '广州综合', '佛山公共', '佛山影视', '佛山综合', '东莞', '深圳财经生活', '南国都市'],
    "港澳频道": ['翡翠台', '有线新闻', '无线新闻', 'tvb', 'now', 'rthk', 'viu', '凤凰', '香港卫视', '天映', '美亚', '澳门', '澳亚', '千禧经典', '华丽台', 
                  '无线华丽','明珠台','thrill', '龙祥','翡翠剧集台'],
    "台湾频道": ['tvbs', '寰宇', '台视', '东森', '東森', '公视', '华视', '中视', '中天', '民视', '龙华', '八大', '非凡', '三立', '纬来', '靖天', '大立'],
    "新加坡": ['新加坡','Fox新闻']
}

# 展开一个扁平化的关键词列表，方便快速匹配
all_extract_keywords = [k.lower() for sublist in categories.values() for k in sublist]

def filter_and_sort_text_playlist(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ 错误：找不到输入文件 {input_file}")
        return

    # 【修改点 1】初始化每个分类的容器，不再添加 "未分类其他" 兜底分类
    classified_data = {cat: {} for cat in categories}
    
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
                matched_cat = None  # 【修改点 2】默认设为 None
                for cat, keywords in categories.items():
                    if any(k.lower() in channel_name for k in keywords):
                        matched_cat = cat
                        break
                
                # 【修改点 3】如果命中了已有的四大分类则放入对应容器，未命中的直接丢弃
                if matched_cat:
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
    INPUT_FILE = "网络收集.txt"
    OUTPUT_FILE = "网络收集.txt"  # 不要与输入文件同名，防止数据丢失
    
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
                                 ####   if sum(len(line) for line in lines) >= 250}   # 过滤掉小于1000字节的IP或域名段
                                      if sum(len(line) for line in lines) >= 2}   # 过滤掉小于1000字节的IP或域名段
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
