import random
import webview
import time, sys
import threading
from gui_layout import *
from gtts import gTTS
# from playsound import playsound
import json
import redis
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import qrcode

load_dotenv()

client_id = os.getenv('CLIENT_ID')
device = "device-001"
deviceId = client_id
topic = f"{client_id}/{device}"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(device)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save('html/images/qr_client.png')

r = redis.Redis()
default_value = json.dumps({
    "config": {
        "ec_mode": "all",
        "ec": 2.5,
        "ph_down": 5.6,
        "ph_up": 7.5,

        "fan_air_temp_min": 30.0,
        "fan_air_temp_max": 100.0,

        "fan_humidity": 100.0,

        "peristaltic_pump_duration": 60,
        "peristaltic_pump_period": 30,
        "waterflow": 0.00,
        "dap": [0.00, 0.00],
        "start_dap": datetime.now().strftime("%Y-%m-%d 00:00:00")
    },
    "value": {
        "ec": 0.00,
        "ph": 0.00,
        "waterflow": 0.00,
        "temp_air": 0.00,
        "temp_water": 0.00,
        "humidity": 0.00,
    },
    "status": {
        "pump_ec_a": False,
        "pump_ec_b": False,
        "pump_ph_up": False,
        "pump_ph_down": False,
        "pump_a": False,
        "pump_b": False,
        "fan": False,
        "heater": False,
    },

})
# r.set(topic, default_value)

all_keys = r.keys('*')
# print(all_keys)
if len(all_keys) > 0:
    for x in r.scan_iter(f"{client_id}*"):
        print(x)
print(len(all_keys))

pump_1 = True
pump_2 = False

pump_ec_a = False
pump_ec_b = False

pump_ph_up = False
pump_ph_down = False

# pH 4.0
_acidVoltage = 3058.0
# pH 7.0
_neutralVoltage = 2628.0

_kvalue = 1.0
_kvalueLow = 1.0
_kvalueHigh = 1.0

_ecCalibrationValue = 193
print(len(all_keys))

# dap_selisih = ""

delayEc = 15
delayPh = 15
pH_up = 7.5
pH_down = 5.6

temperature = 25  # water temperature
ec_value = 0.00
ph_value = 0.00
air_temperature_down = 60.00
air_temperature_up = 100.00

humidity = 100.00

flow = 0.00

# tts = gTTS("Welcome to smart farm intelligent software!")
tts = gTTS(text="sugeng rawuh!", lang="jw")
# tts = gTTS(text="Sugeng rawuh ing aplikasi smart farm!", lang="jw")
tts.save('welcome.mp3')

tts = gTTS("Start the application!")
tts.save('start.mp3')

tts = gTTS("Exit the application!")
tts.save('exit.mp3')
sensor = ""
# global count
count = 0
start_counter = 1

dap = datetime(2023, 2, 1, 7, 30, 00)

fan = False
high_temp = 30
delayFan = 30


# def _show_datetime():
#     # e = threading.Event()
#     # interval = 1
#     while 1:
#         # e.wait(interval)
#         x = datetime.now()
#
#         date_now = x.strftime("%d") + " - " + x.strftime("%b") + " - " + x.strftime("%Y")
#         # canvas.itemconfig(date_now_label, text=str('%s' % date_now))
#
#         time_now = x.strftime("%X")
#         # canvas.itemconfig(time_now_label, text=str('%s' % time_now))
#         global stop_threads
#         if stop_threads:
#             break
#
#
# # make threading
# stop_threads = False
# time.sleep(5)
#
# def start_all():
#     # playsound('welcome.mp3')
#     threading.Thread(target=_show_datetime).start()


def destroy_all():
    global stop_threads
    stop_threads = True
    # playsound('exit.mp3')
    time.sleep(2)
    window.destroy()
    # os.system('sudo reboot')
    sys.exit()


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def getInitial(self):
        global r
        # red = redis.Redis()
        get_value = r.get(client_id).decode()
        data = json.loads(get_value)
        # high_temp = float(data['config']['fan_air_temp'])
        sf_config_ec = data['config']['ec']
        sf_config_ec_mode = data['config']['ec_mode']
        sf_config_ec_dap = data['config']['dap']
        sf_config_ph_down = data['config']['ph_down']
        sf_config_ph_up = data['config']['ph_up']
        sf_config_air_temp_down = data['config']['fan_air_temp_min']
        sf_config_air_temp_up = data['config']['fan_air_temp_max']

        sf_config_humidity = data['config']['fan_humidity']

        # for x1 in r.scan_iter("sf_config_ec_dap*"):
        #     key1 = x1.decode()
        #     value1 = r.get(x1).decode()
        #     print(f"{key1} => {value1}")
        #     sf_config_ec_dap.append({key1: value1})
        response = {
            "sf_config_ec": sf_config_ec,
            "sf_config_ec_mode": sf_config_ec_mode,
            "sf_config_ec_dap": sf_config_ec_dap,
            "sf_config_ph_up": sf_config_ph_up,
            "sf_config_ph_down": sf_config_ph_down,
            "sf_config_fan_air_temp_min": sf_config_air_temp_down,
            "sf_config_fan_air_temp_max": sf_config_air_temp_up,

            "sf_config_fan_humidity": sf_config_humidity

        }
        return response


    def getCurrentValue(self):
        global temperature
        global ec_value
        global ph_value
        global air_temperature
        global humidity
        global flow
        global pump_ec_a
        global pump_ec_b
        global pump_ph_down
        global pump_ph_up
        global pump_1
        global pump_2
        global fan
        global r
        global dap
        resArray = []
        resList = []
        for res in r.scan_iter(f"{client_id}*"):
            resList.append(res)
        resList.sort()
        for res in resList:
            print(res)
            try:
                get_value = r.get(res).decode()
                # print(f"get from redis '{get_value}'")
                data = json.loads(get_value)

                dap = datetime.strptime(data['config']['start_dap'], "%Y-%m-%d %H:%M:%S")
                xx = datetime.now()
                dap_selisih = xx - dap
                sf_config_ph_down = data['config']['ph_down']
                sf_config_ph_up = data['config']['ph_up']
                sf_config_ec = data['config']['ec']
                sf_config_air_temp_down = data['config']['fan_air_temp_min']
                sf_config_air_temp_up = data['config']['fan_air_temp_max']

                sf_config_humidity = data['config']['fan_humidity']

                ec_value = data['value']['ec']
                ph_value = data['value']['ph']
                air_temperature = data['value']['temp_air']
                temperature = data['value']['temp_water']
                humidity = data['value']['humidity']
                if data['config']['ec_mode'] != "all":
                    sf_config_ec = data['config']['dap']

                date_now = xx.strftime("%d") + "  " + xx.strftime("%b") + "  " + xx.strftime("%Y")
                time_now = xx.strftime("%H:%M:%S")

                humidity = data['value']['humidity']
                if data['value']['humidity'] == "NaN":
                    humidity = 0

                temp_air = data['value']['temp_air']
                if data['value']['temp_air'] == "NaN":
                    temp_air = 0

                response = {
                    "ec_mode": data['config']['ec_mode'],
                    "dap": data['config']['dap'],
                    "sf_config_ec": sf_config_ec,
                    "sf_config_ph_up": sf_config_ph_up,
                    "sf_config_ph_down": sf_config_ph_down,
                    "water_temperature": data['value']['temp_water'],
                    "air_temperature": temp_air,
                    "humidity": humidity,
                    "flow": data['value']['waterflow'],
                    "ec": data['value']['ec'],
                    "ph": data['value']['ph'],
                    "dap_days": dap_selisih.days,
                    "dap_time": str(timedelta(seconds=dap_selisih.seconds)),
                    "date_now": date_now,
                    "time_now": str(time_now),
                    "pump_ec_a": data['status']['pump_ec_a'],
                    "pump_ec_b": data['status']['pump_ec_b'],
                    "pump_ph_down": data['status']['pump_ph_down'],
                    "pump_ph_up": data['status']['pump_ph_up'],
                    "pump_1": data['status']['pump_a'],
                    "pump_2": data['status']['pump_b'],
                    "fan": data['status']['fan'],
                    "heater": data['status']['heater'],

                    "sf_config_fan_air_temp_min": sf_config_air_temp_down,
                    "sf_config_fan_air_temp_max": sf_config_air_temp_up,

                    "sf_config_fan_humidity": sf_config_humidity

                }

                print(f"response : '{response}'")
                resArray.append(response)

                # return response

            except Exception as error:
                print(error)
        return resArray

    def setRedisValue(self, key, value,client):
        global r
        global client_id
        try:

            client_ids = f"{client_id}{client}"
            print(f"set val {client_ids} '{key}' '{value}'")
            get_value = r.get(client_ids).decode()

            # print(f"get from redis '{get_value}'")
            data = json.loads(get_value)

            if key == "ec":

                data['config'][key] = value
                data['config']['ec_mode'] = "all"

            elif key == "start_dap":
                #value = tuple(value)
                #print(value)
                year, month, day = map(int, value.split('-'))
                data['config']['start_dap'] = datetime(year, month, day).strftime("%Y-%m-%d 00:00:00")

            elif key == "dap":
                data['config']['dap'] = value
                data['config']['ec_mode'] = "single"
            else:
                data['config'][key] = value

            r.set(client_ids, json.dumps(data))
            get_value = r.get(client_ids).decode()
            print(f"get from redis '{get_value}'")
            response = {
                key: value,
                "message": f"{key} Value has been set to {value}"
            }
            return response
        except Exception as error:
            print(error)


    def doHeavyStuff(self):
        time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': 'Operation cancelled'}
                break
        else:
            then = time.time()
            response = {
                'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now),
                                                                                     threading.current_thread())
            }
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True

    def sayHelloTo(self, name):
        response = {
            'message': 'Hello {0}!'.format(name)
        }
        return response

    def error(self):
        raise Exception('This is a Python exception')


startLink = "html/dashboard.html"

if __name__ == '__main__':
    api = Api()
    # start_all()
    window = webview.create_window('Smartfarm', startLink, fullscreen=True, js_api=api)
    webview.start()
