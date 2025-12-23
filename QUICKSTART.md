# 🚀 Quick Start Guide

## Fastest Way to Get Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your API Key
Edit `input/config.json` and add your FunBypass API key:
```json
{
    "solverKey": "YOUR_API_KEY_HERE",
    "threads": 5
}
```

### 3. Add Proxies (Recommended)
Create `proxies.txt` and add your proxies:
```
******res-v1.nettify.xyz:8080
******res-v1.nettify.xyz:8080
```

### 4. Run the Script

**With GUI (if tkinter is available):**
```bash
python main.py
```

**Without GUI (console mode):**
```bash
python main_console.py
```

### 5. Enter Your Details
- **Group ID**: The Roblox group ID you want to join
- **Cookies**: Your .ROBLOSECURITY cookie value(s)
- **Proxies**: (Optional) Can also be entered in the GUI

---

## How to Get Your Cookie

1. Go to [roblox.com](https://www.roblox.com) and log in
2. Press `F12` to open Developer Tools
3. Go to the **Application** or **Storage** tab
4. Click **Cookies** → **https://www.roblox.com**
5. Find `.ROBLOSECURITY` and copy the value
6. Paste it into the script when prompted

---

## Testing

Run the test script to verify everything is set up correctly:
```bash
python test.py
```

This will check:
- ✓ All modules load correctly
- ✓ Dependencies are installed
- ✓ Configuration files exist
- ✓ Proxy files are set up

---

## Common Issues

### "tkinter not found"
→ Use console version: `python main_console.py`

### "curl_cffi not found"
→ No problem! The script will use regular requests library as fallback

### "No proxies found"
→ Add proxies to `proxies.txt` for better performance (optional)

---

## Need Help?

Check the full [README.md](README.md) for detailed documentation and troubleshooting.
