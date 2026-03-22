# ===== Wi-Fi 設定 =====
WIFI_SSID = "YOUR_SSID"
WIFI_PASSWORD = "YOUR_PASSWORD"

# ===== サーボ設定 =====
SERVO_GPIO_PIN = 0

# SG90 系サーボの一般的なPWMパラメータ
SERVO_FREQ_HZ = 50          # 50Hz（周期 20ms）
SERVO_MIN_US = 500           # 0° に対応するパルス幅 (µs)
SERVO_MAX_US = 2400          # 180° に対応するパルス幅 (µs)

# ===== 開錠動作の角度設定 =====
# 実機で調整すること
ANGLE_REST = 0               # 待機位置（ボタンから離れた角度）
ANGLE_PRESS = 90             # 押下位置（ボタンを押す角度）
PRESS_DURATION_MS = 600      # ボタンを押し続ける時間 (ms)

# ===== MQTT 設定 =====
# --- テスト用: 公開ブローカー（認証なし）---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_USE_SSL = False
MQTT_WS_PORT = 8000          # controller.html 用（WebSocket）
MQTT_WS_SCHEME = "ws"

# --- 本番用: HiveMQ Cloud（TLS + 認証）---
# MQTT_BROKER = "xxxxxxxx.s1.eu.hivemq.cloud"
# MQTT_PORT = 8883
# MQTT_USER = "your-username"
# MQTT_PASSWORD = "your-password"
# MQTT_USE_SSL = True
# MQTT_WS_PORT = 8884
# MQTT_WS_SCHEME = "wss"

MQTT_CLIENT_ID = "pico_interphone"
MQTT_TOPIC_CMD = "interphone/cmd"
MQTT_TOPIC_STATUS = "interphone/status"

# 共有シークレット（スマホ側と一致させること）
MQTT_SECRET = "CHANGE_ME_TO_RANDOM_STRING"
