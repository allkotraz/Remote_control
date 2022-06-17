'''
    from pynput import mouse

    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    # Collect events until released
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()
'''

'''
import threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class Worker(QObject):
    progress = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.i = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)

    def run(self):
        print(self.i)
        self.i = self.i + 1
        if self.i == 10:
            self.progress.emit()


class MainClass(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.thread = QThread()
        self.worker = Worker()
        self.worker.progress.connect(lambda: self.msg_print())

    def start_thread(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def msg_print(self):
        msg = QMessageBox(QMessageBox.Information,
                          "Окно Worker", "Окно Worker")
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_class = MainClass()
    main_class.start_thread()

    dialog = QMessageBox(QMessageBox.Information,
                         "Типа главное окно", "Типа главное окно")
    dialog.exec()
'''