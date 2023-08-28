from tkinter import *
import os

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

window = Tk()
window.title("SMART FARM SYSTEM Dashboard")
window.geometry("800x480")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=480,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    16.0,
    11.0,
    anchor="nw",
    text="SMART\nFARM",
    fill="#13445F",
    font=("Montserrat Black", 20 * -1)
)

canvas.create_rectangle(
    16.0,
    69.0,
    230.0,
    465.0,
    fill="#F6C2C2",
    outline="")

canvas.create_rectangle(
    247.0,
    214.0,
    417.0,
    465.0,
    fill="#FCE0FF",
    outline="")

canvas.create_rectangle(
    430.0,
    214.0,
    600.0,
    465.0,
    fill="#E9E996",
    outline="")

canvas.create_rectangle(
    613.0,
    214.0,
    783.0,
    465.0,
    fill="#C1C1FF",
    outline="")

canvas.create_rectangle(
    247.0,
    69.0,
    783.0,
    200.0,
    fill="#F1D6D6",
    outline="")

canvas.create_text(
    41.0,
    79.0,
    anchor="nw",
    text="Temperature",
    fill="#13445F",
    font=("Helvetica", 16 * -1, "bold")
)

canvas.create_text(
    274.0,
    94.0,
    anchor="nw",
    text="Controller 1",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)

canvas.create_text(
    274.0,
    154.0,
    anchor="nw",
    text="Available",
    fill="#13445F",
    font=("Helvetica", 12 * -1)
)

canvas.create_text(
    274.0,
    224.0,
    anchor="nw",
    text="EC",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)

canvas.create_text(
    454.0,
    224.0,
    anchor="nw",
    text="pH",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)

canvas.create_text(
    638.0,
    226.0,
    anchor="nw",
    text="Waterflow",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)

air_temp_label = canvas.create_text(
    41.0,
    197.0,
    anchor="nw",
    text="28.5 ºC",
    fill="#13445F",
    font=("Helvetica", 32 * -1)
)

ec_label = canvas.create_text(
    274.0,
    248.0,
    anchor="nw",
    text="0.01",
    fill="#13445F",
    font=("Helvetica", 32 * -1)
)

relay_ec_a_label = canvas.create_text(
    274.0,
    338.0,
    anchor="nw",
    text="On",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

relay_ph_up_label = canvas.create_text(
    457.0,
    338.0,
    anchor="nw",
    text="On",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

relay_pump_1_label = canvas.create_text(
    638.0,
    340.0,
    anchor="nw",
    text="On",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

relay_fan_label = canvas.create_text(
    41.0,
    408.0,
    anchor="nw",
    text="On",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

relay_heater_label = canvas.create_text(
    117.0,
    408.0,
    anchor="nw",
    text="Off",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

relay_ph_down_label = canvas.create_text(
    457.0,
    406.0,
    anchor="nw",
    text="Off",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

relay_ec_b_label = canvas.create_text(
    274.0,
    406.0,
    anchor="nw",
    text="On",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)
relay_pump_2_label = canvas.create_text(
    638.0,
    408.0,
    anchor="nw",
    text="Off",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

ph_label = canvas.create_text(
    454.0,
    248.0,
    anchor="nw",
    text="6.20",
    fill="#13445F",
    font=("Helvetica", 32 * -1)
)

dap_selisih_label = canvas.create_text(
    638.0,
    119.0,
    anchor="nw",
    text="65 ",
    fill="#13445F",
    font=("Helvetica", 24 * -1)
)

wtf_label = canvas.create_text(
    638.0,
    250.0,
    anchor="nw",
    text="0.00",
    fill="#13445F",
    font=("Helvetica", 32 * -1)
)

temp_label = canvas.create_text(
    45.0,
    124.0,
    anchor="nw",
    text="24 ºC",
    fill="#13445F",
    font=("Helvetica", 32 * -1)
)

canvas.create_text(
    43.0,
    181.0,
    anchor="nw",
    text="Air",
    fill="#13445F",
    font=("Helvetica", 14 * -1)
)

canvas.create_text(
    41.0,
    379.0,
    anchor="nw",
    text="Fan",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    117.0,
    379.0,
    anchor="nw",
    text="Heater",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    457.0,
    313.0,
    anchor="nw",
    text="pH Up",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    44.0,
    108.0,
    anchor="nw",
    text="Water",
    fill="#13445F",
    font=("Helvetica", 14 * -1)
)

canvas.create_text(
    457.0,
    380.0,
    anchor="nw",
    text="pH Down",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    274.0,
    313.0,
    anchor="nw",
    text="A Nutrition",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    638.0,
    315.0,
    anchor="nw",
    text="Pump 1",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    274.0,
    380.0,
    anchor="nw",
    text="B Nutrition",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    638.0,
    382.0,
    anchor="nw",
    text="Pump 2",
    fill="#13445F",
    font=("Helvetica", 15 * -1)
)

canvas.create_text(
    274.0,
    122.0,
    anchor="nw",
    text="Status",
    fill="#13445F",
    font=("Helvetica", 12 * -1)
)

date_now_label = canvas.create_text(
    454.0,
    123.0,
    anchor="nw",
    text="09 - Feb - 2023",
    fill="#13445F",
    font=("Montserrat Bold", 12 * -1)
)

time_now_label = canvas.create_text(
    454.0,
    154.0,
    anchor="nw",
    text="20:32",
    fill="#13445F",
    font=("Montserrat Bold", 12 * -1)
)

time_dap_label = canvas.create_text(
    638.0,
    154.0,
    anchor="nw",
    text="20:32:54",
    fill="#13445F",
    font=("Montserrat Bold", 12 * -1)
)

hum_label = canvas.create_text(
    41.0,
    299.0,
    anchor="nw",
    text="50%",
    fill="#13445F",
    font=("Helvetica", 32 * -1)
)

canvas.create_text(
    41.0,
    268.0,
    anchor="nw",
    text="Humidity",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)
#
# button_image_1 = PhotoImage(
#     file=relative_to_assets("button_1.png"))
# button_1 = Button(
#     image=button_image_1,
#     borderwidth=0,
#     highlightthickness=0,
#     command=lambda: print("button_1 clicked"),
#     relief="flat"
# )
# button_1.place(
#     x=736.0,
#     y=20.0,
#     width=33.888916015625,
#     height=30.182281494140625
# )

canvas.create_text(
    454.0,
    93.0,
    anchor="nw",
    text="DateTime",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)

canvas.create_text(
    638.0,
    93.0,
    anchor="nw",
    text="DAP",
    fill="#13445F",
    font=("Helvetica", 16 * -1)
)
# window.resizable(False, False)

#
