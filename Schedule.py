# -*- coding: utf-8 -*-
from ClassesDB import ClassesDB as DB

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

class Schedule(object):
    def __init__(self, agent):
        self.Agent = agent
        self.SectionKey = ['A', '1', '2', '3', '4', 'B', '5', '6', '7', '8', '9', 'C', 'D', 'E', 'F']
        self.DayKey = [0, 1, 2, 3, 4, 5, 6]
        self.Data = {}
        for sk in self.SectionKey:
            self.Data[sk] = {}
            for dk in self.DayKey:
                self.Data[sk][dk] = []
        self.Start()

    def Start(self):
        db = DB()
        self.Select = self.Agent.GetSelectedClass()
        for s in self.Select:
            for c in s:
                new_c = db.GetClassByNumber(c.Number)
                new_c.Tag = c
                self.Add(new_c)

    def Add(self, class_detail):
        table = class_detail.Table
        for i in range(7):
            for n in table[i]:
                same = False
                for c in self.Data[n][i]:
                    if c.Number == class_detail.Number:
                        same = True
                        break
                if not same:
                    self.Data[n][i].append(class_detail)

    def ToHtml(self):
        result = '<table class="table table-bordered table-sm" width="100%">\
                    <thead>\
                        <tr class="text-center">\
                            <th>節</th>\
                            <th>星期一</th>\
                            <th>星期二</th>\
                            <th>星期三</th>\
                            <th>星期四</th>\
                            <th>星期五</th>\
                            <th>星期六</th>\
                            <th>星期日</th></tr></thead><tbody>'
        for sk in self.SectionKey:
            if not sk.isnumeric():
                result += '<tr class="table-active">'
            else:
                result += '<tr class="">'
            result += '<td class="align-middle text-center" width="2%">' + str(sk) + '</td>'
            for dk in self.DayKey:
                result += '<td id="TD' + str(sk) + str(dk) + '" class="align-middle text-center" width="14%">'
                idx = 0
                for c in self.Data[sk][dk]:
                    if idx > 0:
                        result += '<br/>'
                    result += '<a id="C' + str(sk) + str(dk) + str(idx) + '" class="'
                    if c.Tag.Get == '選上':
                        result += 'text-success'
                    elif c.Tag.Get == '登記加選':
                        result += 'text-warning'
                    else:
                        result += 'text-danger'
                    result += '" href="javascript:classclick(\'' + c.Number + '\');">' + c.Number + '<br/>' + c.Name + ('<br/>(' + c.Tag.Point + ')' if c.Tag.Point != '' else '') + '</a>'
                    idx += 1
                result += '</td>'
            result += '</tr>'
        result += '</tbody></table>'
        return result