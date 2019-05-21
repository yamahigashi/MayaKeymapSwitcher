# -*- coding: utf-8 -*-
import maya.utils as utils


def keymap_switcher_execute_after_start():
    try:
        import keymapswitcher
        print("keymap switcher injecting begin")
        keymapswitcher.inject_keymap_switcher()

    except Exception:
        # avoidng the invoking userSetup.py chain accidentally stop,
        # all exception must collapse
        print("keymap switcher injecting failed")
        import traceback
        traceback.print_exc()


utils.executeDeferred('keymap_switcher_execute_after_start()')
