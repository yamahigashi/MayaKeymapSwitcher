# # -*- coding: utf-8 -*-
import sys
import contextlib

import maya.cmds as cmds

import keymapswitcher
from keymapswitcher.vendor.Qt import QtWidgets, QtCore, QtGui  # type: ignore

if False:
    # For type annotation
    from typing import Any, Dict, List, Type, Text, Tuple  # NOQA
    from PyQt5 import QtCore, QtWidgets, QtGui  # NOQA


self = sys.modules[__name__]
self._window = None


@contextlib.contextmanager
def application():
    app = QtWidgets.QApplication.instance()

    if not app:
        print("Starting new QApplication..")
        app = QtWidgets.QApplication(sys.argv)
        yield app
        app.exec_()
    else:
        print("Using existing QApplication..")
        yield app


class KeymapSwitcher(QtWidgets.QDialog):
    """Pass."""

    def __init__(self, keymaps=None, current=None, implicitSave=False, parent=None):
        # type: (Text, Dict, QtCore.QObject) -> None
        super(KeymapSwitcher, self).__init__(parent)

        self.implicitSave = implicitSave

        title = "Hotkey Switcher"
        self.setWindowTitle(title)

        self.innerWidget = SelectorCombobox(
            keymaps=keymaps,
            current=current,
            implicitSave=implicitSave,
            parent=self
        )

        self.grid = QtWidgets.QGridLayout(self)
        self.grid.addWidget(self.innerWidget, 0, 0, 1, 1)

        if not self.implicitSave:
            self.ok_button = QtWidgets.QPushButton("ok", self)
            self.grid.addWidget(self.ok_button, 1, 1, 1, 1)
            self.ok_button.clicked.connect(self.accept)

    def getResult(self, exit_code):
        # type: (int) -> Tuple

        if exit_code != QtWidgets.QDialog.Accepted:
            return None

        new_name = self.innerWidget.selector.currentText()
        new = next(x for x in self.innerWidget.keymaps if x.get("name") == new_name)
        # request.set_shotgun_project(new_name)

        return new

    def keyPressEvent(self, event):
        # type: (QtGui.QEvent) -> None
        super(KeymapSwitcher, self).keyPressEvent(event)
        if type(event) == QtGui.QKeyEvent:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.accept()


class SelectorCombobox(QtWidgets.QWidget):
    """Pass."""

    def __init__(self, keymaps=None, current=None, implicitSave=False, parent=None):
        # type: (Text, Dict, QtCore.QObject) -> None
        super(SelectorCombobox, self).__init__(parent)

        self.implicitSave = implicitSave

        if not keymaps:
            self.keymaps = keymapswitcher.get_keymaps().keys()
        else:
            self.keymaps = keymaps

        if not current:
            self.current = cmds.hotkeySet(q=True, current=True)
        else:
            self.current = current

        self.keymaps.insert(0, "Maya_Default")
        items = self.keymaps
        self.selector = QtWidgets.QComboBox(self)
        self.selector.addItems(items)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("hotkey:"))
        self.layout.addWidget(self.selector)
        self.layout.setContentsMargins(0, 0, 0, 0)

        try:
            self.selector.setCurrentText(self.current)

        except AttributeError:
            for i, name in enumerate(items):
                if self.current == name:
                    self.selector.setCurrentIndex(i)

        if self.implicitSave:
            self.selector.currentIndexChanged.connect(self.selectorChanged)

    def selectorChanged(self, index):
        change_to = self.keymaps[int(index)]
        keymapswitcher.change_to(change_to)


def switch(keymaps, current, debug=False):
    # type: (Dict, Text, bool) -> None
    """Display task updater GUI."""

    if self._window:
        self._window.close()
        del(self._window)

    try:
        widgets = QtWidgets.QApplication.topLevelWidgets()
        widgets = dict((w.objectName(), w) for w in widgets)
        parent = widgets["MayaWindow"]

    except KeyError:
        parent = None

    with application():
        dialog = KeymapSwitcher(keymaps, current, parent)
        self._dialog = dialog

        res = dialog.exec_()
        return dialog.getResult(res)
