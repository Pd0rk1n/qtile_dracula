#!/bin/bash

# Kill any running Polybar instance
killall -q polybar

# Wait for it to fully close
while pgrep -u $USER -x polybar >/dev/null; do sleep 1; done

# Launch Polybar on all monitors
for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
    MONITOR=$m polybar --reload mainbar-qtile &
done
