import json
import requests
import threading
import time
import websocket
import random
import datetime
import pytz

# ---- CONFIG ----
# Replace with your local Hue Bridge details
HUE_BRIDGE_IP = "192.168.x.x"      # e.g. 192.168.1.10
USERNAME = "YOUR_HUE_USERNAME"     # generated via /debug/clip.html
GROUP_ID = "YOUR_GROUP_ID"         # e.g. "100" for Office group

# ---- SETTINGS ----
THRESHOLD = 0.01  # 1% price change
GREEN_HEX = "#00ff33"
RED_HEX = "#ff0000"

PUMP_PHRASES = [
    "🚀 It's going up forever, Laura",
    "💚 Call Robin Nakamoto, tell him to start the party!",
    "🐂 Going up, going up",
    "🟢 We call them poor",
    "💸 I'll be buying at the top forever"
]

DUMP_PHRASES = [
    "💀 Bitcoin is on Sale!",
    "📉 BUY THE DIP!",
    "🔻 Deploying more capital — steady lads.",
    "😬 WAGMI",
    "🔥 Don't get REKT, HODL"
]

# ---- HELPERS ----
def hex_to_xy(hex_color):
    """Convert hex color to XY for Hue lights."""
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

    # Gamma correction
    r = ((r + 0.055) / (1.0 + 0.055)) ** 2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / (1.0 + 0.055)) ** 2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / (1.0 + 0.055)) ** 2.4 if b > 0.04045 else b / 12.92

    X = r * 0.664511 + g * 0.154324 + b * 0.162028
    Y = r * 0.283881 + g * 0.668433 + b * 0.047685
    Z = r * 0.000088 + g * 0.072310 + b * 0.986039
    if (X + Y + Z) == 0:
        return [0, 0]
    return [X / (X + Y + Z), Y / (X + Y + Z)]

def set_group_color(hex_color):
    """Send new color to Hue group (room)."""
    xy = hex_to_xy(hex_color)
    url = f"http://{HUE_BRIDGE_IP}/api/{USERNAME}/groups/{GROUP_ID}/action"
    try:
        requests.put(url, json={"on": True, "bri": 254, "xy": xy}, timeout=2)
    except Exception as e:
        print(f"[Hue Error] {e}")

def get_open_price():
    """Fetch 24h open price from Gemini."""
    url = "https://api.gemini.com/v2/ticker/btcusd"
    data = requests.get(url, timeout=5).json()
    return float(data["open"])

def seconds_until_midnight_ny():
    """Seconds until next midnight in New York (Gemini reset)."""
    tz = pytz.timezone("America/New_York")
    now = datetime.datetime.now(tz)
    tomorrow = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return (tomorrow - now).total_seconds()

# ---- MAIN ----
reference_price = get_open_price()
print(f"24h reference price: ${reference_price:,.0f}")

current_state = "neutral"

def on_message(ws, message):
    global reference_price, current_state
    data = json.loads(message)
    if "events" not in data:
        return
    for event in data["events"]:
        if event["type"] == "trade":
            price = float(event["price"])
            change = (price - reference_price) / reference_price

            print(f"BTC: ${price:,.0f} | Δ {change*100:.2f}% ", end="\r")

            if change >= THRESHOLD and current_state != "pump":
                print("\n" + random.choice(PUMP_PHRASES))
                set_group_color(GREEN_HEX)
                current_state = "pump"

            elif change <= -THRESHOLD and current_state != "dump":
                print("\n" + random.choice(DUMP_PHRASES))
                set_group_color(RED_HEX)
                current_state = "dump"

def keep_reference_fresh():
    """Refresh reference price exactly at NY midnight."""
    global reference_price
    while True:
        sleep_time = seconds_until_midnight_ny()
        print(f"\nNext reference reset in {sleep_time/3600:.2f} hours (NY midnight)")
        time.sleep(sleep_time)
        reference_price = get_open_price()
        print(f"\n📅 New trading day! Reference reset → ${reference_price:,.0f}")

# ---- THREADS + WS ----
threading.Thread(target=keep_reference_fresh, daemon=True).start()

ws = websocket.WebSocketApp(
    "wss://api.gemini.com/v1/marketdata/btcusd",
    on_message=on_message
)
ws.run_forever()
