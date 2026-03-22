# Remote Interphone Unlocker

マンションのインターホンの物理的な開錠ボタンを、スマホから遠隔で押せるようにするプロジェクト。

## 方式

物理ボタンをサーボモータで直接押す方式を採用。

| 項目 | 選定 |
|------|------|
| マイコン | Raspberry Pi Pico WH |
| アクチュエータ | サーボモータ |
| 通信 | Wi-Fi（Pico WH 内蔵） |
| 電源 | 5V ACアダプタ（Picoとサーボに並列給電） |

## 選定理由

- 物理ボタンなので回路解析が不要
- サーボを既に所持
- Pico WH を購入済み
- インターホンの分解を最小限にできる

## ドキュメント構成

| ファイル | 内容 |
|----------|------|
| [docs/architecture.md](docs/architecture.md) | システム全体構成 |
| [docs/power-design.md](docs/power-design.md) | 電源設計 |
| [docs/wiring.md](docs/wiring.md) | 物理配線 |
| [docs/communication.md](docs/communication.md) | 通信方式 |
| [docs/implementation-plan.md](docs/implementation-plan.md) | 実装ロードマップ |
| [docs/parts-list.md](docs/parts-list.md) | 部品リスト |
