from main import hpfuncs
from machine import UART
global uart
uart = UART(1, 9600)
uart.init(9600,bits = 8,parity = 0,stop = 1,rx = 32,tx = 33,timeout = 10, timeout_char=50)
import uasyncio as asyncio
from main.mqtt_as import MQTTClient
from config import config
import time
from time import sleep
import machine

topic_sub_setp =  b"" + config['maintopic'] + "/setpoint/set"
topic_sub_state =  b"" + config['maintopic'] + "/state/set"
topic_sub_fanmode =  b"" + config['maintopic'] + "/fanmode/set"
topic_sub_swingmode =  b"" + config['maintopic'] + "/swingmode/set"
topic_sub_mode =   b"" + config['maintopic'] + "/mode/set"
topic_sub_doinit =  b"" + config['maintopic'] + "/doinit"
topic_sub_restart =  b"" + config['maintopic'] + "/restart"
topic_sub_watchdog =  b"" + config['maintopic'] + "/watchdog"
topics = [topic_sub_setp, topic_sub_state, topic_sub_doinit, topic_sub_fanmode, topic_sub_mode, topic_sub_swingmode, topic_sub_restart, topic_sub_watchdog]

def int_to_signed(intval):
    if intval > 127:
        return (256-intval) * (-1)
    else:
        return intval

#mqtt stuff
def sub_cb(topic, msg, retained, properties=None):
    runwrite = True
    hpfuncs.logprint(str(topic) + " -- " + str(msg))
    ################################################
    #setpoint
    if topic == topic_sub_setp:
        try:
            values = hpfuncs.setpointVal(int(float(msg)))
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
    ################################################
    #restart
    if topic == topic_sub_restart:
        try:
            machine.reset()
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
        ################################################
    # state
    elif topic == topic_sub_state:
        try:
            values = hpfuncs.stateControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
    ################################################
    # swingstate
    elif topic == topic_sub_swingmode:
        try:
            values = hpfuncs.swingControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
    ################################################
    # mode
    elif topic == topic_sub_mode:
        try:
            values = hpfuncs.modeControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
    ################################################
    # fanmode
    elif topic == topic_sub_fanmode:
        try:
            values = hpfuncs.fanControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
    ################################################
    # do init
    elif topic == topic_sub_doinit:
        myvals = hpfuncs.queryall()
        hpfuncs.logprint("initial read")
        for i in myvals:
            uart.write(bytearray(i))
            sleep(0.2)
        hpfuncs.logprint("initial read done")
        runwrite = False

    ################################################
    # do watchdog
    elif topic == topic_sub_watchdog:
        myvals = hpfuncs.watchdog()
        for i in myvals:
            uart.write(bytearray(i))
            sleep(0.2)
        hpfuncs.logprint("watchdog processed")
        runwrite = False
    ################################################
    if runwrite == True and values != False:
        #print(values)
        for i in values:
            hpfuncs.logprint("writing: " + str(i))
            uart.write(bytearray(i))
            sleep(0.2)


def chunkifyarray(vals):
    val_length = len(vals)
    start = 0
    rest_size = val_length
    myresult = []
    while rest_size > 14:
        lengde= int(vals[start+6])
        chunk_size = lengde + 8
        chunk_end = start + int(vals[start+6]) + 8
        myresult.append(vals[start:chunk_end])
        start = (start + chunk_size)
        rest_size = rest_size - chunk_size
    return myresult


# subscribe to topics
async def conn_han(client):
    hpfuncs.logprint("subscribing to MQTT topics")
    for i in topics:
        await client.subscribe(i,1)
    hpfuncs.logprint("subscribtion done")

# first run to collect values and run watchdog
async def firstrun_and_watchdog(client, version):
    firstrun = False
    await asyncio.sleep(10)
    if firstrun == False:
        await client.publish(config['maintopic'] + '/doinit', "firstrun")
        hpfuncs.logprint("init firstrun")
        await client.publish(config['maintopic'] + '/version', version, retain=True)
        hpfuncs.logprint("publish version")
        firstrun = True
    while True:
        await asyncio.sleep(60)
        hpfuncs.logprint("watchdog publishes..")
        await client.publish(config['maintopic'] + '/watchdog', "get")
        hpfuncs.logprint("running watchdog..")

async def process_event(client, event, event_data):
    if(event == "187"):
        roomtemp = int_to_signed(event_data)
        await client.publish(config['maintopic'] + '/roomtemp', str(roomtemp), qos=1)
    if(event == "179"):
        setpoint = event_data
        await client.publish(config['maintopic'] + '/setpoint/state', str(setpoint), retain=True, qos=1)
    if(event == "128"):
        state = hpfuncs.inttostate[event_data]
        await client.publish(config['maintopic'] + '/state/state', str(state), retain=True, qos=1)
    if(event == "160"):
        fanmode = hpfuncs.inttofanmode[event_data]
        await client.publish(config['maintopic'] + '/fanmode/state', str(fanmode), retain=True, qos=1)
    if(event == "163"):
        swingmode = hpfuncs.inttoswing[event_data]
        await client.publish(config['maintopic'] + '/swingmode/state', str(swingmode), retain=True, qos=1)
    if(event == "176"):
        mode = hpfuncs.inttomode[event_data]
        await client.publish(config['maintopic'] + '/mode/state', str(mode), retain=True, qos=1)
    if(event == "190"):
        outdoortemp = int_to_signed(event_data)
        if (outdoortemp != 127):
            # 127 seems to be "temperature not available"
            await client.publish(config['maintopic'] + '/outdoortemp', str(outdoortemp), qos=1)


async def receiver(client):
    hpfuncs.logprint("Starting receiver loop")
    sreader = asyncio.StreamReader(uart)
    try:
        while True:
            hpfuncs.logprint("awaiting data from heatpump")
            serdata = await sreader.read(2048)
            if serdata is not None:
                readable = list()
                for i in serdata:
                    readable.append(str(int(i)))
                hpfuncs.logprint("length of data: " + str(len(readable)))
                chunks = chunkifyarray(readable)
                for data in chunks:
                    hpfuncs.logprint(data)
                    await client.publish(config['maintopic'] + '/debug/fullstring', str(data))
                    if len(data) == 17:
                        await process_event(client, str(data[14]), int(data[15]))
                    elif len(data) == 15:
                        await process_event(client, str(data[12]), int(data[13]))
    except Exception as e:
        hpfuncs.logprint(e)


async def connect_to_client(client):
    await client.connect()

async def main_loop(client, version):
    await asyncio.gather(connect_to_client(client), receiver(client), firstrun_and_watchdog(client, version))

def _handle_exception(loop, context):
    print("Unhandled loop exception caught:")
    print(context["exception"])
    print("resetting...")
    machine.reset()

def start_loop(version):
    config['subs_cb'] = sub_cb
    config['connect_coro'] = conn_han
    MQTTClient.DEBUG = True
    client = MQTTClient(config)

    from main import aioprof
    aioprof.enable()
    try:
        asyncio.get_event_loop().set_exception_handler(_handle_exception)
        asyncio.run(main_loop(client, version))
    finally:
        aioprof.report()
