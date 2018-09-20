# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

class ClassSelect(object):
    def __init__(self, data):
        self.Data = data

        '''
        self.Get = array[0]
        self.Department = array[1]
        self.Number = array[2]
        self.Grade = array[3]
        self.Code = array[4]
        self.Name = array[5]
        self.Url = array[6]
        self.Point = array[7]
        self.Stage = array[8]
        self.Credit = array[9]
        self.YearSemester = array[10]
        self.CompulsoryElective = array[11]
        self.Teacher = array[12]
        self.Room = array[13]
        self.Context = array[14]
        '''

    @property
    def Get(self):
        return self.Data[0]

    @property
    def Department(self):
        return self.Data[1]

    @property
    def Number(self):
        return self.Data[2]

    @property
    def Name(self):
        return self.Data[5]

    @property
    def Point(self):
        return self.Data[7]

    @property
    def Teacher(self):
        return self.Data[12]

    @property
    def Room(self):
        return self.Data[13]

    