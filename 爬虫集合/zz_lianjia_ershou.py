import requests
import os
import threading
from bs4 import BeautifulSoup
from openpyxl import Workbook

excel_name = "zhengzhou.xlsx"
wb = Workbook()


fenqu = {'二七区': 'erqi'}
fenqu['郑东新区'] = 'zhengdongxinqu'
fenqu['荥阳市'] = 'xingyangshi'
fenqu['新郑市'] = 'xinzhengshi'
fenqu['上街区'] = 'shangjiequ'
fenqu['巩义市'] = 'gongyishi'
fenqu['新密市'] = 'xinmishi'
fenqu['登封市'] = 'dengfengshi'
fenqu['中牟县'] = 'zhongmuxian'
fenqu['经开区'] = 'jingkaiqu'
fenqu['高新区'] = 'gaoxin9'
fenqu['航空港区'] = 'hangkonggangqu'
fenqu['中原区'] = 'zhongyuan'
fenqu['管城回族区'] = 'guanchenghuizuqu'
fenqu['惠济区'] = 'huiji'
fenqu['金水区'] = 'jinshui'

def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    return r.text


def get_text_list(html, fenquming, page_num):
    '''
    获取每个页面的数据列表
    '''
    soup = BeautifulSoup(html, 'html.parser')
    text_list = soup.find_all('div', class_='info clear')
    ws1 = wb.active
    for i in text_list:
        title = i.find('div', class_='title').find('a').get_text()
        titleHtml = i.find('div', class_='title').find('a')['href']
        flood1 = i.find('div', class_='flood').find('div', class_='positionInfo').find_all('a')[0].get_text().strip()
        flood2 = i.find('div', class_='flood').find('div', class_='positionInfo').find_all('a')[1].get_text().strip()
        address = i.find('div', class_='address').find('div', class_='houseInfo').get_text()
        follow_info = i.find('div', class_='followInfo').get_text()
        follow_info0 = follow_info.split('/')[0].replace('人关注', '').strip()
        follow_info1 = follow_info.split('/')[1].replace('发布', '').strip()

        tag = i.find('div', class_='tag').get_text()
        price_info = i.find('div', class_='priceInfo')
        total_price = price_info.find('div', class_='totalPrice').get_text()
        unit_price = price_info.find('div', class_='unitPrice').get_text().replace('单价', '').replace('/平米', '')

        index = (text_list.index(i) + 2) + (page_num * 30)
        location1 = 'A%s' % index
        ws1[location1] = title

        location2 = 'B%s' % index
        ws1[location2] = flood1

        location3 = 'C%s' % index
        ws1[location3] = flood2

        location4 = 'D%s' % index
        ws1[location4] = address

        location5 = 'E%s' % index
        ws1[location5] = follow_info0

        location6 = 'F%s' % index
        ws1[location6] = follow_info1

        location6 = 'G%s' % index
        ws1[location6] = tag

        location7 = 'H%s' % index
        ws1[location7] = total_price

        location8 = 'I%s' % index
        ws1[location8] = unit_price

        location9 = 'J%s' % index
        ws1[location9] = titleHtml

        ws1['A1'] = '户型描述'
        ws1['B1'] = '小区名称'
        ws1['C1'] = '区域'
        ws1['D1'] = '户型详情'
        ws1['E1'] = '关注人数'
        ws1['F1'] = '发布时间'
        ws1['G1'] = '户型特色'
        ws1['H1'] = '总价'
        ws1['I1'] = '单价'
        ws1['J1'] = '详情链接'
        ws1.title = fenquming
        wb.save(filename=excel_name)
        print('①{}==②{}==③{}==④{}==⑤{}==⑥{}==⑦{}==⑧{}'.format(title, flood1, flood2, address, follow_info, tag, total_price, unit_price))


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url, fenquming, page_num):
    page_html = download_page(url)
    get_text_list(page_html, fenquming, page_num - 1)


def main():
    create_dir('lianjia')
    threads = []
    for key in fenqu:
        queue = [i for i in range(1, 2)]  # 构造 url 链接 页码。
        while len(queue) > 0:
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < 1 and len(queue) > 0:  # 最大线程数设置为1
                cur_page = queue.pop(0)
                url = 'https://zz.lianjia.com/ershoufang/{}/pg{}/'.format(f'{fenqu[key]}', cur_page)
                print(url)
                thread = threading.Thread(target=execute, args=(url, f'{key}', cur_page))
                thread.setDaemon(True)
                thread.start()
                print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
                threads.append(thread)


if __name__ == '__main__':
    main()
