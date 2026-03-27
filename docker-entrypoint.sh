#!/bin/sh
set -e
export DISPLAY=:99

rm -f /tmp/.X99-lock /tmp/.X11-unix/X99 2>/dev/null || true

# Virtual framebuffer sized for WINDOW_WIDTH x WINDOW_HEIGHT (see main.py)
Xvfb :99 -screen 0 1000x520x24 -ac +extension RANDR +extension RENDER &
sleep 0.5

# Minimal window manager helps pygame window focus and stacking
fluxbox -display :99 &
sleep 0.3

# VNC: connect with RealVNC/TightVNC to host port 5900 (mapped in compose/run)
x11vnc -display :99 -forever -shared -nopw -listen 0.0.0.0 -rfbport 5900 &
sleep 0.3

exec python main.py
