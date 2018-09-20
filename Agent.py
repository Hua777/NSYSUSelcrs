# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

import Req
from ClassSelect import ClassSelect

import time as T
from urllib import parse as PARSE
import re as RE

class Agent(object):
    def __init__(self):
        self.Session = Req.Session()
        self.Logined = False

    # 获取验证码 filename, filepath
    def GetValidCode(self) -> [str, str]:
        req = self.Session.get(Req.Urls['valid'], stream = True, headers = Req.Headers, timeout = 10)
        filename = str(T.time()) + '.jpg'
        filepath = 'static/img/validcode/' + filename
        open(filepath, 'wb').write(req.raw.read())
        return filename, filepath

    # 登入 login, msg
    def Login(self, username, password, validcode) -> [bool, str]:
        html = Req.SessPostBS(self.Session, 'check', {
            'stuid': username,
            'SPassword': password,
            'ValidCode': validcode
        }, headers = None)
        if html.get_text().find('此網頁使用框架,但是您的瀏覽器並不支援.作業失敗') >= 0:
            self.Logined = True
            self.InitUser()
            return True, ''
        self.Logined = False
        return False, html.get_text().strip()

    # 初始化用户参数
    def InitUser(self):
        self.SelectStage = 0
        self.StartTime = ''
        self.EndTime = ''
        self.Edu = ''
        self.DegCod = ''
        self.College = ''
        self.Dept = ''
        self.Grade = ''
        self.SchCod = ''
        self.UseYr = ''
        self.Stage = '選課關閉'

        self.Name = ''
        self.Id = ''
        self.Department = ''
        self.Grade = 0
        import traceback as TB
        try:
            html = Req.SessGetBS(self.Session, 'selected').find('body').get_text().strip()
            sp = [s.split('：')[1] for s in (' '.join(html.split(' ')[0].replace('\xa0', ' ').split()).split())[0:4]]
            self.Id = sp[0]
            self.Name = sp[1]
            self.Department = sp[2]
            self.Grade = int(sp[3])
        except:
            TB.print_exc()
            print('奇怪的錯誤')
        try:
            html = Req.SessGetBS(self.Session, 'check')
            next_url = Req.Urls['menu4'] + html.select('#header')[0]['src']
            html = Req.SessGetBS(self.Session, next_url)
            a = html.find('table').find('tr').find('td').find('a')
            url = a['href']
            qs = dict(PARSE.parse_qs(PARSE.urlparse(url).query))
            self.StartTime = qs['x1'][0]
            self.EndTime = qs['X2'][0]
            self.Edu = qs['EDU'][0]
            self.DegCod = qs['DEG_COD'][0]
            self.College = qs['college'][0]
            self.Dept = qs['dept'][0]
            self.Grade = qs['grade'][0]
            self.SchCod = qs['SCH_COD'][0]
            self.UseYr = qs['USE_YR'][0]
            self.Stage = a.get_text().strip()
        except:
            TB.print_exc()
            print('選課關閉')

    # 获取正在加选、未选上、选上、失败的课程
    def GetSelectedClass(self):
        html = Req.SessGetBS(self.Session, 'selected')
        res_selected = []
        res_other = []
        for tr in html.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 13:
                tmp = []
                idx = 0
                for td in tds:
                    text = td.get_text().strip()
                    if len(tds) == 13 and idx == 4:
                        tmp.append('')
                        idx += 1
                    if idx == 5:
                        tmp.append(text)
                        tmp.append(td.find('a')['href'])
                    else:
                        tmp.append(text)
                    idx += 1
                c = ClassSelect(tmp)
                if c.Get == '選上':
                    res_selected.append(c)
                else:
                    res_other.append(c)
        return res_selected, res_other

    # 加退選
    def Select2(self, type_, number_, point_):
        return self.Select(type_, number_, point_, 2)

    # 選課
    def Select(self, type_, number_, point_, step):
        Req.SessPost(self.Session, 'step2', {
            "D1": type_,
            "C1": number_,
            "T1": point_,
            "D2": "N",
            "C2": "",
            "T2": "",
            "D3": "N",
            "C3": "",
            "T3": "",
            "D4": "N",
            "C4": "",
            "T4": "",
            "D5": "N",
            "C5": "",
            "T5": "",
            "D6": "N",
            "C6": "",
            "T6": "",
            "D7": "N",
            "C7": "",
            "T7": "",
            "D8": "N",
            "C8": "",
            "T8": "",
            "D9": "N",
            "C9": "",
            "T9": "",
            "D10": "N",
            "C10": "",
            "T10": "",
            "D11": "N",
            "C11": "",
            "T11": "",
            "D12": "N",
            "C12": "",
            "T12": "",
            "D13": "N",
            "C13": "",
            "T13": "",
            "D14": "N",
            "C14": "",
            "T14": "",
            "D15": "N",
            "C15": "",
            "T15": "",
            "X1": self.StartTime,
            "X2": self.EndTime,
            "MAX_ADD": "15",
            "DEG_COD": self.DegCod,
            "college": self.College,
            "dept": self.Dept,
            "grade": self.Grade,
            "S_class": 0,
            "M_DPT_COD": "",
            "S_DPT_COD": "",
            "EDU": self.Edu,
            "SCH_COD": self.SchCod,
            "USE_YR": self.UseYr,
            "step": step
        })
        return True