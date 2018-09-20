# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

import opencc as CC

# 简体字转换成繁体字
def S2T(line):
    cc = CC.OpenCC('s2t')
    return cc.convert(line)

# 繁体字转换成简体字
def T2S(line):
    cc = CC.OpenCC('t2s')
    return cc.convert(line)