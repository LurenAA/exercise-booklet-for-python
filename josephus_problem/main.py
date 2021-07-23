from ui.view_controller import MainWindow

import sys

from PySide6.QtWidgets import QApplication
import click

UI = "ui"
CMD = "cmd"
STYLE = "--style"
COMMAND_HELP = "选择显示模式（ui或者cmd）,不可识别的输入默认为ui"
COMMAND_PROMPT = COMMAND_HELP


@click.command()
@click.option(
    STYLE,
    default=UI,
    help=COMMAND_HELP,
    prompt=COMMAND_PROMPT
)
def start(style):
    if style not in (UI, CMD):
        style = UI
    if style == CMD:
        ...
    elif style == UI:
        app = QApplication()
        widget = MainWindow()
        widget.show()
        app.exec()


if __name__ == "__main__":
    start()
