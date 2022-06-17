from pynput import mouse
from PyQt5.QtCore import *

def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1} button {2}'.format('Pressed' if pressed else 'Released', (x, y), button))

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    print('{0} release'.format(key))

class MouseWorker(QObject):
    progress = pyqtSignal()

    def __init__(self, main):
        super().__init__()
        self.main = main

    def run(self):
        while True:  # Цикл вне блока with для постоянного обновления очереди
            if not self.main._isRunning:
                break
            else:
                with mouse.Events() as events:
                    event = events.get(1)  # Ждём событие клавиши 1 секунду
                    if event == None:  # Если события не было, обновляем очередь
                        continue
                    elif isinstance(event, mouse.Events.Move):  # Кнопка зажата
                        on_move(event.x, event.x)
                    elif isinstance(event, mouse.Events.Click):
                        on_click(event.x, event.y, event.button, event.pressed)
                        if event.button == mouse.Button.left:
                            import requests

                    elif isinstance(event, mouse.Events.Scroll):
                        on_scroll(event.x, event.y, event.dx, event.dy)
                    else:  # Логируем если появляется неизвестный event
                        self.main.append_text_log(action_name=f'Действие - {event}')

    def stop(self):
        self._isRunning = False

