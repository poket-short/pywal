"""
kde.
"""
import logging
import os
import random
import re
import sys
import dbus

from . import theme
from . import util
from .settings import CACHE_DIR, MODULE_DIR, __cache_version__


def setwallpaper(filepath, plugin = 'org.kde.image'):
    jscript = """
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "%s";
        d.currentConfigGroup = Array("Wallpaper", "%s", "General");
        d.writeConfig("Image", "file://%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % (plugin, plugin, filepath))


def setcolorcheme(colors):
    print(colors)
    print(colors["special"]["background"])
    #colors["special"]["background"].lstrip('#')
    color_rgb = tuple(int(colors["colors"]["color1"].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    backgroundDic = {'Colors:Button': 'BackgroundNormal',
     'Colors:Complementary': 'BackgroundNormal',
     'Colors:Tooltip': 'BackgroundNormal',
     'Colors:View': ('BackgroundAlternate', 'BackgroundNormal'),
     'Colors:Window': 'BackgroundNormal',
     'WM': ('activeBackground', 'inactiveBackground')}

    applyColorScheme(backgroundDic, color_rgb) 


def applyColorScheme(dic, color):

    for key,value in dic.items():
        if type(value) == tuple:
            for i in dic[key]:
                bashCommand = "kwriteconfig5 --file ~/.config/kdeglobals --group \"{}\" --key \"{}\" \"{},{},{}\"".format(key, i, color[0], color[1], color[2])
                os.system(bashCommand)
        else:
            bashCommand = "kwriteconfig5 --file ~/.config/kdeglobals --group \"{}\" --key \"{}\" \"{},{},{}\"".format(key, value, color[0], color[1], color[2])
            os.system(bashCommand)
