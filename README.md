# 💡 rekt-lights-therapy

**Real-time Bitcoin price visualizer for Philips Hue lights — turns your room green when BTC pumps and red when it dumps.**

---

## 🤡 Origin Story

This project started as a “brilliant idea” —  
a little Python script that turned all my Philips Hue lights **red** when Bitcoin started dumping.  

Big mistake 😳  
→ [See the tweet that started it all](https://x.com/RobinNakamoto/status/1976698432615231931)

Now it’s evolved into *rekt-lights-therapy* — because if you can’t stop Bitcoin from dumping,  
you might as well make it look pretty while it happens.

---

## 🚀 Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/RobinNakamoto/rekt-lights-therapy.git
   cd rekt-lights-therapy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Find your Hue Bridge IP**
   - Open the Hue app → Settings → Bridge Information  
   - Or visit [https://discovery.meethue.com](https://discovery.meethue.com)

4. **Create a Hue username**
   - Go to `http://<bridge_ip>/debug/clip.html`
   - Press the **link button** on your bridge  
   - POST this JSON to `/api`:
     ```json
     { "devicetype": "rekt_lights_therapy#script" }
     ```
   - Copy the `"username"` from the response.

5. **Edit your config**
   In `rekt_lights_therapy.py`, set:
   ```python
   HUE_BRIDGE_IP = "192.168.x.x"
   USERNAME = "YOUR_HUE_USERNAME"
   GROUP_ID = "YOUR_GROUP_ID"
   ```
   You can find your group IDs via:
   ```
   GET /api/<username>/groups
   ```

6. **Run it**
   ```bash
   python rekt_lights_therapy.py
   ```

---

## ⚙️ How it works
- Streams live BTC/USD trades from **Gemini’s WebSocket**
- Compares against Gemini’s 24-hour open price
- Changes light color if price moves ±0.9 %
- Resets reference price every day at **New York midnight**

---

## 💬 Example output
```
24h reference price: $111,250
BTC: $111,982 | Δ +0.66%

💚 Call Robin Nakamoto, tell him to start the party!
```

---

## 🧠 Ideas
- Adjust `THRESHOLD` for sensitivity  
- Add sound alerts or flashing effects  
- Extend to ETH, SOL, or multiple rooms  
- Or… connect it to your emotional support RGB keyboard  

---

## 🪪 License
MIT License © 2025 Robin Nakamoto  
See the [LICENSE](LICENSE) file for details.

---

> Inspired by Robin Nakamoto’s viral “Big mistake 😳” tweet 💡  
> https://x.com/RobinNakamoto/status/1976698432615231931
