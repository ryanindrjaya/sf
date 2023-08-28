import time, sys
import threading
from gtts import gTTS
from playsound import playsound
from paho.mqtt import client as mqtt_client
import json
import redis
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv('CLIENT_ID')
device_number = "001"
device = "device-001"
r = redis.Redis()
all_keys = r.keys(client_id)
topic = f"{client_id}/{device}"
print(len(all_keys))
# if len(all_keys) < 0:
    # for x in r.scan_iter("sf_config_ec_date_value*"):
try:
    get_values = r.get(client_id).decode()
    print(f"get from redis '{get_values}'")
    # data = json.loads(get_value)s

    # for x in r.scan_iter(client_id):
    #     key = x.decode()
    #     value = r.get(x).decode()
    #     print(f"{key} => {value}")
        # r.delete(key)

except Exception as error:
    default_value = json.dumps({
        "config": {
            "ec_mode": "all",
            "ec": 2.5,
            "ph_down": 5.6,
            "ph_up": 7.5,
            "fan_air_temp": 30,
            "fan_humidity": 30,
            "peristaltic_pump_duration": 60,
            "peristaltic_pump_period": 30,
            "waterflow": 0.00,
            "dap": [],
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
    r.set(topic, default_value)

broker = 'localhost'
port = 1883
# topic = "smartfarm/device-001"
# topic_sub = "smartfarm/device-001"


username = 'smartfarm'
password = 'smartfarm*2023'
deviceId = client_id
esp_dc = deviceId + "-dc"
esp_ac = deviceId + "-ac"

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

# dap_selisih = ""

delayEc = 15
delayPh = 15
pH_up = 7.6
pH_down = 5.6

temperature = 25  # water temperature
ec_value = 0.00
ph_value = 0.00
air_temperature = 0.00
humidity = 0.00
flow = 0.00
dap = datetime(2023, 2, 1, 7, 30, 00)


# def connect_mqtt():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Successfully connected to MQTT broker")
#             client.subscribe(topic, qos=1)
#         else:
#             print("Failed to connect, return code %d", rc)
#
#     client = mqtt_client.Client(client_id)
#     client.username_pw_set(username, password)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client


def publish(client, status, to, type, timer=0):
    global topic
    # global client
    # msg = f"messages: {msg_count}"
    msg = json.dumps({"action": status, "from": deviceId, "to": to, "type": type, "timer": timer})
    # print(f"{msg}")
    # msg = '{"action":"command/insert","command":{"id":432436060,"command":"LED_control","timestamp":"2021-03-24T00:19:44.418","lastUpdated":"2021-03-24T00:19:44.418","userId":37,"deviceId":"s3s9TFhT9WbDsA0CxlWeAKuZykjcmO6PoxK6","networkId":37,"deviceTypeId":5,"parameters":{"led":"on"},"lifetime":null,"status":null,"result":null},"subscriptionId":1616544981034531}'
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
        time.sleep(2)
    else:
        print(f"Failed to send message to topic {topic}")
        # publish(client, status, to, type)


# def subscribe(client: mqtt_client):
#     def on_message(client, userdata, msg):
#         try:
#             # print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
#
#             y = json.loads(str(msg.payload.decode("utf-8")))
#             _from = y["from"]
#             to = y["to"]
#             _type = y["type"]
#
#             if _from == f"{client_id}-sensor":
#                 get_value = r.get(client_id).decode()
#                 print(f"get from redis '{get_value}'")
#                 data = json.loads(get_value)
#                 data['value']['ec'] = y["ec"]
#                 data['value']['ph'] = y["ph"]
#                 r.set(client_id, json.dumps(data))
#                 print(f"new data '{json.dumps(data)}'")
#             else:
#                 if to == deviceId:
#                     action = y["action"]
#                     print(f"aksi: {action} type: {_type} dari: {to}")
#                 elif _from == deviceId:
#                     print(f"laporan diterima {_from}")
#
#         except:
#             print("An exception occurred")
#
#     # client.subscribe(topic_sub)
#     client.subscribe(topic)
#     client.on_message = on_message
#     # client.loop_start()


def on_message(client, userdata, msg):
    global ec_value
    global ph_value
    global temperature  # water temperature
    global air_temperature
    global humidity
    global flow
    global pump_1
    global pump_2
    try:
        print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")

        y = json.loads(str(msg.payload.decode("utf-8")))
        _from = y["from"]
        to = y["to"]
        _type = y["type"]

        if _from == f"{client_id}-{device_number}-sensor":
            get_value = r.get(topic).decode()
            print(f"get from redis '{get_value}'")
            data = json.loads(get_value)
            data['value']['ec'] = y["ec"]
            data['value']['ph'] = y["ph"]
            data['value']['temp_water'] = y["temp_water"]
            data['value']['temp_air'] = y["temp_air"]
            data['value']['humidity'] = y["humidity"]
            data['value']['waterflow'] = y["waterflow"]
            data['status']['pump_a'] = pump_1
            data['status']['pump_b'] = pump_2
            ec_value = y["ec"]
            ph_value = y["ph"]
            temperature = y["temp_water"]  # water temperature
            air_temperature = y["temp_air"]
            humidity = y["humidity"]
            flow = y["waterflow"]
            r.set(topic, json.dumps(data))
            print(f"new data '{json.dumps(data)}'")
        else:
            if to == deviceId:
                action = y["action"]
                print(f"aksi: {action} type: {_type} dari: {to}")
            elif _from == deviceId:
                print(f"laporan diterima {_from}")

    except:
        print("An exception occurred")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT broker")
        client.subscribe(topic, qos=1)
    else:
        print("Failed to connect, return code %d", rc)


client = mqtt_client.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
# client = connect_mqtt()
# subscribe(client)


# client.loop_start()

# tts = gTTS("Welcome to smart farm intelligent software!")
tts = gTTS(text="mulai aplikasine dap!", lang="jw")
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


def _relay_start():
    # call(['espeak "Start the Relay!" 2>/dev/null'], shell=True)
    # mixer.init()
    # mixer.music.load("start.mp3")
    # mixer.music.play()  # Wait for the audio to be played
    # time.sleep(3)
    # canvas.itemconfig(relay_ec_a_label, text="Off")
    publish(client, "off", esp_dc, "relay1")
    # canvas.itemconfig(relay_ec_b_label, text="Off")
    publish(client, "off", esp_dc, "relay2")
    # canvas.itemconfig(relay_ph_up_label, text="Off")
    publish(client, "off", esp_dc, "relay3")
    # canvas.itemconfig(relay_ph_down_label, text="Off")
    publish(client, "off", esp_dc, "relay4")
    # canvas.itemconfig(relay_pump_1_label, text="Off")
    # canvas.itemconfig(relay_pump_2_label, text="Off")
    # canvas.itemconfig(relay_fan_label, text="Off")
    publish(client, "off", esp_ac, "relay7")
    # canvas.itemconfig(relay_heater_label, text="Off")
    publish(client, "off", esp_ac, "relay8")


# def destroy():
#     # GPIO.output(Relay_channel_dc, GPIO.HIGH)
#     # GPIO.output(Relay_channel_ac, GPIO.LOW)
#     # GPIO.cleanup()


def _pumpEC():
    global pump_ec_a
    global pump_ec_b
    global ec_value
    e = threading.Event()
    interval = 1
    global stop_threads
    global r
    global client_id
    while 1:
        e.wait(interval)
        if stop_threads:
            break
        try:
            get_value = r.get(topic).decode()
            data = json.loads(get_value)
            # data['value']['ec'] = y["ec"]
            # data['value']['ph'] = y["ph"]
            # data['value']['temp_water'] = y["temp_water"]
            # data['value']['temp_air'] = y["temp_air"]
            # data['value']['humidity'] = y["humidity"]
            # data['value']['waterflow'] = y["waterflow"]
            # ec_value = y["ec"]
            # ph_value = y["ph"]
            # temperature = y["temp_water"]  # water temperature
            # air_temperature = y["temp_air"]
            # humidity = y["humidity"]
            # flow = y["waterflow"]
            # r.set(client_id, json.dumps(data))
            sf_config_ec = float(data['config']['ec'])
            if data['config']['ec_mode'] != "all":
                daps = datetime.strptime(data['config']['start_dap'], "%Y-%m-%d %H:%M:%S")
                xx = datetime.now()
                dap_selisih1 = xx - daps
                # n = 0
                try:
                    sf_config_ec = data['config']['dap'][dap_selisih1]

                except Exception as error:
                    print(error)

                # for x in data['config']['dap']:
                #     sf_config_ec
                #     n = n+1
                # x1 = r.get(f"sf_config_ec_dap_{dap_selisih1.days}").decode()
                # if x1 is not None:
                #     sf_config_ec = x1

            if ec_value < sf_config_ec:
                time.sleep(10)
                if ec_value < sf_config_ec:
                    get_value = r.get(topic).decode()
                    data = json.loads(get_value)
                    # canvas.itemconfig(relay_ec_b_label, text="Off")
                    publish(client, "on", esp_dc, "relay1", delayEc)
                    pump_ec_a = True
                    data['status']['pump_ec_a'] = True
                    r.set(client_id, json.dumps(data))
                    # publish(client, "off", esp_dc, "relay2")
                    # canvas.itemconfig(relay_ec_a_label, text="On")

                    time.sleep(delayEc)
                    get_value = r.get(topic).decode()
                    data = json.loads(get_value)
                    pump_ec_a = False
                    data['status']['pump_ec_a'] = False
                    r.set(client_id, json.dumps(data))
                    # canvas.itemconfig(relay_ec_a_label, text="Off")
                    # publish(client, "off", esp_dc, "relay1")
                    publish(client, "on", esp_dc, "relay2", delayEc)
                    get_value = r.get(topic).decode()
                    data = json.loads(get_value)
                    pump_ec_b = True
                    data['status']['pump_ec_b'] = True
                    r.set(client_id, json.dumps(data))
                    # canvas.itemconfig(relay_ec_b_label, text="On")
                    time.sleep(delayEc)
                    get_value = r.get(topic).decode()
                    data = json.loads(get_value)
                    pump_ec_b = False
                    data['status']['pump_ec_b'] = False
                    r.set(client_id, json.dumps(data))
                    # publish(client, "off", esp_dc, "relay2")
                    # canvas.itemconfig(relay_ec_b_label, text="Off")
                time.sleep(5)

        except Exception as error:
            print(error)


def _pumpPHUp():
    global pH_down
    global ph_value
    global pump_ph_up
    e = threading.Event()
    interval = 1
    global stop_threads
    global r
    global client_id
    while 1:
        e.wait(interval)
        if stop_threads:
            break
        get_value = r.get(topic).decode()
        data = json.loads(get_value)
        pH_down = float(data['config']['ph_down'])
        if ph_value < pH_down:
            val = 0
            for x in range(9):
                if ph_value < pH_down:
                    val = val + 1
                time.sleep(1)

            if val > 5:
                publish(client, "on", esp_dc, "relay3", delayPh)
                # publish(client, "off", esp_dc, "relay2")
                # canvas.itemconfig(relay_ph_up_label, text="On")
                pump_ph_up = True
                get_value = r.get(topic).decode()
                data = json.loads(get_value)
                data['status']['pump_ph_up'] = True
                r.set(topic, json.dumps(data))
                time.sleep(delayPh)
                pump_ph_up = False
                get_value = r.get(topic).decode()
                data = json.loads(get_value)
                data['status']['pump_ph_up'] = False
                r.set(topic, json.dumps(data))
                # canvas.itemconfig(relay_ph_up_label, text="Off")
            time.sleep(5)


def _pumpPHDown():
    global pH_up
    global pH_down
    global ph_value
    global pump_ph_down
    global r
    e = threading.Event()
    interval = 1
    global stop_threads
    while 1:
        e.wait(interval)
        if stop_threads:
            break
        get_value = r.get(topic).decode()
        data = json.loads(get_value)
        pH_up = float(data['config']['ph_up'])
        if ph_value > pH_up:
            val = 0
            for x in range(9):
                if ph_value > pH_up:
                    val = val + 1
                time.sleep(1)

            if val > 5:
                publish(client, "on", esp_dc, "relay4", delayPh)
                # publish(client, "off", esp_dc, "relay2")
                # canvas.itemconfig(relay_ph_down_label, text="On")
                pump_ph_down = True
                get_value = r.get(topic).decode()
                data = json.loads(get_value)
                data['status']['pump_ph_down'] = True
                r.set(topic, json.dumps(data))
                time.sleep(delayPh)
                pump_ph_down = False
                get_value = r.get(topic).decode()
                data = json.loads(get_value)
                data['status']['pump_ph_down'] = False
                r.set(topic, json.dumps(data))
                # canvas.itemconfig(relay_ph_down_label, text="Off")
            time.sleep(5)


fan = False
high_temp = 30
delayFan = 30


def _pumpFan():
    global air_temperature
    global fan
    global high_temp
    e = threading.Event()
    interval = 1
    global stop_threads
    global pump_1
    global pump_2
    while 1:
        e.wait(interval)
        if stop_threads:
            break
        get_value = r.get(topic).decode()
        data = json.loads(get_value)
        high_temp = float(data['config']['fan_air_temp'])
        if air_temperature > high_temp:
            val = 0
            for x in range(9):
                if air_temperature > high_temp:
                    val = val + 1
                time.sleep(1)

            if val > 5:
                publish(client, "on", esp_ac, "relay7", delayFan)
                fan = True
                get_value = r.get(topic).decode()
                data = json.loads(get_value)
                data['status']['fan'] = True
                r.set(topic, json.dumps(data))
                time.sleep(delayFan)
                fan = False
                get_value = r.get(topic).decode()
                data = json.loads(get_value)
                data['status']['fan'] = False
                r.set(topic, json.dumps(data))
                # canvas.itemconfig(relay_ph_down_label, text="Off")
            time.sleep(5)


def _pumpBalance():
    global flow
    global pump_1
    global pump_2
    e = threading.Event()
    interval = 1
    global stop_threads
    global client_id
    global r
    while 1:
        e.wait(interval)
        if stop_threads:
            break
        print(f"-------------------- A'{pump_1}' B '{pump_2}'")
        if pump_1:
            publish(client, "off", esp_ac, "relay6")
            publish(client, "on", esp_ac, "relay5")
            # canvas.itemconfig(relay_pump_1_label, text="On")
            # canvas.itemconfig(relay_pump_2_label, text="Off")
        elif pump_2:
            publish(client, "off", esp_ac, "relay5")
            publish(client, "on", esp_ac, "relay6")
            # canvas.itemconfig(relay_pump_2_label, text="On")
            # canvas.itemconfig(relay_pump_1_label, text="Off")
        while 1:
            if flow == 0:
                if pump_1:
                    publish(client, "off", esp_ac, "relay5")
                    publish(client, "on", esp_ac, "relay6")
                    # canvas.itemconfig(relay_pump_2_label, text="On")
                    # canvas.itemconfig(relay_pump_1_label, text="Off")
                    pump_1 = False
                    pump_2 = True
                    get_value = r.get(topic).decode()
                    data = json.loads(get_value)
                    data['status']['pump_a'] = False
                    data['status']['pump_b'] = True
                    r.set(topic, json.dumps(data))
                elif pump_2:
                    publish(client, "off", esp_ac, "relay6")
                    publish(client, "on", esp_ac, "relay5")
                    # canvas.itemconfig(relay_pump_1_label, text="On")
                    # canvas.itemconfig(relay_pump_2_label, text="Off")
                    pump_2 = False
                    pump_1 = True
                    get_value = r.get(topic).decode()
                    data = json.loads(get_value)
                    data['status']['pump_a'] = True
                    data['status']['pump_b'] = False
                    r.set(topic, json.dumps(data))
                time.sleep(15)


def _show_datetime():
    # e = threading.Event()
    # interval = 1
    while 1:
        # e.wait(interval)
        x = datetime.now()

        date_now = x.strftime("%d") + " - " + x.strftime("%b") + " - " + x.strftime("%Y")
        # canvas.itemconfig(date_now_label, text=str('%s' % date_now))

        time_now = x.strftime("%X")
        # canvas.itemconfig(time_now_label, text=str('%s' % time_now))
        global stop_threads
        if stop_threads:
            break


# make threading
stop_threads = False
time.sleep(5)


def start_all():
    # playsound('welcome.mp3')

    threading.Thread(target=_show_datetime).start()
    threading.Thread(target=_relay_start).start()
    threading.Thread(target=_pumpEC).start()
    threading.Thread(target=_pumpPHUp).start()
    threading.Thread(target=_pumpPHDown).start()
    threading.Thread(target=_pumpBalance).start()
    client.loop_forever(30, 1, True)


def destroy_all():
    global stop_threads
    stop_threads = True
    playsound('exit.mp3')
    time.sleep(2)
    client.loop_stop()
    # os.system('sudo reboot')
    sys.exit()


start_all()



# if __name__ == '__main__':
#     start_all()
