import sys
import argparse

from keymapswitcher.vendor.Qt import QtWidgets, QtCore, QtGui  # type: ignore
from . import widget

if False:
    # For type annotation
    from typing import Any, Dict, List, Type, Text, Tuple  # NOQA
    from PyQt5 import QtCore, QtWidgets, QtGui  # NOQA


self = sys.modules[__name__]
self._window = None


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--implicit',
        '-i',
        action='store_true',
    )
    arg = parser.parse_args()
    app = QtWidgets.QApplication(sys.argv)
    dialog = widget.ProjectSelector(implicitSave=arg.implicit)
    dialog.show()
    dialog.exec_()


if __name__ == "__main__":
    sys.exit(cli())
