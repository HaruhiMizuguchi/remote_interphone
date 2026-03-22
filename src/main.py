import network
import socket
import time
import config
from servo import Servo

# ---------- Wi-Fi 接続 ----------

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

    ip = wlan.ifconfig()[0]
    print(f"Connected! IP: {ip}")
    return wlan


# ---------- HTML ----------

HTML_PAGE = """\
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Interphone Unlocker</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0f172a; color: #e2e8f0;
    display: flex; justify-content: center; align-items: center;
    min-height: 100vh;
  }
  .card {
    background: #1e293b; border-radius: 16px; padding: 40px;
    text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,.4);
    max-width: 360px; width: 90%%;
  }
  h1 { font-size: 1.2rem; margin-bottom: 8px; }
  .status { font-size: .85rem; color: #94a3b8; margin-bottom: 32px; }
  .btn {
    display: inline-block; padding: 18px 48px;
    font-size: 1.1rem; font-weight: 600;
    color: #fff; background: #2563eb; border: none; border-radius: 12px;
    cursor: pointer; transition: background .2s;
    text-decoration: none;
  }
  .btn:active { background: #1d4ed8; }
  .msg { margin-top: 20px; font-size: .9rem; min-height: 1.4em; }
  .ok  { color: #4ade80; }
  .err { color: #f87171; }
</style>
</head>
<body>
<div class="card">
  <h1>Interphone Unlocker</h1>
  <p class="status">%s</p>
  <button class="btn" id="btn" onclick="doUnlock()">開錠</button>
  <p class="msg" id="msg"></p>
</div>
<script>
async function doUnlock(){
  const btn=document.getElementById('btn');
  const msg=document.getElementById('msg');
  btn.disabled=true; btn.textContent='動作中…';
  msg.textContent=''; msg.className='msg';
  try{
    const r=await fetch('/unlock');
    if(r.ok){msg.textContent='開錠しました'; msg.className='msg ok';}
    else{msg.textContent='エラー'; msg.className='msg err';}
  }catch(e){msg.textContent='通信失敗'; msg.className='msg err';}
  btn.disabled=false; btn.textContent='開錠';
}
</script>
</body>
</html>
"""


# ---------- HTTP サーバ ----------

def start_server(servo):
    addr = socket.getaddrinfo("0.0.0.0", config.SERVER_PORT)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(2)
    print(f"HTTP server listening on port {config.SERVER_PORT}")

    while True:
        cl, remote = s.accept()
        try:
            request = cl.recv(1024).decode()
            path = request.split(" ")[1] if " " in request else "/"
            print(f"{remote[0]} -> {path}")

            if path == "/unlock":
                servo.press_button()
                send_response(cl, 200, "application/json", '{"status":"ok"}')
            elif path == "/health":
                send_response(cl, 200, "application/json", '{"status":"healthy"}')
            else:
                ip = network.WLAN(network.STA_IF).ifconfig()[0]
                page = HTML_PAGE % f"IP: {ip}"
                send_response(cl, 200, "text/html", page)
        except Exception as e:
            print("Error:", e)
            try:
                send_response(cl, 500, "text/plain", "Internal Server Error")
            except:
                pass
        finally:
            cl.close()


def send_response(cl, status_code, content_type, body):
    reason = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}
    cl.send(f"HTTP/1.0 {status_code} {reason.get(status_code, 'Error')}\r\n")
    cl.send(f"Content-Type: {content_type}\r\n")
    cl.send("Connection: close\r\n\r\n")
    cl.send(body)


# ---------- メイン ----------

def main():
    wlan = connect_wifi()
    servo = Servo()

    ip = wlan.ifconfig()[0]
    print(f"Ready! Open http://{ip}/ on your phone")

    try:
        start_server(servo)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        servo.deinit()


main()
