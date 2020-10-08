from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework import viewsets
from django.middleware.csrf import get_token
import datetime, time
import MySQLdb
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

import json
import hashlib

from .models import User
from .models import Datastatus

#这个可能需要放入login
engine_ts = create_engine('mysql://sopython_root:Free0921@127.0.0.1:3306/sopython_aistocks?charset=utf8&use_unicode=1')
tspro = ts.pro_api('cb01935d73e23f6d59991c576f31534e13659f76be1a94ae403532e3')

'''
from stocks.serializer import UserSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''

def hash_code(s, salt='mypython'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

# csrf认证
@require_http_methods(["GET"])
def get_csrf(request):
    response = {}

    # 生成 csrf 数据，发送给前端
    csrf_token = get_token(request)

    #response['Access-Control-Allow-Origin'] = '*'

    response['msg'] = 'success'
    response['error_num'] = 0
    response['token'] = csrf_token
    return JsonResponse(response)

# 获取stocklist
@require_http_methods(["GET"])
def get_stocklist(request):
    response = {}
    selectedStocks = []

    isLogin = False
    #verify if is a valid user
    try:
        username = request.COOKIES["user_name"]
        isLogin = request.COOKIES["is_login"]
    except Exception as e:
        response['msg'] = 'Not a valid user'
        response['error_num'] = 1001
        return JsonResponse(response)


    #print("cookie name:" + username + " session name:" + request.session["user_name"])
    if not (isLogin and (request.session["user_name"] == username)):
        response['msg'] = 'session is closed'
        response['error_num'] = 1001
        return JsonResponse(response)
     
    #获取自选股信息
    try:
        user = User.objects.get(name=username)
        selectedStocks = user.stocks.split(";")
    except :
        response['msg'] = '用户不存在！'
        response['error_num'] = 1001
        return JsonResponse(response)

    #check whether the stocklist has been updated this day
    if (Datastatus.objects.count() == 0):
        status = Datastatus()
        status.save()

    #如果当天没有更新过，就先更新一下stocklist
    if not (Datastatus.objects.filter(id=1).first().update_date == datetime.date.today()):
        # 从tushare获取数据
        df = tspro.stock_basic(exchange='', list_status='L', fields='symbol,name,area,industry,market,exchange,list_date,is_hs')

        #增加id列
        df.insert(0, 'id', range(len(df)))

        #增加一列：本股票交易信息最后更新日期
        df['update_date'] = None

        #存入mysql表
        res = df.to_sql('stocks_stocklist', engine_ts, index=False, if_exists='replace', chunksize=5000)

        #表示当天股票列表已更新
        Datastatus.objects.filter(id=1).update(update_date=datetime.date.today())

        #获取stocklist表里的数据返回
        ''' e留着供参考
        datalist = Stocklist.objects.all()
        json_data = serialize('json', datalist) # str
        json_data = json.loads(json_data) # 序列化成json对象
        '''
        
    #get the stocklist from DB
    try:
        conn = MySQLdb.connect(host="localhost", user="sopython_root", passwd="Free0921", db="sopython_aistocks", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("select id, symbol, name, market, exchange from stocks_stocklist")
            datarows = cursor.fetchall()
            #print(datarows[0], datarows[1])

            rows = list(datarows)
            #print(rows[0], rows[1])
            for row in rows:
                if (row['symbol'] in selectedStocks):
                    row.update({'selected': 'true'})
                else:
                    row.update({'selected': 'false'})
                    
                #print(row)
    finally:
            conn.close()

    response['msg'] = 'success'
    response['error_num'] = 0
    response['datalist'] = rows
    #response['datalist'] = json.loads(serializers.serialize("json", rows))
    
    return JsonResponse(response, safe=False)

# add new user
@require_http_methods(["POST"])
def add_user(request):
    response = {}
    message = 'success'
    error_num = 0
    
    #get the string
    dic0 = list(request.POST.keys())
    #print(dic0)
    #get the value pair from the string
    dic = eval(dic0[0])

    username = dic.get('name')
    password = dic.get('password')
    email = dic.get('email')
    
    print(password)

    sameuser = User.objects.filter(name=username)
    if sameuser:
        message = '用户名已经存在'
        error_num = 1
    elif (User.objects.filter(email=email)):
        message = '该邮箱已经被注册了！'
        error_num = 1
    else:
        try:
            new_user = User()
            new_user.name = username
            
            passcode = hash_code(password)
            #print("passcode:" + passcode)
            new_user.password = passcode
            new_user.email = email
            new_user.stocks = ''

            new_user.save()
            message = 'success'
            error_num = 0
        except Exception as e:
            message = str(e)
            error_num = 1

    response['msg'] = message
    response['error_num'] = error_num
    return JsonResponse(response)

@require_http_methods(["POST"])
def login(request):
    response = {}
    message = 'success'
    error_num = 0

    #get the string
    dic0 = list(request.POST.keys())
    #get the value pair from the string
    dic = eval(dic0[0])
    #print(dic)

    username = dic.get('name')
    password = dic.get('password')

    #print('user:', username)

    try:
            user = User.objects.get(name=username)
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name

                #print(request.COOKIES.get("csrftoken"))

                response['user_id'] = user.id
                response['user_name'] = user.name
                response['is_login'] = True
                #response['stocks'] = user.stocks
                #selectedStocks = user.stocks.split()

                message = 'success'
                error_num = 0
            else:
                message = '密码不正确！'
                error_num = 1
    except :
            message = '用户不存在！'
            error_num = 1

    response['msg'] = message
    response['error_num'] = error_num
    return JsonResponse(response)

@require_http_methods(["POST"])
def logout(request):
    response = {}
    message = 'success'
    error_num = 0

    try:
        request.session.flush()
    except Exception as e:
        message = str(e)
        error_num = 1
        
    response['msg'] = message
    response['error_num'] = error_num
    return JsonResponse(response)
 
@require_http_methods(["POST"]) 
def save_selected(request):
    response = {}
    selectedStocks = []

    isLogin = False
    #verify if is a valid user
    try:
        username = request.COOKIES["user_name"]
        isLogin = request.COOKIES["is_login"]
    except Exception as e:
        response['msg'] = 'Not a valid user'
        response['error_num'] = 1001
        return JsonResponse(response)


    if not (isLogin and (request.session["user_name"] == username)):
        response['msg'] = 'session is closed'
        response['error_num'] = 1001
        return JsonResponse(response)
        
    #get the data
    dic0 = list(request.POST.keys())
    #get the value pair from the string
    dic = eval(dic0[0])
    #print(dic)

    symbol = dic.get('symbol')
    selected = dic.get('selected')
    
    print("symbol:" + symbol + " select:" + selected)
     
    #获取自选股信息
    try:
        user = User.objects.get(name=username)
        str1= user.stocks
        selectedStocks = str1.split(';')
        
        if selected == "true":
            if len(selectedStocks) >= 20:
                response['msg'] = 'The maxium number of favorite stocks is 20'
                response['error_num'] = 1001
                return JsonResponse(response)
            else:
                selectedStocks.append(symbol)
        else:
            selectedStocks.remove(symbol)
        
        #print("s2:", selectedStocks)
        
        selectedstr = ";".join(selectedStocks)
        user.stocks = selectedstr
        user.save()

    except Exception as e:
        response['msg'] = 'Save favorite failed'
        response['error_num'] = 1001
        print(str(e))
        return JsonResponse(response)

    response['msg'] = 'success'
    response['error_num'] = 0
    return JsonResponse(response)
