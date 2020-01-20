# This file is executed on every boot (including wake-boot from deepsleep)
import sys
import gc

# Set default path
# Needed for importing modules and upip
sys.path.append('/flash/lib')
sys.path.append('/flash/sys_lib')

# timer: init timer 0 as EXTBASE, m5cloud used 6, button use 7, speak use 8, mqtt use 9
# free: 1, 2, 3, 4, 5, 10, 11 -> need application: tof, ir
# pwm timer: analogWrite, lcd pwm use timer 1, speak use timer 2 , Serveo use timer3
from machine import Timer
tex = Timer(0)
tex.init(mode = tex.EXTBASE)

# boot view
import uos as os
import utime as time
from m5stack import *
from config import __VERSION__

lcd.show_flow(10, 40)
lcd.text(__VERSION__, 8, 5)

import ujson as json
with open('modeconfig.json', 'r') as f:
    config = json.loads(f.read())

# wait 1000 for user choose
cnt_down = time.ticks_ms() + 1000
while time.ticks_ms() < cnt_down:
    if buttonA.isPressed():
        speaker.tone(2000, 50, timer=False) # Beep        
        press_time = time.ticks_ms()
        time.sleep_ms(10)

        while buttonA.isPressed():
            time.sleep_ms(10)

        if time.ticks_ms() - press_time > 300:
            import wificonfig
            wificonfig.webserver_start()
            break

        if(config['start']) == 'app':
            core_start('flow')
        else:
            core_start('app')
        break      

#     elif buttonB.isPressed(): # APP list
#         speaker.tone(2000, 50, volume=1, timer=False) # Beep
#         from app_manage import file_choose
#         file_choose()
#         core_start('app')
#         break      

#     elif buttonC.isPressed(): # WiFi setting
#         speaker.tone(2000, 50, volume=1, timer=False) # Beep
#         import wifichoose
#         wifichoose.start()
#         break

import ujson as json
with open('modeconfig.json', 'r') as f:
    config = json.loads(f.read())

# # 0 -> run main.py
# # 1 -> run flow.py
# # 2 -> run debug.py
import m5base
if config['start'] == 'app':
    m5base.app_start(0)
elif config['start'] == 'flow':
    if config['mode'] == 'usb':
        m5base.app_start(3)
    else:
        m5base.app_start(1)
elif config['start'] == 'debug':
    m5base.app_start(2)

m5button.clear()

# config = None
# cnt_down = None
# gc.collect() 
# del config
# del cnt_down
