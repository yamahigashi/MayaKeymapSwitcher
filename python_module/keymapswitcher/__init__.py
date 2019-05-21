# # -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import os
import glob
from collections import OrderedDict


def get_keymaps():
    # type: () -> Dict[Text, Text]
    """Returns dict that key is keymap name and value is path."""
    import maya.cmds as cmds

    user_pref_dir = cmds.internalVar(upd=True).rstrip("/").rstrip(os.sep)
    maps = glob.glob("{}/hotkeys/userHotkeys_*.mel".format(user_pref_dir))

    res = OrderedDict()
    for hotkeymap in maps:
        match = re.search("userHotkeys_(\w+).mel", hotkeymap)
        if not match:
            continue

        res[match.groups(1)[0]] = hotkeymap.replace(os.sep, "/")

    return res


def get_main_window():
    from keymapswitcher.vendor.Qt import QtWidgets

    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj


def source_additional_directories():
    import os
    import glob
    import maya.mel as mel

    print(os.getenv("HOTKEY_DIRS", []))

    for directory in os.getenv("HOTKEY_DIRS", "").split(";"):
        query = os.path.join(directory, "userHotkeys_*.mel")
        for hotkey in glob.glob(query):
            normalized = os.path.abspath(hotkey).replace(os.sep, "/")
            print("source hotkey {}".format(normalized))
            mel.eval('''source "{}";'''.format(normalized))


def inject_keymap_switcher():

    from keymapswitcher.vendor.Qt import QtWidgets
    import keymapswitcher.widget as widget

    for kid in get_main_window().children():
        if isinstance(kid, QtWidgets.QMenuBar):
            menuBar = kid
            break
    else:
        raise Exception("menuBar not found")

    corner = menuBar.cornerWidget()

    cbox = widget.SelectorCombobox(implicitSave=True)

    oldLayout = corner.layout()
    oldLayout.addWidget(cbox)
    oldLayout.update()


def change_to(keymap):
    # type: (Text) -> None
    import maya.mel as mel
    import maya.cmds as cmds

    menu_set = mel.eval("""findMenuSetFromLabel("{}");""".format(keymap))

    cmds.hotkeySet(keymap, e=True, current=True)
    if cmds.menuSet(q=True, exists=menu_set):
        cmd = """workingMode("{}");""".format(menu_set)
        mel.eval(cmd)
