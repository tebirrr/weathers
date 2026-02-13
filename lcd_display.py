from machine import I2C, Pin
import time

# Grove LCD I2C port 1 (Pico W)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
LCD_ADDR = 0x3e

def lcd_write(cmd, mode=0):
    i2c.writeto(LCD_ADDR, bytes([mode, cmd]))

def init():
    time.sleep_ms(50)
    lcd_write(0x38)
    lcd_write(0x39)
    lcd_write(0x14)
    lcd_write(0x70 | 0x0F)
    lcd_write(0x56)
    lcd_write(0x6C)
    time.sleep_ms(200)
    lcd_write(0x38)
    lcd_write(0x0C)
    lcd_write(0x01)
    time.sleep_ms(2)

def clear():
    lcd_write(0x01)
    time.sleep_ms(2)

def set_cursor(col, row):
    addr = col + (0x40 if row else 0x00)
    lcd_write(0x80 | addr)

def print_line(text):
    for char in text:
        lcd_write(ord(char), 0x40)
