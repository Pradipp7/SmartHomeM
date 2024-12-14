import time
import network
import urequests
from socket import socket, getaddrinfo
from machine import Pin
from dht import DHT11

#Wi-Fi Credentials
SSID = "NO"
PASSWORD = "nuno1234"

#Sensor & Relay Pins
dht_sensor = DHT11(Pin(1))
relay = Pin(16, Pin.OUT)

#Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected:", wlan.ifconfig())

connect_wifi()

#Send data to server
def send_data(temperature, humidity):
    url = "http://165.232.125.94/api/write-data"
    data = {"temperature": temperature, "humidity": humidity}
    try:
        res = urequests.post(url, json=data)
        print(res.text)
    except Exception as e:
        print("Error:", e)

def ping_google():
    try:
        addr = getaddrinfo('www.google.com', 80)[0][-1]
        s = socket()
        s.connect(addr)
        print("Connected to Google - Internet connection is up.")
        s.close()
    except OSError as e:
        print("Unable to connect to Google:", e)

#Main loop
while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    send_data(temp, hum)
    ping_google()
    time.sleep(5)