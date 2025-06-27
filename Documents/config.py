from libqtile import layout, hook
from libqtile.config import Key, Group, Screen
from libqtile.lazy import lazy

mod = "mod4"

keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),

    Key([mod], "space", lazy.next_layout()),

    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),

    Key([mod], "Return", lazy.spawn("alacritty")),

    Key([mod], "d", lazy.spawn("dmenu_run")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Max(),
    layout.MonadTall(),
    layout.Stack(num_stacks=2),
]

# No Qtile bar defined here, since Polybar will be the panel.

@hook.subscribe.startup_once
def autostart():
    import subprocess
    # Start Polybar on startup (change your monitor name if needed)
    subprocess.Popen(["polybar", "qtilebar"])

    # Set a default cursor
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])

floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wname': 'branchdialog'},
    {'wname': 'pinentry'},
])

