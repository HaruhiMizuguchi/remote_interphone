# 実装ロードマップ

## 第1段階: ハードウェア基盤

**目標:** Pico WH とサーボを安定して動かす

- [ ] 5V 並列給電の配線
- [ ] GND 共通化の確認
- [ ] GPIO から PWM でサーボ制御
- [ ] ボタンを押せる角度の調整
- [ ] サーボの物理固定（両面テープ・ステー等）

**完了条件:** サーボがインターホンの開錠ボタンを確実に押せる

---

## 第2段階: ローカル操作（HTTP）

**目標:** 家の Wi-Fi 内からスマホで操作

- [x] Pico WH に簡易 HTTP サーバを実装
- [x] `/unlock` エンドポイントでサーボ動作
- [x] スマホのブラウザからアクセスして動作確認

**ソースコード:**
| ファイル | 役割 |
|----------|------|
| `src/config.py` | Wi-Fi・サーボ・サーバの定数 |
| `src/servo.py` | サーボ制御クラス |
| `src/test_server.py` | ローカル HTTP テスト |

**完了条件:** 同一ネットワーク内のスマホから開錠できる ✅

---

## 第3段階: リモート操作（MQTT）

**目標:** 外出先からモバイルデータ経由で開錠できる

- [x] 通信方式の決定 → MQTT 採用
- [x] MQTT 版 `main.py` 実装
- [x] スマホ操作ページ `web/controller.html` 作成
- [x] シークレット照合によるセキュリティ
- [ ] `umqtt.simple` のインストール（`install_deps.py`）
- [ ] テスト用公開ブローカーで通信確認（`test_mqtt.py`）
- [ ] 本番ブローカー（HiveMQ Cloud）への移行

**ソースコード:**
| ファイル | 役割 |
|----------|------|
| `src/config.py` | Wi-Fi・MQTT・サーボの定数 |
| `src/servo.py` | サーボ制御クラス |
| `src/main.py` | Wi-Fi + MQTT メインループ |
| `src/install_deps.py` | umqtt インストール用 |
| `src/test_mqtt.py` | サーボ無し MQTT テスト |
| `web/controller.html` | スマホ操作ページ（MQTT over WebSocket） |

**完了条件:** 外出先のスマホから開錠操作ができる

---

## 第4段階: LINE 連携（将来）

**目標:** LINE で「開けて」と送ると開錠できる

- [ ] LINE Bot 作成
- [ ] Webhook → MQTT publish の中継
