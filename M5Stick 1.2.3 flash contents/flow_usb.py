from m5stack import *
import m5ucloud

lcd.clear()

# Reset apikey
if buttonB.isPressed():
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
lcd.clear(lcd.BLACK)
lcd.font(lcd.FONT_DejaVu24)
lcd.fillRect(0, 0, 320, 30, 0x5757fc)
lcd.setTextColor(lcd.WHITE, 0x5757fc)
lcd.print("USB Mode", 5, 5, lcd.WHITE)

# apikey qrcode
lcd.font(lcd.FONT_DejaVu18)
lcd.setTextColor(0xaaaaaa, lcd.BLACK)
lcd.print(__VERSION__, 29, 80)
lcd.println("APIKEY", 27, 115)
lcd.font(lcd.FONT_DejaVu24)
# lcd.print(apikey, 12, 148, color=lcd.ORANGE)
lcd.print(apikey[:3], 35, 140, color=lcd.ORANGE)
lcd.print(apikey[3:], 20, 166, color=lcd.ORANGE)
lcd.qrcode("https://m5stack.com/", 126, 46, 175)

cloud = m5ucloud.M5UCloud()
cloud.run()