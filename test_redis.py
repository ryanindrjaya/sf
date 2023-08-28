from time import strptime

import redis
from datetime import datetime

r = redis.Redis()
all_keys = r.keys('*')
print(len(all_keys))
if len(all_keys) < 0:
    # for x in r.scan_iter("sf_config_ec_date_value*"):
    for x in r.scan_iter("sf_config*"):
        key = x.decode()
        value = r.get(x).decode()
        print(f"{key} => {value}")
        # r.delete(key)
else:
    # r.set("sf_config_dap", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    r.set("sf_config_dap", datetime.now().strftime("%Y-%m-%d 00:00:00"))
    r.set("sf_config_ec", 2.5)
    r.set("sf_config_ph_down", 5.6)
    r.set("sf_config_ph_up", 7.5)
    r.set("sf_config_fan_air_temp", 30)
    r.set("sf_config_fan_humidity", 50)
    r.set("sf_config_peristaltic_pump_duration", 60)  # seconds
    r.set("sf_config_peristaltic_pump_period", 30)  # minutes
    r.set("sf_config_waterflow", 0)
    r.set("sf_config_ec_date_2023-03-07", 2.4)
    r.set("sf_config_ec_date_2023-03-08", 2.3)
    r.set("sf_config_ec_date_2023-03-09", 2.2)

c = r.get("sf_config_dap")
if c is not None:
    dap = datetime.strptime(c.decode(), "%Y-%m-%d %H:%M:%S")
    x = datetime.now()
    print(x)
    print(dap)
    dap_selisih = x - dap
    print(dap_selisih.days)
else:
    print("tidak ditemukan")
