"""
umqtt ライブラリをインストールするスクリプト。
Wi-Fi 接続済みの状態で Thonny から1回だけ実行する。
"""

import network
import time
import config

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print(f"Connecting to {config.WIFI_SSID} ...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    for _ in range(20):
        if wlan.isconnected():
            break
        time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError("Wi-Fi connection failed - cannot install packages")

print("Wi-Fi connected:", wlan.ifconfig()[0])
print("Installing umqtt.simple ...")

import mip
mip.install("umqtt.simple")

print("Done! You can now run main.py or test_mqtt.py")
