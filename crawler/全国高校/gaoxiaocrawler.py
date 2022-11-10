# ! /usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__:leezp
# __date__:2019-08-11

url = 'https://gaokao.chsi.com.cn/sch'
json_data = {
    '北京': 11, '天津': 12, '河北': 13, '山西': 14, '内蒙古': 15,
    '辽宁': 21, '吉林': 22, '黑龙江': 23,
    '上海': 31, '江苏': 32, '浙江': 33, '安徽': 34, '福建': 35, '江西': 36, '山东': 37,
    '河南': 41, '湖北': 42, '湖南': 43, '广东': 44, '广西': 45, '海南': 46,
    '重庆': 50, '四川': 51, '贵州': 52, '云南': 53, '西藏': 54,
    '陕西': 61, '甘肃': 62, '青海': 63, '宁夏': 64, '新疆': 65,
    '香港': 81,
    '澳门': 91,
    '台湾': 71
}

'''
页码  &start= 0
0,20,40,60

n=(page-1)*20
'''

import requests
from bs4 import BeautifulSoup

'''
[<td class="js-yxk-yxmc"><a href="/sch/schoolInfo--schId-1980497017.dhtml" target="_blank">海军军医大学</a> </td>, 
                            <td class="js-yxk-yxmc">上海公安学院</td>]
'''


# n=(page-1)*20
def getonepage(num, page, count):
    response = requests.get(
        'https://gaokao.chsi.com.cn/sch/search.do?searchType=1&ssdm=' + str(num) + '&start=' + str((page - 1) * 20))
    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
    all_t = soup.find_all("td", class_="js-yxk-yxmc")
    if len(all_t) != 0:
        for k in all_t:
            num = k.find_all('a')
            if len(num) > 0:  # 如果有a标签
                with open("gaoxiao.txt", "a", encoding='utf-8') as f:
                    f.write(num[0].text.strip() + ',https://gaokao.chsi.com.cn' + num[0]['href'] + '\n')
                count += 1
            elif len(num) == 0:
                pass  # 没有a标签(url)的不知名高校暂时不作处理
        return count
    return 0


def getoneprovince(num, province):
    print(province + '高校')
    i = 1
    sum = 0
    count = 0
    while (1):
        count = getonepage(num, i, count)
        i += 1
        if (count != 0):
            sum = count
        if (count == 0):
            break
    '''
    with open("gaoxiao.txt", "a", encoding='utf-8') as f:
        f.write(province + '高校数量:' + str(sum)+'\n')
    '''


def main():
    items = ["北京", "天津", "河北", "山西", "内蒙古",
             "辽宁", "吉林", "黑龙江",
             "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东",
             "河南", "湖北", "湖南", "广东", "广西", "海南",
             "重庆", "四川", "贵州", "云南", "西藏",
             "陕西", "甘肃", "青海", "宁夏", "新疆",
             "香港",
             "澳门",
             "台湾"]
    for province in items:
        num = json_data[province]
        getoneprovince(num, province)


main()

