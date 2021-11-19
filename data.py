import random
import time
from adafruit_bme280 import basic as adafruit_bme280
import board

def get_data():
    # Create sensor object, using the board's default I2C bus.
    i2c = board.I2C()   # uses board.SCL and board.SDA
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    # change this to match the location's pressure (hPa) at sea level
    bme280.sea_level_pressure = 1013.25

    sensor_data = bytearray(7)   

    temp_val = bme280.temperature
    humid_val = bme280.relative_humidity
    press_val = bme280.pressure

    sensor_data[0] = 1
    # Temperature data
    sensor_data[1] = (temp_val >> 8) & 0xff
    sensor_data[2] = temp_val & 0xff
    # Humidity data
    sensor_data[3] = (humid_val >> 8) & 0xff
    sensor_data[4] = humid_val & 0xff
    # Pressure data
    sensor_data[5] = (press_val >> 8) & 0xff
    sensor_data[6] = press_val & 0xff
    
    return sensor_data