from time import sleep
from machine import RTC
import ntptime
try:
    ntptime.settime()
except Exception as e:
    print(e)

OP_CODE_SWING = 163
OP_CODE_MODE = 176
OP_CODE_FAN = 160
OP_CODE_STATE = 128
OP_CODE_TARGET_TEMP = 179
OP_CODE_ROOM_TEMP = 187
OP_CODE_OUTDOOR_TEMP = 190
OP_CODE_FUNCTION_MODE = 247
OP_CODE_UNKNOWN_1 = 135
OP_CODE_UNKNOWN_2 = 203
OP_CODE_UNKNOWN_3 = 136
OP_CODE_UNKNOWN_4 = 134
OP_CODE_UNKNOWN_5 = 144
OP_CODE_UNKNOWN_6 = 148

modetoint = {"auto":65, "cool":66, "heat":67, "dry":68, "fan_only":69}
inttomode = dict(map(reversed, modetoint.items()))

fanmodetoint = {"quiet":49, "lvl_1": 50, "lvl_2":51, "lvl_3":52, "lvl_4":53, "lvl_5":54, "auto":65}
inttofanmode = dict(map(reversed, fanmodetoint.items()))

swingtoint = {"off": 49, "on":65}
inttoswing = dict(map(reversed, swingtoint.items()))

statetoint = {"ON":48, "OFF":49}
inttostate = dict(map(reversed, statetoint.items()))

functionmodetoint = {"normal":0, "hi_power":1, "silent":2, "eco":3}
inttofunctionmode = dict(map(reversed, functionmodetoint.items()))

def checksum(msg,function):
    numb = 434 - msg - function
    if numb > 256:
        retval = numb - 256
    else:
        retval = numb
    return retval

def calc_message_checksum(data):
    # somehow byte 0 (always 2) is not included in the checksum.
    payload_slice = data[1:len(data)]
    return (-sum(payload_slice)) & 0xFF

def build_send_message(operation, *args):
    message = (2,0,3,16,0,0,6 + len(args),1,48,1,0,1 + len(args), operation) + args
    result = message + tuple([calc_message_checksum(message)])
    return result

def logprint(msg):
    rtc = RTC()
    t = rtc.datetime()
    #(2020, 4, 22, 2, 8, 43, 38, 88387)
    # yyyy, m, dd, ?, h, mm, ss, ms
    timestamp = str(t[2]) + "-" + str(t[1]) + "-" + str(t[0]) + " " + str(t[4]) + ":" + str(t[5]) + ":" + str(t[6]) + "." + str(t[7])
    result = str(timestamp) + " -> " + str(msg)
    print(result)
 
def control(op_code, value):
    return (build_send_message(op_code, value), build_send_message(op_code))

def swingControl(msg):
    try:
        function_value = swingtoint[msg.decode("utf-8")]
        myvalues = control(OP_CODE_SWING, function_value)
    except Exception as e:
        logprint(e)
        myvalues = False
    return myvalues

def modeControl(msg):
    try:
        function_value = modetoint[msg.decode("utf-8")]
        myvalues = control(OP_CODE_MODE, function_value)
    except Exception as e:
        logprint(e)
        myvalues = False
    return myvalues

def fanControl(msg):
    try:
        function_value = fanmodetoint[msg.decode("utf-8")]
        myvalues = control(OP_CODE_FAN, function_value)
    except Exception as e:
        logprint(e)
        myvalues = False
    return myvalues

def stateControl(msg):
    try:
        function_value = statetoint[msg.decode("utf-8")]
        myvalues = control(OP_CODE_STATE, function_value)
    except Exception as e:
        logprint(e)
        myvalues = False
    return myvalues

def setpointVal(msg):
    try:
        function_value = int(msg)
        myvalues = control(OP_CODE_TARGET_TEMP, function_value)
    except Exception as e:
        logprint(e)
        myvalues = False
    return myvalues

def functionmodeControl(msg):
    try:
        function_value = functionmodetoint[msg.decode("utf-8")]
        myvalues = control(OP_CODE_FUNCTION_MODE, function_value)
    except Exception as e:
        logprint(e)
        myvalues = False
    return myvalues

def queryall():
     bootlist = []
     bootlist.append(build_send_message(OP_CODE_STATE))
     bootlist.append(build_send_message(OP_CODE_MODE))
     bootlist.append(build_send_message(OP_CODE_TARGET_TEMP))
     bootlist.append(build_send_message(OP_CODE_FAN))
     bootlist.append(build_send_message(OP_CODE_UNKNOWN_1))
     bootlist.append(build_send_message(OP_CODE_SWING))
     bootlist.append(build_send_message(OP_CODE_ROOM_TEMP))
     bootlist.append(build_send_message(OP_CODE_OUTDOOR_TEMP))
     bootlist.append(build_send_message(OP_CODE_FUNCTION_MODE))
     bootlist.append(build_send_message(OP_CODE_UNKNOWN_2))
     bootlist.append(build_send_message(OP_CODE_UNKNOWN_3))
     #bootlist.append(build_send_message(OP_CODE_UNKNOWN_4))
     bootlist.append(build_send_message(OP_CODE_UNKNOWN_5))
     bootlist.append(build_send_message(OP_CODE_UNKNOWN_6))
     return bootlist    

def watchdog():
    bootlist = []
    bootlist.append(build_send_message(OP_CODE_ROOM_TEMP))
    bootlist.append(build_send_message(OP_CODE_OUTDOOR_TEMP))
    return bootlist
