# M5Cloud config file
__VERSION__ = 'V1.2.3'

config_online = {
    "type": "M5CORE",
    "web": "Flow.m5stack.com",
    "qrcode_url":'http://flow.m5stack.com/?k=',
    "port": "80",
    "ntp_server": "hr.pool.ntp.org",
    "time_zone": "UTC-8",
    "mqtt": {
        "server": "mqtt.m5stack.com",
        "port": 1883
    },
    "version": "0.50"
}

config_offline = {
    "type": "M5CORE",
    "web": "13.67.90.180",
    "qrcode_url":'192.168.1.119/?k=',
    "port": "80",
    "ntp_server": "hr.pool.ntp.org",
    "time_zone": "UTC-8",
    "mqtt": {
        "server": "13.67.90.180",
        "port": 1883
    },
    "version": "0.50"
}

config_offline2 = {
    "type": "M5CORE",
    "web": "192.168.0.106",
    "qrcode_url":'192.168.0.215/?k=',
    "port": "80",
    "ntp_server": "hr.pool.ntp.org",
    "time_zone": "UTC-8",
    "mqtt": {
        "server": "192.168.0.106",
        "port": 1883
    },
    "version": "0.50"
} 

config_pi = {
    "type": "M5CORE",
    "web": "10.0.0.1",
    "qrcode_url":'10.0.0.1/?k=',
    "port": "5000",
    "ntp_server": "hr.pool.ntp.org",
    "time_zone": "UTC-8",
    "mqtt": {
        "server": "10.0.0.1",
        "port": 1883
    },
    "version": "0.50"
} 

# server_map = {'Flow.m5stack.com': config_online, '192.168.1.119': config_offline}
server_inside = {'bin': config_offline2}
server_map = { 'Flow.m5stack.com': config_online }