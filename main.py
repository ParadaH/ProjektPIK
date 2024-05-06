import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QDialog, QGridLayout, QWidget
from PyQt5.QtCore import QTimer
import can
import time


class CANMonitorApp(QMainWindow):

    def __init__(self, parnet=None):
        super().__init__()
        self.setWindowTitle("CAN Monitor")
        self.setGeometry(100, 100, 600, 400)
        self.timer = QTimer(self)

        main_layout = QGridLayout()
        main_layout.addWidget(QLabel)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 580, 300)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(10, 320, 100, 30)
        self.start_button.clicked.connect(self.start_can_monitor)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(120, 320, 100, 30)
        self.stop_button.clicked.connect(self.stop_can_monitor)

        # Loop for receiving CAN frames

        self.can_bus = None

    def start_can_monitor(self):
        if not self.can_bus:
            try:
                self.can_bus = can.interface.Bus(bustype ='pcan', channel='PCAN_USBBUS1', bitrate = 500000)
                self.text_edit.append("CAN Monitor started...")
                self.start_button_on()

                self.timer.timeout.connect(self.receive_can_frames)
                self.timer.start(10)

                # while(1):
                #     msg = self.can_bus.recv()
                #     self.text_edit.append("{}".format(msg))
                # self.text_edit.append("{}".format(msg.timestamp))
                # self.text_edit.append("{}".format(msg.data))
                # self.text_edit.append("{}".format(msg.dlc))
                # self.text_edit.append("{}".format(msg.arbitration_id))
                # self.text_edit.append("{}".format(msg.bitrate_switch))
                # print(msg)

            except Exception as e:
                self.text_edit.append("Error: " + str(e))

    def stop_can_monitor(self):
        if self.can_bus:
            self.can_bus.shutdown()
            self.can_bus = None
            self.timer.stop()
            self.text_edit.append("CAN Monitor stopped.")

    def receive_can_frames(self):
        if self.can_bus:
            try:
               msg = self.can_bus.recv()
               self.text_edit.append("Received CAN frame: ID={}, Data={}".format(msg.arbitration_id, msg.data))

            except Exception as exc:
               self.text_edit.append("Error receiving CAN frame: " + str(exc))

    # def send_can_frames(self):
    #     if self.can_bus:
    #         with can.bus() as bus:
    #             message = can.Message(arbitration_id=0x00, data=[0],is_extended_id=False)
    #         try:
    #             bus.send(message)
    #             print(f"Message sent!")
    #         except:
    #             print(f"Message not sent...")

class TabsWidget(QWidget):

    def __init__(self, parent, width, height):
        super().__init__(parent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CANMonitorApp()
    window.show()
    sys.exit(app.exec_())

