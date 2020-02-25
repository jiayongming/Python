import requests
import os
import threading
from bs4 import BeautifulSoup
from openpyxl import Workbook

excel_name = "zz_zhen2_xinfang.xlsx"
wb = Workbook()
ws1 = wb.active
ws1.title = '郑州在售楼盘(真二网)'

def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    return r.text


def get_text_list(html, page_num):
    '''
    获取每个页面的数据列表
    '''
    soup = BeautifulSoup(html, 'html.parser')
    text_list = soup.find_all('li', class_='search_item')
    for i in text_list:
        info = i.find('div', class_='search_info')
        search_url = 'https://www.zhen22.com' + info.find('div', class_='item_content').find('div', class_='item_left').find('div', class_='search_title').find('a')['href']
        search_status = info.find('div', class_='item_content').find('div', class_='item_left').find('div', class_='search_title').find('a').find('el-tag').get_text()
        search_name = info.find('div', class_='item_content').find('div', class_='item_left').find('div', class_='search_title').find('a').get_text().replace(search_status, '').replace('\n', '').strip()
        search_miaosu = info.find('div', class_='item_content').find('div', class_='item_left').find('div', class_='search_rooms').find('div', class_='area').get_text().replace('\n', '').strip()
        search_huxing = info.find('div', class_='item_content').find('div', class_='item_left').find('div', class_='search_rooms').find('div', class_='search_rooms_main').get_text().replace('\n', '').replace(' ', '').strip()
        dizhis = info.find('div', class_='item_content').find('div', class_='item_left').find('div', class_='search_address').find('div', class_='search_address_main').get_text().replace('\n', '').replace(' ', '').strip().split(']')

        search_quyu = dizhis[0].replace('[', '')
        search_dizhi = dizhis[1]

        print(search_url)

        ws1['A1'] = '小区名称'
        ws1['B1'] = '小区性质'
        ws1['C1'] = '小区状态'
        ws1['D1'] = '行政区域'
        ws1['E1'] = '区域板块'
        ws1['F1'] = '具体位置'
        ws1['G1'] = '在售户型'
        ws1['H1'] = '建筑面积'
        ws1['I1'] = '房屋总价(万元)'
        ws1['J1'] = '房屋单价(元/平均价)'
        ws1['K1'] = '房屋特色'
        ws1['L1'] = '详情链接'
        wb.save(filename=excel_name)

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url, page_num):
    page_html = download_page(url)
    get_text_list(page_html, page_num - 1)


def main():
    create_dir('lianjia')
    threads = []
    queue = [i for i in range(1, 2)]  # 构造 url 链接 页码。
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 1 and len(queue) > 0:  # 最大线程数设置为1
            cur_page = queue.pop(0)
            url = 'https://www.zhen22.com/zz/new-house/search?page={}'.format(cur_page)
            print(url)
            thread = threading.Thread(target=execute, args=(url, cur_page))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()
