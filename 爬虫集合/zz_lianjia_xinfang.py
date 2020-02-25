import requests
import os
import threading
from bs4 import BeautifulSoup
from openpyxl import Workbook

excel_name = "zhengzhou_xinfang.xlsx"
wb = Workbook()
ws1 = wb.active
ws1.title = '郑州在售楼盘'

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
    text_list = soup.find_all('div', class_='resblock-desc-wrapper')
    for i in text_list:
        title = i.find('div', class_='resblock-name').find('a').get_text()
        title0 = 'https://zz.fang.lianjia.com' + i.find('div', class_='resblock-name').find('a')['href']
        title1 = i.find('span', class_='resblock-type').get_text()
        title2 = i.find('span', class_='sale-status').get_text()

        title3 = i.find('div', class_='resblock-location').find_all('span')[0].get_text()
        title4 = i.find('div', class_='resblock-location').find_all('span')[1].get_text()
        title5 = i.find('div', class_='resblock-location').find('a').get_text()
        title6 = i.find('a', class_='resblock-room').get_text().replace('\n', '').strip()
        title7 = i.find('div', class_='resblock-area').find('span').get_text().replace('建面 ', '').replace('㎡', '')
        title8 = i.find('div', class_='resblock-tag').get_text().replace('\n', '/').strip('/')
        title9 = i.find('div', class_='resblock-price').find('div', class_='main-price').get_text().replace('\n', '').replace('/平(均价)', '').replace('元', '').strip()
        title10 = i.find('div', class_='resblock-price').find('div', class_='second')
        if title10 is None:
            title10 = ''
        else:
            title10 = title10.get_text().replace('总价', '').replace('/套', '').replace('万', '').strip()

        index = (text_list.index(i) + 2) + (page_num * 10)
        ws1['A%s' % index] = title
        ws1['B%s' % index] = title1
        ws1['C%s' % index] = title2
        ws1['D%s' % index] = title3
        ws1['E%s' % index] = title4
        ws1['F%s' % index] = title5
        ws1['G%s' % index] = title6
        ws1['H%s' % index] = title7
        ws1['I%s' % index] = title10
        ws1['J%s' % index] = title9
        ws1['K%s' % index] = title8
        ws1['L%s' % index] = title0

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
    queue = [i for i in range(1, 60)]  # 构造 url 链接 页码。
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 1 and len(queue) > 0:  # 最大线程数设置为1
            cur_page = queue.pop(0)
            url = 'https://zz.fang.lianjia.com/loupan/nhs1pg{}/'.format(cur_page)
            print(url)
            thread = threading.Thread(target=execute, args=(url, cur_page))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()
