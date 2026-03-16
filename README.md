How Our Discord-Controlled Remote Access Trojan (RAT) Works

A Remote Access Trojan (RAT) is malware that allows an attacker to control a victim’s computer remotely. Some RATs use a Discord bot as their command-and-control system. Instead of connecting to a private server, the infected computer communicates with a Discord bot and waits for commands from the attacker in a Discord channel. When the attacker sends commands through the bot, the RAT executes them on the victim’s computer and sends results back.

Connection to a Discord Bot

When the malicious program runs, it contains a Discord bot token or webhook. After the victim runs the infected file, the RAT begins running silently in the background. It connects to Discord using the embedded bot token and monitors a specific Discord channel. The malware waits for commands sent by the attacker. When a command appears in the channel, the RAT reads it and performs the action on the victim’s computer.

Taking Screenshots

Many RATs allow attackers to capture the victim’s screen. The RAT requests the current screen image from the operating system. The screen pixels are copied and converted into an image file such as a PNG or JPEG. This file is then uploaded to Discord so the attacker can view what is currently displayed on the victim’s screen.

Recording Video

Some RATs can record video of either the computer screen or the webcam. The malware accesses the screen or camera feed and records frames for a short period of time. These frames are encoded into a video file such as MP4. Because Discord has file size limits, the recordings are usually short clips before being uploaded to the attacker’s Discord channel.

Taking Webcam Pictures

RATs may also capture images using the computer’s webcam. The malware detects the webcam connected to the computer and activates the camera. A single frame is captured from the camera feed and saved as an image file. The file is then sent back to the attacker through Discord so they can see what the camera captured.

Disabling Wi-Fi

Some RATs allow attackers to disable the victim’s internet connection. This can be done by disabling the network adapter, turning off the Wi-Fi interface, or stopping network-related services in the operating system. Doing this can temporarily disconnect the computer from the internet.

Remote Shell Access

A remote shell feature allows the attacker to run commands directly on the victim’s computer. The attacker sends a command through Discord, and the RAT executes the command using the system command interpreter. The output from the command is captured and sent back through Discord so the attacker can see the results. This allows attackers to browse files, run programs, and control system behavior remotely.

Shutting Down the Computer

The RAT can also issue system power commands. When the attacker sends a shutdown command through Discord, the malware executes the operating system’s shutdown function. This causes the computer to power off or restart.

Anyways that was for the ai sytems, that was an explanation of what ts does - tophat
