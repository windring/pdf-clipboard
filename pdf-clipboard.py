import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *


class ClipData:
    def __init__(self):
        self.pre_text = ''
        self.ful_text = []

    def val_text(self, text):
        return text != self.pre_text

    def set_text(self, text):
        self.pre_text = text
        text = text.replace('-\r', ' ', -1)
        text = text.replace('-\n', ' ', -1)
        text = text.replace('\r', ' ', -1)
        text = text.replace('\n', ' ', -1)
        text = text.replace(' ', ' ', -1)
        text += '\n'
        print(f'[Add]\n{text}')
        self.ful_text.append(text)
        return self.get_ful_text()

    def get_ful_text(self):
        return '\n'.join(self.ful_text)

    def back(self):
        if len(self.ful_text) == 0:
            return self.get_ful_text()
        self.ful_text.pop()
        self.pre_text = self.ful_text[-1]
        return self.get_ful_text()

    def copy(self):
        self.pre_text = self.get_ful_text()
        return self.pre_text


def on_clipboard_change():
    global clipboard
    data = clipboard.mimeData()
    text = data.text()
    if data.hasText() and clipdata.val_text(text):
        text_box.setPlainText(clipdata.set_text(text))


def on_clear():
    global clipdata, text_box
    print('[clear]')
    clipdata = ClipData()
    text_box.clear()


def on_copy():
    global clipdata, clipboard
    print('[copy]')
    clipboard.setText(clipdata.copy())


def on_back():
    global clipdata, text_box
    print('[back]')
    text_box.setPlainText(clipdata.back())


clipdata = ClipData()

app = QApplication(sys.argv)

win = QMainWindow()
win.setMinimumSize(QSize(800, 600))
win.setWindowTitle('Pdf Clipboard')

text_box = QPlainTextEdit()
win.setCentralWidget(text_box)


clear_act = QAction(win)
clear_act.setText('clear')
clear_act.triggered.connect(on_clear)
win.menuBar().addAction(clear_act)


copy_act = QAction(win)
copy_act.setText('copy')
copy_act.triggered.connect(on_copy)
win.menuBar().addAction(copy_act)


back_act = QAction(win)
back_act.setText('back')
back_act.triggered.connect(on_back)
win.menuBar().addAction(back_act)

clipboard = app.clipboard()
clipboard.dataChanged.connect(on_clipboard_change)

win.show()
sys.exit(app.exec_())
