# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

import CC

from ClassDetail import ClassDetail
from ClassesPage import ClassesPage

import pymysql as PYSQL

'''
for Id,\
    Change,\
    Description,\
    MultipleCompulsory,\
    Department,\
    SDepartment,\
    Number,\
    Grade,\
    Class,\
    Name,\
    SName,\
    Url,\
    Credit,\
    YearSemester,\
    CompulsoryElective,\
    Restrict,\
    Select,\
    Selected,\
    Remaining,\
    Teacher,\
    STeacher,\
    Room,\
    Monday,\
    Tuesday,\
    Wednesday,\
    Thursday,\
    Friday,\
    Saturday,\
    Sunday,\
    Context in self.Query(''):
'''

class ClassesDB(object):
    def __init__(self):
        self.Config = {
            'host':'localhost',
            'user':'user',
            'password':'password',
            'database':'database',
            'charset': 'utf8mb4'
        }

    def Connect(self):
        self.Connection = PYSQL.connect(self.Config['host'], self.Config['user'], self.Config['password'], self.Config['database'])
        self.Cursor = self.Connection.cursor()

    def Execute(self, sql):
        self.Cursor.execute(sql)

    def Commit(self):
        self.Connection.commit()

    def Disconnect(self):
        self.Cursor.close()
        self.Connection.close()

    def Query(self, sql):
        connection = PYSQL.connect(self.Config['host'], self.Config['user'], self.Config['password'], self.Config['database'])
        cursor = connection.cursor()
        row_num = cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def FeedBack(self, name, email, subject, message):
        self.Connect()
        self.Execute("INSERT INTO `feedbacks` VALUES (0, '%s','%s','%s','%s');" % (name, email, subject, message))
        self.Commit()
        self.Disconnect()

    def GetFeedBacks(self):
        return self.Query('SELECT * FROM `feedbacks`;')

    # 根据信息获取课程
    def Classes(self, dept, teacher, name, number, week, sect):
        dept = CC.S2T(dept)
        teacher = CC.S2T(teacher)
        name = CC.S2T(name)
        result = []
        sql = "SELECT * FROM `classes` WHERE `Department` LIKE '%" + str(dept) + "%' AND `Teacher` LIKE '%" + str(teacher) + "%' AND `Name` LIKE '%" + str(name) + "%' AND `Number` LIKE '%" + str(number) + "%';"
        for r in self.Query(sql):
            c = ClassDetail(r[1:])
            t = c.Table
            if week != '' and sect != '' and t[int(week) - 1].find(sect) >= 0:
                result.append(c)
            elif week == '' and sect != '':
                for i in range(7):
                    if t[i].find(sect) >= 0:
                        result.append(c)
            elif week != '' and sect == '':
                if t[int(week) - 1] != '':
                    result.append(c)
            elif week == '' and sect == '':
                result.append(c)
        return result

    # 获取系所列表（繁体、简体）
    def GetDepartments(self):
        result = []
        for Department, SDepartment in self.Query("SELECT `Department`, `SDepartment` FROM `classes` GROUP BY `Department` ORDER BY `Department` ASC;"):
            result.append([Department, SDepartment])
        return result

    # 获取老师列表（繁体、简体）
    def GetTeachers(self):
        result = []
        for Teacher, STeacher in self.Query("SELECT `Teacher`, `STeacher` FROM `classes` GROUP BY `Teacher` ORDER BY `Teacher` ASC;"):
            result.append([Teacher, STeacher])
        return result

    # 透过系所获取课程列表
    def GetClassByDepartment(self, department):
        result = []
        for r in self.Query("SELECT * FROM `classes` WHERE `Department` LIKE '%" + department + "%' GROUP BY `Number` ORDER BY `Number` ASC;"):
            result.append(ClassDetail(r[1:]))
        return result

    # 透过课程代号获取课程
    def GetClassByNumber(self, number):
        result = []
        for r in self.Query("SELECT * FROM `classes` WHERE `Number` = '" + number + "';"):
            result.append(ClassDetail(r[1:]))
        return result[0]

    # 透过课程代号爬取课程
    def CrawlClassByNumber(self, number):
        cp = ClassesPage()
        cp.SetNumber(number)
        return cp.Crawl(True)[0]

    # 开始爬虫所有课程
    def Crawl(self):
        self.Connect()
        self.Execute('TRUNCATE `classes`')
        self.Commit()
        cp = ClassesPage()
        print(1)
        result = cp.Crawl()
        print(len(result))
        for r in result:
            self.Execute("INSERT INTO `classes` VALUES (0, '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % tuple(r))
        self.Commit()
        for i in range(2, cp.Pages + 1):
            cp.SetPage(i)
            print(i)
            result = cp.Crawl()
            print(len(result))
            for r in result:
                self.Execute("INSERT INTO `classes` VALUES (0, '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % tuple(r))
            self.Commit()
        self.Disconnect()