# wowmouse

Small X11 overlay that draws a cursor image and plays a "WOW" scale animation
when any mouse button is pressed. The overlay is click-through and follows the
system cursor.

Tested on Debian 13. Feedback from testing on other distros is welcome.

## Install (for current user)

1. Install dependencies on Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-pyqt6 python3-xlib
```

2. Create a launcher in `~/.local/bin`:

```bash
cat > ~/.local/bin/wowmouse <<'EOF'
#!/bin/sh
cd /absolute/path/to/wowmouse
exec python3 /absolute/path/to/wowmouse/wowmouse.py
EOF
chmod 755 ~/.local/bin/wowmouse
```

Replace `/absolute/path/to/wowmouse` with your project directory. If you move
the directory later, update the launcher.
s
If `~/.local/bin` is not in your `PATH`, add:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Run:

```bash
wowmouse
```

To run without installing, place `overlay.png` next to `wowmouse.py`, then:

```bash
python3 wowmouse.py
```
