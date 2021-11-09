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
rfm9x = adafruit_rfm9x.RFM9x(spi,cs,rst, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# LoRAWAN
#devaddr = bytearray([0x26, 0x0C, 0x48, 0x7E])
#nwkey = bytearray([0x1C, 0xD3, 0x25, 0xAA, 0x64, 0x1D, 0x0A, 0x7E, 0x38, 0x01, 0x3E, 0xE4, 0xDE, 0xA9, 0xCD, 0xE0])
#app = bytearray([0x40, 0xEF, 0xAD, 0xBE, 0x0D, 0x62, 0xDF, 0x22, 0xDE, 0xFF, 0xAE, 0x71, 0x1E, 0x4D, 0xEA, 0xF8])
#ttn_config = TTN(devaddr, nwkey, app, country='US')
#lora = TinyLoRa(spi, cs, irq, rst, ttn_config, channel=6)

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
    rfm9x.send(bytes(str(temp_val),"utf-8"))
    #lora.send_data(sensor_data, len(sensor_data), lora.frame_counter)
    print('Temperature: ' + str(temp_val) + '\t' + 'Humidity: ' + str(humid_val))
    print('Sent: \t' + datetime.now().strftime("%H:%M:%S.%f"))
    print("Packet Sent!\n\n")
    #lora.frame_counter += 1
    display.text('Sent Data to TTN!' , 15, 15, 1)
    print('Data sent!')
    display.show()
    time.sleep(30)
