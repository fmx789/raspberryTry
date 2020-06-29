import requests
import json

def get_code(uid):  #1
    url = "http://112.124.21.59:8000/code?uid=" + uid
    response = requests.get(url)
    print('验证码已成功发送至邮箱，请查收')

def get_token(uid, code):  #2
    url = "http://112.124.21.59:8000/token?uid=" + uid + "&code=" + code
    response = requests.get(url)
    values = json.loads(response.text)
    token = values.get('d')
    print("已成功获取token")
    return token


def get_token2(uid):#, token):                 #15
    url="http://112.124.21.59:8000//auth/app"
    data = dict()
    data['uid']= uid
    headers = dict()
    headers['Access-Token'] = 'eyJhbGciOiJ0aG9yIiwiZXhwIjoxNTkzODYyMzAwLCJwZXJtIjowLCJkYXQiOnsiYXBwaWQiOiJKNkI0V1hUZE5CTW54MmFweGM5Z0dUIiwidWlkIjoiMjAxNzIxMzAzOSJ9fQ==.7a038d4a001a9df496ebf52777ce409be9f627d8ae2edc8e2094bd0c490cec4c'
    response = requests.post(url, data = data, headers = headers)
    values = json.loads(response.text)
    token2 = values.get('d')
    appid = token2.get('appid')
    appkey = token2.get('appkey')
    return appid,appkey

def get_token3(uid,appid,appkey):    #16
    url="http://112.124.21.59:8000/apptoken?uid="+ uid + "&appid="+ appid+ "&appkey="+ appkey
    response = requests.get(url)
    values = json.loads(response.text)
    Token = values.get('d')
    print("已成功获取Token")
    return Token
    
def add_rfid1(Type,Token):#,uid,cid,):      #17 rfid
    url="http://112.124.21.59:8000/ac/rfid"
    #data = dict()
    #data['uid']= '2017213039' #uid
    #data['cid']= '1234567' #str(cid)
    #data['type']=int(Type)
    
    payload={'uid':'2017213039','cid':'6001','type':'2'}
    headers = dict()
    headers['Access-Token'] = str(Token)
    response = requests.post(url, data = payload, headers = headers)
    print(response.text)
    
def add_temp1(uid,Token,temp):
    url="http://112.124.21.59:8000/ac/temp"
    data1=dict()
    data1['uid']=uid
    data1['temp']=float(temp)
    #data2=json.dumps(data1)
    
    # payload = {'uid': '2017213039', 'temp': 100.0}
    
    headers = dict()
    headers['Access-Token'] = str(Token)

    response = requests.post(url, data=data1, headers = headers)

    print(response.text)


def add_temp(uid,temp):#,Token):
    url="http://112.124.21.59:8000/ac/temp"
    payload=dict()
    payload['uid']=str(uid)
    payload['temp']=float(temp)

    headers = dict()
    headers['Access-Token'] = 'eyJhbGciOiJ0aG9yIiwiZXhwIjoxNTkzOTE0OTg4LCJwZXJtIjowLCJkYXQiOnsiYXBwaWQiOiJ0V1o2OUNxaTQ4Z2o0TVg3YmpRVlpDIiwidWlkIjoiMjAxNzIxMzAzOSJ9fQ==.a10470f9ab8ed40127aef3da600d94d5cdcb5235f34e5b2690a46f5bd5213369'

    response = requests.post(url, data=payload, headers = headers)

    print(response.text)
    
    
def add_rfid(Type,uid,rfid):#Token):      #17 rfid
    url="http://112.124.21.59:8000/ac/rfid"
    payload= dict()
    payload['uid']= str(uid) 
    payload['rfid']= str(rfid)
    payload['type']=int(Type)
    
    headers = dict()
    headers['Access-Token'] = 'eyJhbGciOiJ0aG9yIiwiZXhwIjoxNTkzOTE0OTg4LCJwZXJtIjowLCJkYXQiOnsiYXBwaWQiOiJ0V1o2OUNxaTQ4Z2o0TVg3YmpRVlpDIiwidWlkIjoiMjAxNzIxMzAzOSJ9fQ==.a10470f9ab8ed40127aef3da600d94d5cdcb5235f34e5b2690a46f5bd5213369'
    response = requests.post(url, data = payload, headers = headers)