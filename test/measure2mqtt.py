# Simple Python script to read the frequency measurement from an HP 53131A over GPIB and
# a voltage of a Siglent SDM2065X. The results are sent to an MQTT broker on a local server
# running InfluxDB and Grafana.

# Prerequisites:
# - pip install pyvisa-py
# - pip install gpib-ctypes
# - python-vxi11 from https://github.com/python-ivi/python-vxi11

import pyvisa
import vxi11
import time
import threading
from paho.mqtt import client as mqtt_client


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker\n")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client('FreqCounter')
    client.on_connect = on_connect
    broker = '192.168.20.30'
    port = 1883
    client.connect(broker, port)
    return client


def check_user_input():
    global run
    key = input('Press any key to stop taking measurements ...\n')
    run = False


def check_measurement():
    global run
    client = connect_mqtt()
    client.loop_start()
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    print(str(resources))

    # HP 53131A
    print('Instrument 1')
    print('------------')
    inst1 = rm.open_resource('GPIB0::10::INSTR')
    inst1.write('*RST')
    inst1.write('*CLS')
    inst1.write('*SRE 0')
    inst1.write('*ESE 0')
    print('Identification: ' + inst1.query('*IDN?')[:-1])
    print('Options:        ' + inst1.query('*OPT?')[:-1])
    print('')
    inst1.write(":FUNC 'FREQ 1'")
    inst1.write(':FREQ:ARM:STAR:SOUR IMM')
    inst1.write(':FREQ:ARM:STOP:SOUR TIM')
    inst1.write(':FREQ:ARM:STOP:TIM .100')

    # Siglent SDM3065X
    print('Instrument 2')
    print('------------')
    inst2 = vxi11.Instrument("192.168.20.235")
    print('Identification: ' + inst2.ask('*IDN?'))
    print('')
    inst2.write('CONF:VOLT:DC')

    timeout = time.time()
    while run:
        if time.time() > timeout:
            freq_hp53131a = float(inst1.query('READ?')[:-1])
            volt_sdm3065x = float(inst2.ask('MEAS:VOLT:DC?'))
            client.publish('freqcounter/freq_hp53131a', '%.2f' % freq_hp53131a)
            client.publish('freqcounter/volt_sdm3065x', '%.3e' % volt_sdm3065x)
            timeout = time.time() + 1  # seconds
    inst1.close()
    inst2.close()

run = True
thread1 = threading.Thread(target=check_measurement)
thread2 = threading.Thread(target=check_user_input)
thread1.start()
thread2.start()



