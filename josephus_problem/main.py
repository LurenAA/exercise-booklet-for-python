import sys

from ui.view_controller import MainWindow
from cli.jc_shell import JcShell

from PySide6.QtWidgets import QApplication
import click

UI = "ui"
CMD = "cmd"
STYLE = "--style"
COMMAND_HELP = "选择显示模式"
COMMAND_PROMPT = COMMAND_HELP


@click.command()
@click.option(
    STYLE,
    type=click.Choice([UI, CMD]),
    help=COMMAND_HELP,
    prompt=COMMAND_PROMPT
)
def start(style):
    if style == CMD:
        JcShell().cmdloop()
    elif style == UI:
        app = QApplication()
        widget = MainWindow()
        widget.show()
        app.exec()


if __name__ == "__main__":
    start()
