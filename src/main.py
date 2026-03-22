import network
import time
import machine
from umqtt.simple import MQTTClient
import config
from servo import Servo

led = machine.Pin("LED", machine.Pin.OUT)


# ---------- Wi-Fi ----------

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return wlan

    print(f"Connecting to {config.WIFI_SSID} ...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    for _ in range(20):
        if wlan.isconnected():
            break
        time.sleep(1)

    if not wlan.isconnected():
        raise RuntimeError("Wi-Fi connection failed")

    print(f"Connected! IP: {wlan.ifconfig()[0]}")
    return wlan


# ---------- MQTT ----------

servo = None


def on_message(topic, msg):
    payload = msg.decode().strip()
    print(f"MQTT recv: {topic} -> {payload}")

    if payload == config.MQTT_SECRET:
        print("Secret OK -> pressing button")
        led_blink(3, 100)
        servo.press_button()
        publish_status(b"unlocked")
    else:
        print("Secret mismatch, ignoring")
        publish_status(b"rejected")


_mqtt_client = None


def publish_status(msg):
    try:
        if _mqtt_client:
            _mqtt_client.publish(config.MQTT_TOPIC_STATUS, msg)
    except:
        pass


def connect_mqtt():
    global _mqtt_client

    client = MQTTClient(
        config.MQTT_CLIENT_ID,
        config.MQTT_BROKER,
        port=config.MQTT_PORT,
        user=config.MQTT_USER or None,
        password=config.MQTT_PASSWORD or None,
        ssl=config.MQTT_USE_SSL,
        ssl_params={"server_hostname": config.MQTT_BROKER},
    )
    client.set_callback(on_message)
    client.connect()
    client.subscribe(config.MQTT_TOPIC_CMD)
    _mqtt_client = client

    print(f"MQTT connected to {config.MQTT_BROKER}")
    print(f"Subscribed to: {config.MQTT_TOPIC_CMD}")
    return client


# ---------- LED ----------

def led_blink(times, interval_ms):
    for _ in range(times):
        led.on()
        time.sleep_ms(interval_ms)
        led.off()
        time.sleep_ms(interval_ms)


# ---------- メイン ----------

def main():
    global servo

    connect_wifi()
    servo = Servo()

    led.on()
    print("Waiting for MQTT unlock commands...")
    print(f"Topic: {config.MQTT_TOPIC_CMD}")

    while True:
        try:
            client = connect_mqtt()
            publish_status(b"online")
            led_blink(2, 200)
            led.on()

            while True:
                client.check_msg()
                time.sleep_ms(100)

        except KeyboardInterrupt:
            print("Shutting down...")
            break
        except Exception as e:
            print(f"MQTT error: {e}, reconnecting in 5s...")
            led.off()
            time.sleep(5)

    publish_status(b"offline")
    servo.deinit()
    led.off()


main()
