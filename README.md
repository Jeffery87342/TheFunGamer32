# 🚀 Roblox Auto-Group Joiner

A powerful Python script that automatically joins Roblox groups at rapid speeds using your Roblox cookies, proxies, and FunBypass.com for captcha solving.

## ✨ Features

- **Rapid Group Joining**: Join groups at high speeds using multiple threads
- **Captcha Bypass**: Automatic captcha solving using FunBypass.com API
- **Proxy Support**: Use proxies to avoid rate limiting
- **Modern UI**: Clean and intuitive tkinter interface
- **Multi-Account**: Support for multiple Roblox accounts simultaneously
- **Real-time Stats**: Track joined groups, runtime, and success rate

## 📋 Requirements

- Python 3.8 or higher
- FunBypass.com API key
- Roblox account cookies (.ROBLOSECURITY)
- Proxies (recommended for high-speed joining)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jeffery87342/TheFunGamer32.git
   cd TheFunGamer32
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the script**:
   - Open `input/config.json`
   - Add your FunBypass.com API key:
     ```json
     {
         "solverKey": "YOUR_FUNBYPASS_API_KEY_HERE",
         "threads": 5
     }
     ```

4. **Add proxies** (optional but recommended):
   - Create a file named `proxies.txt` in the same folder as the scripts
   - OR use `input/proxies.txt`
   - Add your proxies (one per line) in the format:
     ```
     http://username:password@host:port
     ```
   - Example:
     ```
     http://7itfb6-country-US-session-lrj56p-time-1:ualo3fan@res-v1.nettify.xyz:8080
     http://7itfb6-country-US-session-ltyvsj-time-1:ualo3fan@res-v1.nettify.xyz:8080
     ```

## 🚀 Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

2. **In the GUI**:
   - Enter the **Group ID** of the Roblox group you want to join
   - Paste your **Roblox cookies** (.ROBLOSECURITY values, one per line)
   - (Optional) Add **proxies** in the text area
   - Click **▶ Start** to begin joining
   - Click **⬛ Stop** to stop the process

## 📝 How to Get Your Roblox Cookie

1. Log in to Roblox.com in your browser
2. Open Developer Tools (F12)
3. Go to the "Application" or "Storage" tab
4. Find "Cookies" → "https://www.roblox.com"
5. Copy the value of `.ROBLOSECURITY`

## 🔒 API Information

The script uses the official Roblox Groups API:
- **Endpoint**: `https://groups.roblox.com/v1/groups/{groupId}/users`
- **Method**: POST
- **Authentication**: Uses .ROBLOSECURITY cookie
- **Captcha Handling**: Automatic via FunBypass.com

## 📊 Output

- Joined groups are logged to `output/joined_groups.txt`
- Real-time activity log in the GUI
- Statistics including:
  - Total groups joined
  - Runtime
  - Current status

## ⚠️ Important Notes

- **Rate Limiting**: Use proxies to avoid Roblox rate limits
- **Account Safety**: Use this responsibly and at your own risk
- **FunBypass Credits**: Make sure you have sufficient credits on FunBypass.com
- **Legal**: This tool is for educational purposes only

## 🛠️ Troubleshooting

**"Rate limited" error**:
- Add more proxies to `input/proxies.txt`
- Reduce the number of threads in `config.json`

**"Failed to solve captcha"**:
- Check your FunBypass.com API key
- Ensure you have credits on your FunBypass account

**"Proxy failed to make request"**:
- Verify your proxy format is correct
- Check if your proxies are working

## 📦 Dependencies

- `curl-cffi`: For HTTP requests with browser impersonation
- `cryptography`: For authentication intent signing
- `colorama`: For colored console output
- `tkinter`: For the GUI (included with Python)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all requirements are met
3. Ensure your API key and proxies are valid

## 📄 License

This project is provided as-is for educational purposes.

---

**Made with ❤️ | Powered by FunBypass.com**
