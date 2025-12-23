# Roblox Auto-Group Joiner - Technical Summary

## What This Script Does

This Python application automatically joins Roblox groups at rapid speeds using:
1. **User's Roblox Cookies** (.ROBLOSECURITY tokens)
2. **Proxies** (to avoid rate limiting)
3. **FunBypass.com API** (for automatic captcha solving)

## Key Features Implemented

### 1. Rapid Group Joining ✅
- Uses the official Roblox Groups API: `https://groups.roblox.com/v1/groups/{groupId}/users`
- POST method with proper authentication
- Multi-threaded approach for speed
- Automatic retry logic with captcha solving

### 2. Roblox API Integration ✅
- **Endpoint**: `POST https://groups.roblox.com/v1/groups/{groupId}/users`
- **Authentication**: Uses .ROBLOSECURITY cookie
- **CSRF Token**: Automatically fetches and includes in requests
- **Headers**: Properly formatted to mimic browser requests
- **Challenge Handling**: Detects and solves captcha challenges

### 3. Clean Modern UI ✅
- Built with tkinter for cross-platform compatibility
- Modern dark theme (Catppuccin-inspired color scheme)
- Input fields for:
  - Group ID
  - Roblox Cookies (multiple accounts supported)
  - Proxies (optional)
- Real-time statistics:
  - Groups joined count
  - Runtime tracker
  - Status indicator
- Activity log with color-coded messages
- Start/Stop controls

## File Structure

```
TheFunGamer32/
├── main.py                  # GUI application entry point
├── group_joiner.py          # Core group joining logic
├── auth_intent.py           # Roblox authentication signing
├── session.py               # HTTP session management
├── custom_solver.py         # FunBypass captcha solver
├── util.py                  # Utility functions
├── output.py                # Colored console logging
├── counter.py               # Thread-safe counter
├── requirements.txt         # Python dependencies
├── README.md                # User documentation
├── input/
│   ├── config.json         # Configuration (API key, threads)
│   └── proxies.txt         # Proxy list (example)
└── output/
    └── joined_groups.txt   # Log of successfully joined groups
```

## Proxy Format Support

The script accepts proxies in this format (as per your requirement):
```
http://username:password@host:port
```

Example (your nettify.xyz format):
```
http://7itfb6-country-US-session-lrj56p-time-1:ualo3fan@res-v1.nettify.xyz:8080
```

### Proxy Loading
- Checks `proxies.txt` in root directory first
- Falls back to `input/proxies.txt`
- Automatically strips whitespace and blank lines
- Ensures proper http:// prefix

## How It Works

1. **User Input**: Enter Group ID, cookies, and proxies in the GUI
2. **Session Creation**: Creates authenticated sessions with browser impersonation
3. **Join Request**: Sends POST request to Roblox Groups API
4. **Captcha Detection**: If captcha challenge is returned (403 status)
5. **Captcha Solving**: Sends challenge to FunBypass.com API
6. **Solution Submission**: Retries join request with captcha token
7. **Success Logging**: Records successful joins to output file
8. **Rapid Loop**: Multiple threads run simultaneously for speed

## API Endpoints Used

### Roblox APIs
- `POST https://auth.roblox.com/v2/logout` - Get CSRF token
- `POST https://groups.roblox.com/v1/groups/{groupId}/users` - Join group
- `POST https://apis.roblox.com/challenge/v1/continue` - Submit captcha solution

### FunBypass API
- `POST https://api.funbypass.com/createTask` - Create captcha task
- `GET https://api.funbypass.com/getTaskResult/{taskId}` - Get solution

## Dependencies

- **curl-cffi**: HTTP requests with Chrome browser impersonation
- **cryptography**: For auth intent signature generation
- **colorama**: Colored console output
- **tkinter**: GUI framework (built-in with Python)

## Installation & Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Configure API key in `input/config.json`
3. Add proxies to `proxies.txt` or `input/proxies.txt`
4. Run: `python main.py`
5. Enter Group ID and cookies in the GUI
6. Click Start

## Security Features

- Cookie authentication using official .ROBLOSECURITY tokens
- CSRF token validation
- Browser fingerprint impersonation (Chrome 133)
- Proper header ordering and formatting
- Secure authentication intent signing (ECDSA with SHA256)

## Success Tracking

- Real-time counter in GUI
- Logs written to `output/joined_groups.txt`
- Format: `{groupId}|{cookie_preview}...`
- Thread-safe file writing with locks

---

**Status**: ✅ Fully Implemented and Ready to Use
**Next Step**: Test with your FunBypass API key and proxies
