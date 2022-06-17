import mouse, keyboard
from pynput import keyboard as py_keyboard
from PyQt5.QtCore import *

main_window = False


def on_down(key):  # Колбек зажатой кнопки
    print("Pressed {}".format(key))
    # input("input:") # input не вылетает и не зависает


def on_up(key):  # Колбек отжатой кнопки
    print("Released {}".format(key))


def print_pressed_keys(event):
    dir_event = ['device', 'event_type', 'is_keypad', 'modifiers', 'name', 'scan_code', 'time', 'to_json']
    print(event, event.event_type, event.name)
    if not main_window._isRunning:
        mouse.unhook_all()
        keyboard.unhook_all()


class Worker_Keyboard(QObject):
    progress = pyqtSignal()

    def __init__(self, main):
        super().__init__()
        self.main = main

    def run(self):
        global main_window
        main_window = self.main
        self.keyborad_hooks()

    def keyborad_hooks(self):
        keyboard.add_hotkey('Ctrl + 1', lambda: print('Hello'))
        keyboard.hook(print_pressed_keys, suppress=True)


    def keyboard_listener(self):
        while True:  # Цикл вне блока with для постоянного обновления очереди
            if not self.main._isRunning:
                break
            else:
                with py_keyboard.Events() as events:
                    event = events.get(1)  # Ждём событие клавиши 1 секунду
                    if event == None:  # Если события не было, обновляем очередь
                        continue
                    elif isinstance(event, py_keyboard.Events.Press):  # Кнопка зажата
                        on_down(event.key)
                    else:  # Кнопка отжата
                        on_up(event.key)

    def stop(self):
        self._isRunning = False