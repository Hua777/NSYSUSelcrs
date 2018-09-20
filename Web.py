# -*- coding: utf-8 -*-

__author__ = "Hua777"
__copyright__ = "Copyright 2018, Hua777"
__version__ = "2.0"
__email__ = "liao.700529@gmail.com"

from flask import Flask, jsonify, request, make_response, render_template, redirect, url_for
import traceback as TB
import os as OS
import requests as REQ
import time

from Agent import Agent
from Schedule import Schedule
from ClassesDB import ClassesDB as DB
from ValidCode import ValidCode, LoadForwardData

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

ValidCodeModel = None

def MyAgent(req):
    try:
        id_ = req.cookies.get('Id')
        return Global['Agents'][id_]
    except:
        return None

Global = {
    'MyAgent': MyAgent,
    'Agents': {},
    'Id': 0
}

# 首页
@app.route('/', methods=['GET'])
def index():
    try:
        global Global
        global ValidCodeModel
        a = Global['MyAgent'](request)
        if a is not None and a.Logined:
            return render_template('index.html', agent = a)
        else:
            a = Agent()
            resp = make_response(render_template('index.html', agent = a, vc = ValidCodeModel, vcread = LoadForwardData))
            resp.set_cookie('Id', str(Global['Id']), expires = time.time() + 1 * 60 * 60)
            Global['Agents'][str(Global['Id'])] = a
            Global['Id'] += 1
            return resp
    except REQ.exceptions.Timeout:
        TB.print_exc()
        return render_template('timeout.html')
    except:
        TB.print_exc()
        return render_template('error.html')

# 关于
@app.route('/about', methods=['GET'])
def about():
    try:
        global Global
        global ValidCodeModel
        a = Global['MyAgent'](request)
        return render_template('about.html', agent = a, vc = ValidCodeModel, vcread = LoadForwardData)
    except:
        TB.print_exc()
        return redirect(url_for('logout'))

# 课程查询
@app.route('/feedback', methods=['GET'])
def feedback():
    try:
        global Global
        global ValidCodeModel
        a = Global['MyAgent'](request)
        return render_template('feedback.html', agent = a, vc = ValidCodeModel, vcread = LoadForwardData)
    except:
        TB.print_exc()
        return redirect(url_for('logout'))

# 登入首页（废弃）
@app.route('/main', methods=['GET'])
def main():
    try:
        return redirect(url_for('selected'))
    except:
        TB.print_exc()
        return redirect(url_for('logout'))

# 目前已经选的课
@app.route('/selected', methods=['GET'])
def selected():
    try:
        global Global
        a = Global['MyAgent'](request)
        return render_template('selected.html', agent = a, schedule = Schedule(a))
    except:
        TB.print_exc()
        return redirect(url_for('logout'))

# 课程查询
@app.route('/classes', methods=['GET'])
def classes():
    try:
        global Global
        a = Global['MyAgent'](request)
        return render_template('classes.html', agent = a, schedule = Schedule(a), db = DB())
    except:
        TB.print_exc()
        return redirect(url_for('logout'))

# 加退选1
@app.route('/select', methods=['GET'])
def select():
    try:
        return redirect(url_for('classes'))
    except:
        TB.print_exc()
        return redirect(url_for('logout'))

# 课程查询
@app.route('/logout', methods=['GET'])
def logout():
    try:
        global Global
        Global['Agents'].pop(request.cookies.get('Id'))
        return redirect(url_for('index'))
    except:
        TB.print_exc()
        return redirect(url_for('index'))

'''''''''''''''''''''''''''''''''''''''''''''
                    API Start
'''''''''''''''''''''''''''''''''''''''''''''

# 登入
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        global Global
        a = Global['MyAgent'](request)
        data = request.get_json(force=True)
        db = DB()
        login = a.Login(data['username'], data['password'], data['validcode'])
        if login[0]:
            srcpath = 'static/img/validcode/' + data['validcodeSrc']
            corpath = 'static/img/validcode/' + data['validcode'] + '.' + data['validcodeSrc']
            OS.rename(srcpath, corpath)
        return (jsonify({'check': login[0], 'msg': login[1]}))
    except:
        TB.print_exc()
        return (jsonify({'check': False}))

# 单一课程资讯查询
@app.route('/api/classinfo', methods=['POST'])
def api_classinfo():
    try:
        data = request.get_json(force=True)
        db = DB()
        c = db.CrawlClassByNumber(data['number'])
        d = c.ToDict()
        d['Check'] = True
        return (jsonify(d))
    except:
        TB.print_exc()
        return (jsonify({'check': False}))

# 课程资讯查询
@app.route('/api/classes', methods=['POST'])
def api_classes():
    try:
        data = request.get_json(force=True)
        db = DB()
        cs = db.Classes(data['dept'], data['teacher'], data['name'], data['number'], data['week'], data['sect'])
        result = []
        for c in cs:
            result.append(c.ToDict())
        return (jsonify(result))
    except:
        TB.print_exc()
        return (jsonify({'check': False}))

# 選課
@app.route('/api/select', methods=['POST'])
def api_select():
    try:
        global Global
        a = Global['MyAgent'](request)
        data = request.get_json(force=True)
        if a.Stage == '選課關閉':
            return (jsonify({'check': False}))
        else:
            a.Select2(data['type'], data['number'], data['point'])
            return (jsonify({'check': True}))
    except:
        TB.print_exc()
        return (jsonify({'check': False}))

# FeedBack
@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    try:
        data = request.get_json(force=True)
        db = DB()
        db.FeedBack(data['name'], data['email'], data['subject'], data['message'])
        return (jsonify({'check': True}))
    except:
        TB.print_exc()
        return (jsonify({'check': False}))

# Schedule
@app.route('/api/schedule', methods=['POST'])
def api_schedule():
    try:
        global Global
        a = Global['MyAgent'](request)
        s = Schedule(a)
        return (jsonify({'check': True, 'html': s.ToHtml()}))
    except:
        TB.print_exc()
        return (jsonify({'check': False}))

# Get FeedBack
@app.route('/api/get/feedbacks', methods=['GET'])
def api_get_feedbacks():
    db = DB()
    return (jsonify(db.GetFeedBacks()))

'''''''''''''''''''''''''''''''''''''''''''''
                    API End
'''''''''''''''''''''''''''''''''''''''''''''

@app.errorhandler(404)
def not_found(error):
    return render_template('notfound.html')

@app.errorhandler(500)
def program_error(error):
    return render_template('error.html')

if __name__ == '__main__':
    ValidCodeModel = ValidCode()
    '''
    Start bug: 必須建立模型後隨便預測一次，否則出錯。
    '''
    images_f, numbers_f = LoadForwardData('static/img/validcode/1136.test.jpg')
    print(ValidCodeModel.Forward(images_f))
    '''
    End bug
    '''
    app.run(port=80, host='0.0.0.0', debug=True)

