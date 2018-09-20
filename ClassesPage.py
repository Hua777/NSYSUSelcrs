# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

import Req
import CC

from ClassDetail import ClassDetail

from bs4 import BeautifulSoup as BS
import re as RE

class ClassesPage(object):
    def __init__(self):
        self.Reset()
        self.Pages = 0

    # 设定学年期
    def SetYear(self, year):
        self.SetConfig('D0', year)

    # 设定页数
    def SetPage(self, page):
        self.SetConfig('page', page)

    # 设定老师
    def SetTeacher(self, teacher):
        self.SetConfig('page', teacher)

    # 设定课号
    def SetNumber(self, number):
        self.SetConfig('T3', number)

    def FixToBS(self):
        # 学校网站代码有问题，此处为使其恢复正常点
        html = RE.sub(
            r"<style.*<\/style>", 
            '<body>',
            RE.sub(
                r"snall", 
                'small', 
                Req.Get('search', self.Config)
            )
        )
        return BS(html, 'html.parser')

    # 开始爬
    def Crawl(self, obj = False):
        bs = self.FixToBS()
        # 找寻其所有页数
        final_tr = bs.find_all('tr')[-1]
        pattern = RE.compile(r'第 ([0-9]+) \/ ([0-9]+) 頁')
        match = pattern.match(final_tr.get_text())
        self.Pages = int(match[2])
        # 开始把找到的列物件化
        result = []
        for tr in bs.find_all('tr')[3:-2]: # 去头去尾
            tmp = []
            idx = 0
            for td in tr.find_all('td'):
                # 学校代码问题，会超出 25
                if idx < 25:
                    tmp_text = td.get_text().strip().replace('&nbsp', '-')
                    if idx == 7:
                        # 课名只取中文
                        name = td.find('a').get_text().strip()
                        tmp.append(name)
                        tmp.append(CC.T2S(name)) # 简体字课名
                        tmp.append(td.find('a')['href']) # 课纲网址
                    elif idx == 3 or idx == 15:
                        # 简体字系所、老师
                        tmp.append(tmp_text)
                        tmp.append(CC.T2S(tmp_text))
                    else:
                        tmp.append(tmp_text)
                else:
                    break
                idx += 1
            if obj:
                result.append(ClassDetail(tmp))
            else:
                result.append(tmp)
        return result
    
    # 其他设定
    def SetConfig(self, key, value):
        self.Config[key] = value

    # 清除并重置设定
    def Reset(self):
        self.Config = {
            'a': 1, #
            'HIS': 1, # 
            'IDNO': '', #
            'ITEM': '', #
            'D0': Req.Year, # 課程學年期 1071
            'DEG_COD': '*', # 查詢依開課系所 * A B M N P
            'D1': '', # 查詢依開課系所
            'D2': '', # 年級
            'CLASS_COD': '', # 班级
            'SECT_COD': '', # 组别
            'TYP': 1, # 查詢項目 1（课程时间） 2（修课人数）
            'teacher': '', # 授课教师
            'crsname': '', # 课程名称
            'T3': '', # 课别代号
            'WKDAY': '', # 星期 1 2 3 4 5 6 7
            'SECT': '', # 节次 A 1 2 3 4 B 5 6 7 8 9 C D E F
            'page': 1, # 页数
            'bottom_per_page': 10, # 没屁用
            'data_per_page': 20 # 没屁用
        }
