================================================================================
                    ROBLOX AUTO-GROUP JOINER
                    Powered by FunBypass.com
================================================================================

QUICK START:
------------

1. Run start.bat (Windows) or "python main.py" (any OS)

2. Enter your details in the GUI:
   - Group ID: The Roblox group ID you want to join
   - Cookies: Your .ROBLOSECURITY cookie values (one per line)
   - Proxies: Optional, add proxies in format: ******ip:port

3. Click "Start" to begin joining groups

SETUP:
------

1. Add your FunBypass API key to: input/config.json
   {
       "solverKey": "YOUR_API_KEY_HERE",
       "threads": 5
   }

2. (Optional) Add proxies to: proxies.txt
   Format: ******ip:port
   Example: ******proxy.example.com:8080

HOW TO GET YOUR COOKIE:
-----------------------

1. Go to roblox.com and log in
2. Press F12 to open Developer Tools
3. Go to Application/Storage tab -> Cookies -> https://www.roblox.com
4. Find .ROBLOSECURITY and copy the value
5. Paste it into the script when prompted

PROXY FORMATS SUPPORTED:
------------------------

******ip:port (Recommended)
******ip:port
******ip:port
******ip:port

TROUBLESHOOTING:
----------------

- If GUI doesn't work: Run "python main_console.py" instead
- If you get errors: Run "python test.py" to diagnose issues
- Install dependencies: pip install -r requirements.txt

FILES:
------

start.bat         - Windows launcher (double-click to run)
main.py           - GUI version
main_console.py   - Console version (no GUI required)
test.py           - Test and diagnostic tool

input/config.json - Configuration (FunBypass API key)
input/proxies.txt - Proxy list (optional)
proxies.txt       - Alternative proxy location

output/joined_groups.txt - Log of successfully joined groups

================================================================================
For best results, use high-quality residential or mobile proxies
================================================================================
