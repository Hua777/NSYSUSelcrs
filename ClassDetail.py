# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

class ClassDetail(object):
    def __init__(self, data):
        self.Data = data
        self.Title = ['Change','Description','MultipleCompulsory','Department','SDepartment','Number','Grade','Class','Name','SName','Url','Credit','YearSemester','CompulsoryElective','Restrict','Select','Selected','Remaining','Teacher','STeacher','Room','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Context']
        '''
        self.Change = 0
        self.Description = 1
        self.MultipleCompulsory = 2
        self.Department = 3
        self.SDepartment = 4
        self.Number = 5
        self.Grade = 6
        self.Class = 7
        self.Name = 8
        self.SName = 9
        self.Url = 10
        self.Credit = 11
        self.YearSemester = 12
        self.CompulsoryElective = 13
        self.Restrict = 14
        self.Select = 15
        self.Selected = 16
        self.Remaining = 17
        self.Teacher = 18
        self.STeacher = 19
        self.Room = 20
        self.Monday = 21
        self.Tuesday = 22
        self.Wednesday = 23
        self.Thursday = 24
        self.Friday = 25
        self.Saturday = 26
        self.Sunday = 27
        self.Context = 28
        '''

        self.Tag = None

    def ToDict(self):
        return {self.Title[i]: self.Data[i] for i in range(len(self.Title))}

    @property
    def Number(self):
        return self.Data[5]

    @property
    def Restrict(self):
        return self.Data[14]

    @property
    def Select(self):
        return self.Data[15]

    @property
    def Selected(self):
        return self.Data[16]

    @property
    def Remaining(self):
        return self.Data[17]

    @property
    def Department(self):
        return self.Data[3]

    @property
    def SDepartment(self):
        return self.Data[4]

    @property
    def Name(self):
        return self.Data[8]

    @property
    def SName(self):
        return self.Data[9]

    @property
    def Url(self):
        return self.Data[10]

    @property
    def Teacher(self):
        return self.Data[18]

    @property
    def STeacher(self):
        return self.Data[19]

    @property
    def Table(self):
        return self.Data[21:28]

    