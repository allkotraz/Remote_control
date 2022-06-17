from PyQt5 import QtCore, QtGui, QtWidgets
import http.client
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime
from mouse import MouseWorker
from multiprocessing.dummy import Process

import socket

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(710, 530, 75, 23))
        self.pushButton_start.setObjectName("pushButton")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(630, 530, 75, 23))
        self.pushButton_stop.setObjectName("pushButton_2")

        self.log_view = QtWidgets.QTextEdit(self.centralwidget)
        self.log_view.setGeometry(QtCore.QRect(10, 340, 781, 181))
        self.log_view.setObjectName("listWidget")

        self.ip_line_text = QtWidgets.QTextEdit(self.centralwidget)
        self.ip_line_text.setGeometry(QtCore.QRect(10, 310, 150, 23))
        self.ip_line_text.setObjectName("ip_line_text")
        self.ip_line_text.setText("ip adress")
        self.ip_line_text.setEnabled(False)

        self.port_line_text = QtWidgets.QTextEdit(self.centralwidget)
        self.port_line_text.setGeometry(QtCore.QRect(180, 310, 150, 23))
        self.port_line_text.setObjectName("port_line_text")
        self.port_line_text.setText("port")
        self.port_line_text.setEnabled(False)

        self.host_line_text = QtWidgets.QTextEdit(self.centralwidget)
        self.host_line_text.setGeometry(QtCore.QRect(350, 310, 150, 23))
        self.host_line_text.setObjectName("host_line_text")
        self.host_line_text.setText("host_name")
        self.host_line_text.setEnabled(False)

        self._client = QtWidgets.QCheckBox(self.centralwidget)
        self._client.setGeometry(QtCore.QRect(10, 290, 200, 20))
        self._client.setObjectName("_client")
        self._client.setText("Вкл - Клиент, Выкл - Сервер")
        self._client.stateChanged.connect(self.state_changed)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 81, 16))
        self.label.setObjectName("label")
        self.ip_adress_label = QtWidgets.QLabel(self.centralwidget)
        self.ip_adress_label.setGeometry(QtCore.QRect(100, 10, 281, 16))
        self.ip_adress_label.setObjectName("ip_adress_label")

        self.local_label = QtWidgets.QLabel(self.centralwidget)
        self.local_label.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.local_label.setObjectName("label")
        self.local_ip_adress_label = QtWidgets.QLabel(self.centralwidget)
        self.local_ip_adress_label.setGeometry(QtCore.QRect(100, 30, 281, 16))
        self.local_ip_adress_label.setObjectName("local_ip_adress_label")

        self.local_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.local_label_2.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.local_label_2.setObjectName("label")
        self.local_ip_adress_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.local_ip_adress_label_2.setGeometry(QtCore.QRect(100, 50, 281, 16))
        self.local_ip_adress_label_2.setObjectName("local_ip_adress_label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self._isRunning = False

        Main_Window = self

        self.mouse_worker = MouseWorker(Main_Window)
        # self.worker_key = Worker_Keyboard(Main_Window)
        # self.worker_server = WorkerHTTPServer(Main_Window)
        self.mouse_thread = QThread()
        # self.thread_key = QThread()
        # self.thread_server = QThread()
        self.mouse_worker.progress.connect(self.button_start)
        # self.worker_key.progress.connect(self.button_start)
        # self.worker_server.progress.connect(self.button_start)

        self.retranslate_ui(MainWindow)

        self.pushButton_start.clicked.connect(self.button_start)
        self.pushButton_stop.clicked.connect(self.button_stop)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Remote control"))
        self.pushButton_start.setText(_translate("MainWindow", "Старт"))
        self.pushButton_stop.setText(_translate("MainWindow", "Стоп"))
        self.label.setText(_translate("MainWindow", "Global Adress :"))
        self.local_label.setText(_translate("MainWindow", "Local Adress :"))
        self.local_label_2.setText(_translate("MainWindow", "Local Adress :"))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip_adress_label.setText(_translate("MainWindow", f'{self.get_ip()}'))
        self.local_ip_adress_label.setText(_translate("MainWindow", f'{socket.gethostbyname(socket.gethostname())}'))
        self.local_ip_adress_label_2.setText(_translate("MainWindow", f'{s.getsockname()[0]}'))

    def state_changed(self, int):
        if self._client.isChecked():
            self.ip_line_text.setEnabled(True)
            self.port_line_text.setEnabled(True)
            self.host_line_text.setEnabled(True)
        else:
            self.ip_line_text.setEnabled(False)
            self.port_line_text.setEnabled(False)
            self.host_line_text.setEnabled(False)

    def append_text_log(self, action_name='None'):
        now = datetime.now()
        self.log_view.append(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {action_name}")

    def start_stop(self, bool):
        self._isRunning = bool
        self.pushButton_start.setEnabled(not bool)
        self.pushButton_stop.setEnabled(bool)

    def start_mouse_listener(self):
        self.mouse_worker.moveToThread(self.mouse_thread)
        self.mouse_thread.started.connect(self.mouse_worker.run)
        self.mouse_thread.start()

    def stop_mouse_listener(self):
        self.mouse_worker.stop()
        self.mouse_thread.quit()

    def start_thread(self):
        self.start_stop(True)

        if not self._client.isChecked():
            self.start_mouse_listener()
        self.append_text_log(action_name="Start")

    def stop_thread(self):
        self.start_stop(False)
        if not self._client.isChecked():
            self.stop_mouse_listener()
        self.append_text_log(action_name="Stop")

    def msg_print(self):
        msg = QMessageBox(QMessageBox.Information, "Окно Worker", "Окно Worker")
        msg.exec()

    def get_ip(self):
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        return str(conn.getresponse().read().decode())

    def button_start(self):
        self.start_thread()

    def button_stop(self):
        self.stop_thread()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
