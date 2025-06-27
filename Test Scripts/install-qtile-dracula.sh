#!/bin/bash
set -e

echo "📁 Copying configs to ~/.config/..."

mkdir -p ~/.config/qtile ~/.config/polybar/scripts ~/.config/rofi ~/.config/variety ~/Pictures/Wallpapers

cp -v ./qtile/config.py ~/.config/qtile/
cp -v ./polybar/config.ini ~/.config/polybar/
cp -v ./polybar/launch.sh ~/.config/polybar/
cp -v ./polybar/scripts/* ~/.config/polybar/scripts/
cp -v ./rofi/config.rasi ~/.config/rofi/
cp -v ./rofi/power-menu.sh ~/.config/rofi/
cp -v ./variety/variety.conf ~/.config/variety/
cp -v ./wallpapers/* ~/Pictures/Wallpapers/

chmod +x ~/.config/polybar/launch.sh
chmod +x ~/.config/polybar/scripts/*.sh ~/.config/polybar/scripts/*.py
chmod +x ~/.config/rofi/power-menu.sh

echo "🎨 Installing Dracula SDDM theme..."

sudo mkdir -p /usr/share/sddm/themes/dracula
sudo cp -rv ./sddm/dracula/* /usr/share/sddm/themes/dracula/
sudo mkdir -p /etc/sddm.conf.d
echo -e "[Theme]\nCurrent=dracula" | sudo tee /etc/sddm.conf.d/theme.conf

echo "🧊 Setting up betterlockscreen background..."
betterlockscreen -u ~/Pictures/Wallpapers/dracula_wallpaper_1.jpg

echo "✅ Done! Reboot to see the SDDM theme and log into Qtile."
