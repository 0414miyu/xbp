# doyolab package
# ver1.0 20200714
# ver1.1 20220123

import sys
import glob
import serial
import os
import time
import requests
import datetime

def get_SerialPortsList():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def set_serial(port,baudrate):
    """
    :param port:
    :param baudrate:
    :return: serial
    """
    ser = serial.Serial()
    ser.port = port  #Arduinoのポート確認
    ser.baudrate = baudrate  # Arduinoと同じボーレート
    ser.setDTR(False)  # DTRを常にLOWにしReset阻止
    ser.open()
    time.sleep(1)
    ser.flushInput()
    # ser.readline()
    print("set_serial success")
    return ser

def addData_To_textfile(filepath,data):
    """
    :param filepath:
    :param data:
    :return: nothing
    """
    with open(filepath, mode='a') as f:
        if type(data) is list:
            mydata=''
            for value in data:
                mydata= mydata + str(value) + ','
            mydata=mydata[:-1]
        else:
            mydata=str(data)
        f.write('\n')
        f.write(mydata)

def remove_file(filepath):
    """
    :param filepath:
    :return:nothing
    """
    try:
        os.remove(filepath)
    except:
        pass



def sendData_To_dfLink(user_key='',sub_id='',date_data='',int_data='',float_data='',text_data='',pkey=''):
    # payload = {'user_key': user_key, 'sub_id': sub_id, 'date_data': date_data, 'int_data': int_data, 'float_data': float_data, 'text_data': text_data}
    payload = {}
    if user_key !='':
        payload['user_key']=user_key
    if user_key !='':
        payload['sub_id']=sub_id    
    if date_data !='':
        payload['date_data']=date_data
    if int_data !='':
        payload['int_data']=int_data
    if float_data !='':
        payload['float_data']=float_data
    if text_data !='':
        payload['text_data']=text_data
    if pkey !='':
        payload['pkey']=pkey
    response = requests.post("https://doyolab.net/appli/dflink/add", data=payload)

    return response.text

def getData_From_dfLink(user_key="",pkey="",data_limit=1):
    payload = {'user_key': user_key, 'pkey': pkey, 'data_limit':data_limit}
    response = requests.post("https://doyolab.net/appli/dflink/raw_data", data=payload)

    response_str=response.text
    my_data=[]
    if response_str=='データがありません':
        ret=""
    else:
        ret=response_str.split("<br>")
        cnt=0
        for data in ret:
            if cnt>1:
                my_data.append(data.split(","))
            cnt=cnt+1
        ret=my_data
    return ret

def sendMessage_To_Line(token,message):
    payload = {'token': token, 'message': message}
    response = requests.post("https://doyolab.net/appli/dflink/line", data=payload)
    return response.text


def get_now_time():
    return datetime.datetime.now().time()

def get_now():
    return datetime.datetime.now()
