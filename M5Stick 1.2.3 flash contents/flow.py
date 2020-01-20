import gc
import uos as os
import ubinascii
from m5stack import lcd, node_id
from utils import *
from config import __VERSION__
import machine

wait(0.5)
# Connect network
import wifisetup
wifisetup.auto_connect()

# rtc = machine.RTC()
# rtc.ntp_sync(server="cn.ntp.org.cn", tz="CET-8CEST")

# Reset apikey
if buttonA.isPressed():
    try:
        machine.nvs_erase('apikey.pem')
    except:
        pass
        
# Read apikey
apikey = machine.nvs_getstr('apikey.pem')
if apikey == None:
    apikey = ubinascii.hexlify(os.urandom(4)).decode('utf8') #Random APIKEY
    apikey = apikey.upper()
    machine.nvs_setstr('apikey.pem', apikey)

# M5Cloud
import ujson as json
from config import server_map

with open('modeconfig.json', 'r') as f:
    mode = json.loads(f.read()) 

lcd.clear()
# Display 
# lcd.clear(lcd.BLACK)
# lcd.font(lcd.FONT_DejaVu24)
# lcd.fillRect(0, 0, 320, 30, 0x5757fc)
# lcd.setTextColor(lcd.WHITE, 0x5757fc)
# lcd.print(server_map[mode['server']]['web'], 5, 5, lcd.WHITE)
# lcd.drawCircle(285, 15, 5, lcd.RED, lcd.RED)

# apikey qrcode
# lcd.font(lcd.FONT_DejaVu18)
# lcd.setTextColor(0xaaaaaa, lcd.BLACK)
# lcd.print(__VERSION__, 29, 80)
# lcd.println("APIKEY", 27, 115)
# lcd.font(lcd.FONT_DejaVu24)
# lcd.print(apikey, 12, 148, color=lcd.ORANGE)
lcd.text(__VERSION__, 8, 4)
lcd.text("apikey", 8, 16)
lcd.text(apikey[:3], 20, 26)
lcd.text(apikey[3:], 12, 34)
# lcd.print(apikey[:3], 35, 140, color=lcd.ORANGE)
# lcd.print(apikey[3:], 20, 166, color=lcd.ORANGE)
# lcd.qrcode(server_map[mode['server']]['qrcode_url'] + apikey, 126, 46, 175)

lcd.text("wait", 16, 50)
lcd.text("cloud", 12, 58)

from m5cloud import M5Cloud
mqtt_server = server_map[mode['server']]
m5cloud = M5Cloud(token=apikey, server=mqtt_server['mqtt']['server'], port=mqtt_server['mqtt']['port'])

gc.collect()
gc.threshold(gc.mem_free() // 2 + gc.mem_alloc())

m5cloud.run(thread=False)
gc.collect()
