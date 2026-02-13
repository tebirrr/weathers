import network
import urequests
import time
import json
from lcd_display import init, clear, set_cursor, print_line

IP_API = "http://ip-api.com/json"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Load config
with open("config.json") as f:
    config = json.load(f)

SSID = config["wifi_ssid"]
PASSWORD = config["wifi_password"]
API_KEY = config["api_key"]

# LCD init
init()
clear()
print_line("Connecting WiFi")

# WiFi connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

timeout = 15
while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1

if not wlan.isconnected():
    clear()
    print_line("WiFi Error")
    raise SystemExit

clear()
print_line("WiFi OK")
time.sleep(2)

# Get location
try:
    r = urequests.get(IP_API)
    loc = r.json()
    r.close()
    lat = loc["lat"]
    lon = loc["lon"]
except:
    clear()
    print_line("IP Error")
    raise SystemExit

clear()
print_line("Lat:")
set_cursor(0,1)
print_line(str(lat)[:16])
time.sleep(3)

# Main loop
while True:

    # Reconnect if needed
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        time.sleep(5)

    try:
        url = f"{WEATHER_URL}?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        r = urequests.get(url)
        data = r.json()
        r.close()

        if data["cod"] != 200:
            raise Exception("API error")

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]

        clear()
        print_line(f"T:{temp}C H:{humidity}%")
        set_cursor(0,1)
        print_line(desc[:16])

    except:
        clear()
        print_line("API Error")

    time.sleep(600)  # 10 minut
