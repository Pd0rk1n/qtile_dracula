# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.lazy import lazy
from libqtile.widget import Spacer
# import arcobattery

import os
import subprocess
from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])


# mod4 or mod = super key
mod = "mod4"
myTerm = "xfce4-terminal"      # My terminal of choice
myBrowser = "brave"       # My browser of choice
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [

    # Most of our keybindings are in sxhkd file - except these
    # SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


    # SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    

    #  Fix Bar
Key(["mod4", "shift"], "t", lazy.spawn("~/bin/restart-tray-apps.sh"), desc="Restart tray apps")



    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod, "shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod, "shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
# group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
# group_labels = ["", "", "", "", "", "", "", "", "", "",]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall",]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), 
            lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin": 5,
            "border_width": 5,
            "border_focus": "#FF0055",
            "border_normal": "#4c566a"
            }


layout_theme = init_layout_theme()


layouts = [
    # layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Dracula
def init_colors():
    return [["#000000", "#000000"], # color 0
            ["#282A36", "#282A36"], # color 1
            ["#F8F8F2", "#F8F8F2"], # color 2
            ["#F1FA8C", "#F1FA8C"], # color 3
            ["#BD93F9", "#BD93F9"], # color 4
            ["#FF79C6", "#FF79C6"], # color 5
            ["#8BE9FD", "#8BE9FD"], # color 6
            ["#BFBFBF", "#BFBFBF"], # color 7
            ["#4D4D4D", "#4D4D4D"], # color 8
            ["#FF5555", "#FF5555"]] # color 9


colors = init_colors()

#extra icons to choose from
#http://fontawesome.io/cheatsheet/
#       v              


# WIDGETS FOR THE BAR




def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize=12,
                padding=0,
                background=colors[1])


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        widget.GroupBox(
            center_aligned=True,
            font="JetBrainsMono Nerd Font",  # Or any monospaced font you have installed
            fontsize=16,
            margin_y=3,
            margin_x=3,
            padding_y=4,
            padding_x=2,
            borderwidth=0,
            disable_drag=True,
            active=colors[2],
            inactive=colors[5],
            rounded=False,
            highlight_method="text",  # Optional: improves visual alignment
            this_current_screen_border=colors[8],
            foreground=colors[2],
            background=colors[0],
            ),

        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[0]
            ),
        widget.CurrentLayout(
            font="Noto Sans Bold",
            foreground=colors[6],
            background=colors[1]
            ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[0]
            ),
        widget.WindowName(
            font="Noto Sans",
            fontsize=14,
            foreground=colors[5],
            background=colors[0],
            ),
         widget.Net(
                  font="Noto Sans",
                  fontsize=14,
                  interface="enp2s0",
                  foreground=colors[5],
                  background=colors[0],
                  padding = 0,
                  ),
         widget.Sep(
                  linewidth = 0,
                  padding = 10,
                  foreground = colors[2],
                  background = colors[0]
                  ),
         #widget.NetGraph(
         #         font="Noto Sans",
         #         fontsize=12,
         #         bandwidth="down",
         #         interface="auto",
         #         fill_color = colors[4],
         #         foreground=colors[2],
         #         background=colors[0],
         #         graph_color = colors[8],
         #         border_color = colors[3],
         #         padding = 0,
         #         border_width = 1,
         #         line_width = 1,
         #         ),
         widget.Sep(
                  linewidth = 1,
                  padding = 10,
                  foreground = colors[2],
                  background = colors[0]
                  ),
        # # do not activate in Virtualbox - will break qtile
        # widget.ThermalSensor(
        #          foreground = colors[5],
        #          foreground_alert = colors[6],
        #          background = colors[1],
        #          metric = True,
        #          padding = 3,
        #          threshold = 80
        #          ),
        # # battery option 1  ArcoLinux Horizontal icons do not forget to import arcobattery at the top
        # widget.Sep(
        #          linewidth = 1,
        #          padding = 10,
        #          foreground = colors[2],
        #          background = colors[1]
        #          ),
        # arcobattery.BatteryIcon(
        #          padding=0,
        #          scale=0.7,
        #          y_poss=2,
        #          theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
        #          update_interval = 5,
        #          background = colors[1]
        #          ),
        # # battery option 2  from Qtile
        # widget.Sep(
        #          linewidth = 1,
        #          padding = 10,
        #          foreground = colors[2],
        #          background = colors[1]
        #          ),
        # widget.Battery(
        #          font="Noto Sans",
        #          update_interval = 10,
        #          fontsize = 12,
        #          foreground = colors[5],
        #          background = colors[1],
        #          ),
         widget.TextBox(
                  font="FontAwesome",
                  text="  ",
                  foreground=colors[9],
                  background=colors[0],
                  padding = 0,
                  fontsize=16
                  ),
         widget.CPU(
                  border_color = colors[5],
                  fill_color = colors[6],
                  graph_color = colors[6],
                  foreground=colors[4],
                  background=colors[0],
                  border_width = 1,
                  line_width = 1,
                  core = "all",
                  type = "box"
                  ),
         widget.Sep(
                  linewidth = 1,
                  padding = 10,
                  foreground = colors[2],
                  background = colors[0]
                  ),
         # widget.TextBox(
         #         font="FontAwesome",
         #         text="  ",
         #         foreground=colors[4],
         #         background=colors[1],
         #         padding = 0,
         #         fontsize=16
         #         ),
         # widget.Memory(
         #         font="Noto Sans",
         #         format = '{MemUsed}M/{MemTotal}M',
         #         update_interval = 1,
         #         fontsize = 12,
         #         foreground = colors[5],
         #         background = colors[1],
         #        ),
         #  widget.Sep(
         #          linewidth = 1,
         #         padding = 10,
         #         foreground = colors[2],
         #         background = colors[0]
         #         ),
        widget.LaunchBar(
                 progs = [("", "brave", "Brave web browser"),
                          ("", "xfce4-terminal", " xfce4 terminal"),
                          ("", "nemo", "nemo file manager"),
                          ("", "vlc", "VLC media player")
                         ], 
                 fontsize = 14,
                 padding = 12,
                 foreground = colors[3],
                 background=colors[0],
                 ),
        widget.Sep(
                   linewidth = 1,
                  padding = 10,
                  foreground = colors[2],
                  background = colors[0]
                  ),
        widget.TextBox(
            font="FontAwesome",
            text="  ",
            foreground=colors[3],
            background=colors[0],
            padding=3,
            fontsize=16
            ),
        widget.Clock(
            foreground=colors[4],
            background=colors[0],
            fontsize=12,
            format="%Y-%m-%d %H:%M"
            ),
         widget.Sep(
                  linewidth = 1,
                  padding = 10,
                  foreground = colors[2],
                  background = colors[0]
                  ),
        widget.Systray(
            background=colors[0],
            icon_size=22,
            padding=3
            ),
        ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=1)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=1))]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
from libqtile import hook
from libqtile.log_utils import logger

@hook.subscribe.client_new
def assign_app_group(client):
    app_groups = {
        "1": ["nemo"],
        "2": ["xed"],
        "3": ["brave", "brave-browser"],
        "5": ["xfce4-terminal"],
        "6": ["vlc"],
        "7": ["transmission-gtk", "transmission-qt"]
    }

    wm_class = client.window.get_wm_class()
    if wm_class:
        app = wm_class[0].lower()
        logger.warning(f"[Assign Hook] App started: {app}")
        for group, apps in app_groups.items():
            if app in [a.lower() for a in apps]:
                client.togroup(group)
                client.group.cmd_toscreen(toggle=False)  # ← this switches to the group
                logger.warning(f"[Assign Hook] Moved {app} to group {group} and switched to it")
                break



# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None

# hides the top bar when the archlinux-logout widget is opened

@hook.subscribe.client_new
def new_client(window):
    if window.name == "ArchLinux Logout":
        qtile.hide_show_bar()


# shows the top bar when the archlinux-logout widget is closed
@hook.subscribe.client_killed
def logout_killed(window):
    if window.name == "ArchLinux Logout":
        qtile.hide_show_bar()


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
#    Match(wm_class='xfce4-terminal'),

],  fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
