#!/bin/bash
set -e

echo "🧰 Qtile + Polybar Dracula Config Builder"
echo "⚙️  This script will install all configs locally and work alongside XFCE."

# Install packages (Arch-based)
sudo pacman -S --needed --noconfirm \
  qtile polybar rofi picom starship variety \
  thunar neofetch betterlockscreen archlinux-logout sddm \
  nerd-fonts terminus-font ttf-jetbrains-mono

echo "📂 Creating config directories..."
mkdir -p ~/.config/qtile ~/.config/polybar/scripts ~/.config/rofi ~/.config/picom ~/.config/variety ~/Pictures/Wallpapers

echo "📝 Writing config files..."

# Qtile config.py
cat << EOF > ~/.config/qtile/config.py
from libqtile import layout, hook
from libqtile.config import Key, Group, Screen
from libqtile.lazy import lazy
import os, subprocess

mod = "mod4"
keys = [
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod], "p", lazy.spawn("~/.config/rofi/power-menu.sh")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
]
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])
layouts = [layout.MonadTall(), layout.Max()]
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["~/.config/polybar/launch.sh"])
EOF

# Polybar
cat << EOF > ~/.config/polybar/config.ini
[bar/qtilebar]
width = 100%
height = 28
background = #282a36
foreground = #f8f8f2
font-0 = "JetBrainsMono Nerd Font:size=10"
modules-left = qtile workspaces
modules-right = cpu memory pulseaudio tray clock

[module/qtile]
type = custom/script
exec = ~/.config/polybar/scripts/qtile-windows.py
interval = 2

[module/workspaces]
type = internal/xworkspaces
label-active = %name%
label-active-foreground = #bd93f9

[module/clock]
type = internal/date
format = %Y-%m-%d %I:%M %p

[module/cpu]
type = custom/script
exec = ~/.config/polybar/scripts/cpu.sh
interval = 2

[module/memory]
type = custom/script
exec = ~/.config/polybar/scripts/mem.sh
interval = 2

[module/pulseaudio]
type = internal/pulseaudio
format-volume =  %volume%%
format-muted =  muted

[module/tray]
type = internal/tray
EOF

cat << EOF > ~/.config/polybar/launch.sh
#!/bin/bash
pkill polybar
polybar qtilebar &
EOF
chmod +x ~/.config/polybar/launch.sh

# Polybar scripts
cat << EOF > ~/.config/polybar/scripts/cpu.sh
#!/bin/bash
echo " \$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {printf \"%.0f%%\", usage}')"
EOF
chmod +x ~/.config/polybar/scripts/cpu.sh

cat << EOF > ~/.config/polybar/scripts/mem.sh
#!/bin/bash
free -h | awk '/Mem:/ {print " " $3 "/" $2}'
EOF
chmod +x ~/.config/polybar/scripts/mem.sh

cat << EOF > ~/.config/polybar/scripts/qtile-windows.py
#!/usr/bin/env python3
from libqtile.command.client import InteractiveCommandClient
client = InteractiveCommandClient()
groups = client.groups()
print(" ".join(f"[{name}]" if data['screen'] is not None else name for name, data in groups.items()))
EOF
chmod +x ~/.config/polybar/scripts/qtile-windows.py

# Rofi
cat << EOF > ~/.config/rofi/config.rasi
* {
  font: "JetBrainsMono Nerd Font 12";
  background: #282a36;
  foreground: #f8f8f2;
  border-color: #bd93f9;
  border-radius: 6px;
}
EOF

cat << EOF > ~/.config/rofi/power-menu.sh
#!/bin/bash
choice=$(printf " Shutdown\n Reboot\n Suspend\n Lock\n⏻ Logout" | rofi -dmenu -i -p "Power")
case "$choice" in
  " Shutdown") systemctl poweroff ;;
  " Reboot") systemctl reboot ;;
  " Suspend") systemctl suspend ;;
  " Lock") betterlockscreen -l ;;
  "⏻ Logout") archlinux-logout ;;
esac
EOF
chmod +x ~/.config/rofi/power-menu.sh

# Picom
cat << EOF > ~/.config/picom/picom.conf
corner-radius = 10;
blur-method = dual_kawase;
shadow = true;
fading = true;
opacity-rule = ["80:class_g = 'Rofi'"];
EOF

# Starship
cat << EOF > ~/.config/starship.toml
add_newline = true
format = "\n$directory$git_branch$character"
[character]
success_symbol = "[➜](#bd93f9)"
error_symbol = "[✗](#ff5555)"
[directory]
style = "#ff79c6"
EOF

# Variety
cat << EOF > ~/.config/variety/variety.conf
[General]
change_interval = 10
download_interval = 20
use_wallhaven = true
EOF

# Wallpapers
touch ~/Pictures/Wallpapers/dracula_wallpaper_1.jpg

# SDDM
echo "🎨 Installing SDDM Dracula theme..."
sudo mkdir -p /usr/share/sddm/themes/dracula
echo "# Dracula theme" | sudo tee /usr/share/sddm/themes/dracula/theme.conf > /dev/null
echo -e "[Theme]\nCurrent=dracula" | sudo tee /etc/sddm.conf.d/theme.conf

# Xinitrc fallback
echo "exec qtile" > ~/.xinitrc

# betterlockscreen prep
betterlockscreen -u ~/Pictures/Wallpapers/dracula_wallpaper_1.jpg

echo "✅ Done. Reboot and choose 'Qtile' from your login manager to use the Dracula desktop!"
