import time, sys
import threading
import datetime
# from w1thermsensor import W1ThermSensor
from pyA20.gpio import gpio
from pyA20.gpio import port
import OPi.GPIO as GPIO
import dht22
from gui_layout import *
from gtts import gTTS
from playsound import playsound
from paho.mqtt import client as mqtt_client
import json

broker = 'localhost'
port_mqtt = 1883
topic = "smartfarm/device-001"
topic_sub = "smartfarm/device-001"
client_id = 'smartfarm-001'
username = 'smartfarm'
password = 'smartfarm*2023'
deviceId = client_id
esp_dc = deviceId + "-dc"
esp_ac = deviceId + "-ac"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port_mqtt)
    return client


def publish(client, status, to, type):
    # global client
    # msg = f"messages: {msg_count}"
    msg = "{\"action\":\"" + status + "\",\"from\":\"" + deviceId + "\",\"to\":\"" + to + "\",\"type\":\"" + type + "\"}}}"
    # msg = '{"action":"command/insert","command":{"id":432436060,"command":"LED_control","timestamp":"2021-03-24T00:19:44.418","lastUpdated":"2021-03-24T00:19:44.418","userId":37,"deviceId":"s3s9TFhT9WbDsA0CxlWeAKuZykjcmO6PoxK6","networkId":37,"deviceTypeId":5,"parameters":{"led":"on"},"lifetime":null,"status":null,"result":null},"subscriptionId":1616544981034531}'
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        try:
            print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
            y = json.loads(msg.payload.decode())
            # From = y["from"]
            to = y["to"]
            # item = y["item"]
            # action = y["action"]
            if to == deviceId:
                print(f"{to}")


        except:
            print("An exception occurred")

    client.subscribe(topic_sub)
    client.on_message = on_message


# tts = gTTS("Welcome to smart farm intelligent software!")
tts = gTTS(text="mulai aplikasine dap!", lang="jw")
# tts = gTTS(text="Sugeng rawuh ing aplikasi smart farm!", lang="jw")
tts.save('welcome.mp3')

tts = gTTS("Start the application!")
tts.save('start.mp3')

tts = gTTS("Exit the application!")
tts.save('exit.mp3')

# import Adafruit_ADS1x15
sys.path.insert(0, 'libs/DFRobot_ADS1115/python/raspberrypi/')
sys.path.insert(0, 'libs/GreenPonik_EC_Python/src/')
sys.path.insert(0, 'libs/GreenPonik_PH_Python/src/')

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16

from DFRobot_ADS1115 import ADS1115
from GreenPonik_EC import GreenPonik_EC
from GreenPonik_PH import GreenPonik_PH

# sensor = W1ThermSensor()
PIN2 = port.PA6
gpio.init()
dhtDevice = dht22.DHT22(pin=PIN2)

# ADS1015 = 0x00
# ADS1115 = 0x01
ads1115 = ADS1115()
ec = GreenPonik_EC()
ph = GreenPonik_PH()

ec.begin()
ph.begin()

# water flow sensor
FLOW_SENSOR_GPIO = 27  # 13
# MQTT_SERVER = "192.168.1.220"


# global count
count = 0
start_counter = 1


def countPulse(channel):
    global count
    if start_counter == 1:
        if GPIO.input(channel):
            count = count + 1


# RELAY
Relay_channel_dc = [6, 13, 19, 26, 12, 16, 20, 21]


def setup():
    global tts
    GPIO.setboard(GPIO.PCPCPLUS)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.BOTH, callback=lambda x: countPulse(27))
    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Relay_channel_dc, GPIO.OUT, initial=GPIO.HIGH)
    # GPIO.setup(Relay_channel_ac, GPIO.OUT, initial=GPIO.LOW)
    canvas.itemconfig(relay_ec_a_label, text="Off")
    canvas.itemconfig(relay_ec_b_label, text="Off")
    canvas.itemconfig(relay_ph_up_label, text="Off")
    canvas.itemconfig(relay_ph_down_label, text="Off")
    canvas.itemconfig(relay_pump_1_label, text="Off")
    canvas.itemconfig(relay_pump_2_label, text="Off")
    canvas.itemconfig(relay_fan_label, text="Off")
    canvas.itemconfig(relay_heater_label, text="Off")

    # global tts
    # for i in range(0, len(Relay_channel_dc)):
    #     num = i + 1
    #     voice = ""
    #     if num == 1:
    #         voice = "A Nutrition pump"
    #     elif num == 2:
    #         voice = "B Nutrition pump"
    #     elif num == 3:
    #         voice = "PH Up pump"
    #     elif num == 4:
    #         voice = "PH Down pump"
    #     elif num == 5:
    #         voice = "Water pump 1"
    #     elif num == 6:
    #         voice = "Water pump 2"
    #     elif num == 7:
    #         voice = "Fan"
    #     elif num == 8:
    #         voice = "Heater"
    #     tts = gTTS(voice + " switch on!")
    #     tts.save('relay' + str(i + 1) + 'on.mp3')
    #     tts = gTTS(voice + " switch off!")
    #     tts.save('relay' + str(i + 1) + 'off.mp3')
    for i in range(0, len(Relay_channel_dc)):
        num = i + 1
        voice = ""
        if num == 1:
            voice = "pompa nutrisi A"
        elif num == 2:
            voice = "pompa nutrisi B"
        elif num == 3:
            voice = "pompa PH atas"
        elif num == 4:
            voice = "pompa PH bawah"
        elif num == 5:
            voice = "pompa air 1"
        elif num == 6:
            voice = "pompa air 2"
        elif num == 7:
            voice = "kipas angin"
        elif num == 8:
            voice = "pemanas"
        tts = gTTS(text=voice + " hidup!", lang="su", slow=False)
        # (text="mulai aplikasine dap!", lang="jw")
        tts.save('relay' + str(i + 1) + 'on.mp3')
        tts = gTTS(text=voice + " mati!", lang="su", slow=False)
        tts.save('relay' + str(i + 1) + 'off.mp3')


def _relay_start():
    # call(['espeak "Start the Relay!" 2>/dev/null'], shell=True)
    # mixer.init()
    # mixer.music.load("start.mp3")
    # mixer.music.play()  # Wait for the audio to be played
    # time.sleep(3)

    while True:
        try:
            for i in range(0, len(Relay_channel_dc)):
                print('...Relay channel %d on' % (i + 1))
                num = i + 1
                GPIO.output(Relay_channel_dc[i], GPIO.LOW)
                if num == 1:
                    publish(client, "on", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ec_a_label, text="On")
                elif num == 2:
                    publish(client, "on", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ec_b_label, text="On")
                elif num == 3:
                    publish(client, "on", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ph_up_label, text="On")
                elif num == 4:
                    publish(client, "on", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ph_down_label, text="On")
                elif num == 5:
                    publish(client, "on", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_pump_1_label, text="On")
                elif num == 6:
                    publish(client, "on", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_pump_2_label, text="On")
                elif num == 7:
                    publish(client, "on", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_fan_label, text="On")
                elif num == 8:
                    publish(client, "on", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_heater_label, text="On")

                playsound('relay' + str(i + 1) + 'on.mp3')
                # GPIO.output(Relay_channel_ac[i], GPIO.HIGH)
                if num == 1:
                    time.sleep(10)
                else:
                    time.sleep(5)
                print('...Relay channel %d off' % (i + 1))
                GPIO.output(Relay_channel_dc[i], GPIO.HIGH)
                if num == 1:
                    publish(client, "off", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ec_a_label, text="Off")
                elif num == 2:
                    publish(client, "off", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ec_b_label, text="Off")
                elif num == 3:
                    publish(client, "off", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ph_up_label, text="Off")
                elif num == 4:
                    publish(client, "off", esp_dc, "relay" + str(num))
                    canvas.itemconfig(relay_ph_down_label, text="Off")
                elif num == 5:
                    publish(client, "off", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_pump_1_label, text="Off")
                elif num == 6:
                    publish(client, "off", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_pump_2_label, text="Off")
                elif num == 7:
                    publish(client, "off", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_fan_label, text="Off")
                elif num == 8:
                    publish(client, "off", esp_ac, "relay" + str(num))
                    canvas.itemconfig(relay_heater_label, text="Off")
                playsound('relay' + str(i + 1) + 'off.mp3')
                # GPIO.output(Relay_channel_ac[i], GPIO.LOW)
                time.sleep(2)
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            destroy()
            sys.exit()


def destroy():
    GPIO.output(Relay_channel_dc, GPIO.HIGH)
    # GPIO.output(Relay_channel_ac, GPIO.LOW)
    GPIO.cleanup()


setup()
# Play the audio

# if __name__ == '__main__':
#     setup()
#     try:
#         main()
#     except KeyboardInterrupt:
#         destroy()

# temperature = 25
# ads1115.setGain(0)
temperature = 25
# pH 4.0
_acidVoltage = 3058.0
# pH 7.0
_neutralVoltage = 2628.0

_kvalue = 1.0
_kvalueLow = 1.0
_kvalueHigh = 1.0

_ecCalibrationValue = 193


def readPH(voltage):
    global _acidVoltage
    global _neutralVoltage
    slope = (7.0 - 4.0) / ((_neutralVoltage - 1500.0) /
                           3.0 - (_acidVoltage - 1500.0) / 3.0)
    intercept = 7.0 - slope * (_neutralVoltage - 1500.0) / 3.0
    _phValue = slope * (voltage - 1500.0) / 3.0 + intercept
    return round(_phValue, 2)


def readEC(voltage, temperature):
    global _kvalueLow
    global _kvalueHigh
    global _kvalue
    global _ecCalibrationValue
    rawEC = _ecCalibrationValue * voltage / 820.0 / 200.0
    # print(">>>current rawEC is: %.3f" % rawEC)
    # valueTemp = rawEC * _kvalue
    # if(valueTemp > 2.5):
    #     _kvalue = _kvalueHigh
    # elif(valueTemp < 2.0):
    #     _kvalue = _kvalueLow
    value = rawEC * _kvalue
    value = value / (1.0 + 0.0185 * (temperature - 25.0))
    return value


def read_ph_ec():
    global ads1115
    global ec
    global ph
    global temperature
    # or make your own temperature read process

    # Set the IIC address
    ads1115.set_addr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.read_voltage(0)
    adc1 = ads1115.read_voltage(1)
    # Convert voltage to EC with temperature compensation
    EC = readEC(adc0['r'], temperature)
    PH = readPH(adc1['r'])
    canvas.itemconfig(ph_label, text=str('%.2f' % PH))
    canvas.itemconfig(ec_label, text=str('%.2f' % EC))

    print("Voltase:%.1f ^C EC:%.2f ms/cm PH:%.2f " % (temperature, adc0['r'], adc1['r']))
    print("Temperature:%.1f ^C EC:%.2f ms/cm PH:%.2f " % (temperature, EC, PH))
    return temperature, EC, PH


def readEcCalibration(voltage, temperature):
    global _kvalueLow
    global _kvalueHigh
    global _kvalue
    global _ecCalibrationValue
    rawEC = _ecCalibrationValue * (voltage / 820.0 / 200.0)

    x = 2.76 / (voltage / 820.0 / 200.0)
    _ecCalibrationValue = x
    print(">>>current calibrate val is: %.3f" % x)
    print(">>>current rawEC is: %.3f" % rawEC)
    # valueTemp = rawEC * _kvalue
    # if(valueTemp > 2.5):
    #     _kvalue = _kvalueHigh
    # elif(valueTemp < 2.0):
    #     _kvalue = _kvalueLow
    value = rawEC * _kvalue

    value = value / (1.0 + 0.0185 * (temperature - 25.0))
    print(">>>current Val is: %.3f" % value)
    return value


def ec_calibrate():
    global ads1115
    global ec
    temperature = 25  # or make your own temperature read method
    # Set the IIC address
    ads1115.set_addr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.read_voltage(0)

    ec.calibration(adc0['r'], temperature)
    read_calibration = readEcCalibration(adc0['r'], temperature)

    return read_calibration


# ec_calibrate()


def ph_calibration():
    global ads1115
    global ph
    # Set the IIC address
    ads1115.set_addr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    # Get the Digital Value of Analog of selected channel
    adc1 = ads1115.read_voltage(1)
    print("calibration voltage: %.3f" % adc1['r'])
    return ph.calibration(adc1['r'])


# ph_calibration()
dap = datetime.datetime(2023, 2, 1, 7, 30, 00)


def my_mainloop():
    # call(['espeak "EC and PH sensor installed!" 2>/dev/null'], shell=True)
    e = threading.Event()
    interval = 1
    while 1:
        e.wait(interval)
        read_ph_ec()
        global stop_threads
        if stop_threads:
            break

    # time.sleep(1)
    # window.after(1000, my_mainloop)  # run again after 1000ms (1s)


def _show_temp():
    # call(['espeak "Water temperature sensor installed!" 2>/dev/null'], shell=True)
    global temperature
    e = threading.Event()
    interval = 1
    while 1:
        e.wait(interval)
        global stop_threads
        if stop_threads:
            sys.exit()
        try:
            temperature = sensor.get_temperature()
            print("The temperature is %s celsius" % temperature)
            canvas.itemconfig(temp_label, text=str('%.2f' % temperature) + " °C")
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(5.0)
            continue
        except Exception as error:
            # dhtDevice.exit()
            _show_temp()
            raise error


def _show_dap():
    e = threading.Event()
    interval = 1
    while 1:
        e.wait(interval)
        x = datetime.datetime.now()
        dap_selisih = x - dap
        canvas.itemconfig(dap_selisih_label, text=str('%s' % dap_selisih.days))
        canvas.itemconfig(time_dap_label, text=str('%s' % str(datetime.timedelta(seconds=dap_selisih.seconds))))
        global stop_threads
        if stop_threads:
            break


def _show_dht():
    # call(['espeak "Humidity and Air Temperature sensor installed!" 2>/dev/null'], shell=True)
    e = threading.Event()
    interval = 1
    global stop_threads
    while 1:
        e.wait(interval)
        if stop_threads:
            sys.exit()
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.read().temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.read().humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )
            if str('%.2f' % humidity) == "25.50" and str('%.2f' % temperature_c) == "25.50":
                print(
                    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                        temperature_f, temperature_c, humidity
                    )
                )

            else:
                canvas.itemconfig(hum_label, text=str('%.2f' % humidity) + "  %")
                canvas.itemconfig(air_temp_label, text=str('%.2f' % temperature_c) + " °C")

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error


def _show_wtf():
    # call(['espeak "Waterflow sensor installed!" 2>/dev/null'], shell=True)
    global count
    global start_counter
    e = threading.Event()
    interval = 5
    while 1:
        e.wait(interval)
        try:
            start_counter = 1
            time.sleep(1)
            start_counter = 0
            flow = (count / 7.5)  # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
            print("The flow is: %.3f Liter/min" % flow)
            canvas.itemconfig(wtf_label, text=str('%.2f' % flow))

            # publish.single("/Garden.Pi/WaterFlow", flow, hostname=MQTT_SERVER)
            count = 0
            # time.sleep(5)
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            GPIO.cleanup()
            sys.exit()
        global stop_threads
        if stop_threads:
            GPIO.cleanup()
            break


def _show_datetime():
    # e = threading.Event()
    # interval = 1
    while 1:
        # e.wait(interval)
        x = datetime.datetime.now()

        date_now = x.strftime("%d") + " - " + x.strftime("%b") + " - " + x.strftime("%Y")
        canvas.itemconfig(date_now_label, text=str('%s' % date_now))

        time_now = x.strftime("%X")
        canvas.itemconfig(time_now_label, text=str('%s' % time_now))
        global stop_threads
        if stop_threads:
            break


# make threading
stop_threads = False

client = ""


def start_all():
    global client
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()

    playsound('welcome.mp3')

    threading.Thread(target=_show_datetime).start()

    threading.Thread(target=_show_dap).start()
    threading.Thread(target=_show_dht).start()

    # threading.Thread(target=_show_temp).start()

    threading.Thread(target=_show_wtf).start()

    threading.Thread(target=my_mainloop).start()

    threading.Thread(target=_relay_start).start()


def destroy_all():
    global stop_threads

    stop_threads = True
    # mixer.init()
    # mixer.music.load("exit.mp3")
    # mixer.music.play()  # Wait for the audio to be played
    playsound('exit.mp3')
    time.sleep(2)
    # call(['espeak "Application destroy!" 2>/dev/null'], shell=True)
    # eng.stop()
    destroy()
    window.destroy()


window.after(1000, start_all)

window.attributes('-fullscreen', True)
window.bind("<Escape>", lambda event: destroy_all())

window.mainloop()
