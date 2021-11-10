# Author: Colby Sawyer
# Based on the Adafruit documentation for creating a LoRA node (https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/usage)

import time
from datetime import datetime
import busio
import random
from digitalio import DigitalInOut
import board
import digitalio
import adafruit_ssd1306
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
# Import the RFM9x radio module.
import adafruit_rfm9x

FEATHER_ID = 1

i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.CE1)
irq = DigitalInOut(board.D22)
rst = DigitalInOut(board.D25)

# Lora
#rfm9x = adafruit_rfm9x.RFM9x(spi,cs,rst, 925.0)
#rfm9x.tx_power = 23
#prev_packet = None

# LoRAWAN
devaddr = bytearray([0x26, 0x0C, 0xEF, 0xC6])
nwkey = bytearray([0x2C, 0xDD, 0xFF, 0xCB, 0x6C, 0x30, 0x05, 0xC2, 0x57, 0xBB, 0xBD, 0x08, 0x98, 0x38, 0xEC, 0x32])
app = bytearray([0x7B, 0xFF, 0x4D, 0xB7, 0x7E, 0x7C, 0x8A, 0xAA, 0xD0, 0xFC, 0x96, 0x73, 0xCF, 0xD5, 0xA7, 0xE4])
ttn_config = TTN(devaddr, nwkey, app, country='US')
#lora = TinyLoRa(spi, cs, irq, rst, ttn_config, channel=6)
lora = TinyLoRa(spi=spi, cs=cs, irq=irq, rst=rst, ttn_config=ttn_config, channel=3)


sensor_data = bytearray(7)

while True:
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRaWAN', 35, 0, 1)

    temp_val = 75 + random.randint(0,25)
    humid_val = 1000 - random.randint(0,250)

    sensor_data[0] = FEATHER_ID
    # Temperature data
    sensor_data[1] = (temp_val >> 8) & 0xff
    sensor_data[2] = temp_val & 0xff
    # Humidity data
    sensor_data[3] = (humid_val >> 8) & 0xff
    sensor_data[4] = humid_val & 0xff

    print('Sending packet .....')
    #rfm9x.send(bytes(str(temp_val),"utf-8"))
    lora.send_data(sensor_data, len(sensor_data), lora.frame_counter)
    print('Temperature: ' + str(temp_val) + '\t' + 'Humidity: ' + str(humid_val))
    print('Sent: \t' + datetime.now().strftime("%H:%M:%S.%f"))
    print("Packet Sent!\n\n")
    lora.frame_counter += 1
    display.text('Sent Data to TTN!' , 15, 15, 1)
    print('Data sent!')
    display.show()
    time.sleep(30)
