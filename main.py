import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QDialog, QGridLayout, QWidget, \
    QHBoxLayout, QTabWidget, QVBoxLayout, QGroupBox, QLabel
from PyQt5.QtCore import QTimer
import can
import time


class CANMonitorApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Monitor")
        self.setGeometry(300, 150, 600, 400)
        self.timer = QTimer(self)

        # Create groupboxes
        self.createCanAnalyzerGroupBox()
        self.createButtonGroupBox()

        top_layout = QHBoxLayout()

        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 2, 3)
        main_layout.addWidget(self.createCanAnalyzerGroupBox(), 0, 0)
        main_layout.addWidget(self.createButtonGroupBox(), 0, 1)

        self.setLayout(main_layout)

        self.can_bus = None

    def createCanAnalyzerGroupBox(self):
        self.canAnalyzerGroupBox = QGroupBox("CAN frames monitor")
        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 250, 250)
        self.canAnalyzerGroupBox.setLayout(layout)

    def createButtonGroupBox(self):
        self.buttonGroupBox = QGroupBox("Buttons")
        layout = QVBoxLayout()
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(10, 270, 110, 30)
        self.start_button.clicked.connect(self.start_can_monitor)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(150, 270, 110, 30)
        self.stop_button.clicked.connect(self.stop_can_monitor)

        self.buttonGroupBox.setLayout(layout)

    def start_can_monitor(self):
        if not self.can_bus:
            try:
                self.can_bus = can.interface.Bus(bustype ='pcan', channel='PCAN_USBBUS1', bitrate = 500000)
                self.text_edit.append("CAN Monitor started...")

                self.timer.timeout.connect(self.receive_can_frames)
                self.timer.start(2000)

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

                msg_timestamp = msg.timestamp
                msg_id = msg.arbitration_id
                msg_data = msg.data
                msg_dlc = msg.dlc
                msg_bitrate = msg.bitrate_switch

                self.analyze_can_frame(msg_id, msg_data)

            except Exception as exc:
               self.text_edit.append("Error receiving CAN frame: " + str(exc))


    def analyze_can_frame(self, msg_id, msg_data):
        self.turn_lights_id = 2
        self.brake_lights_id = 3
        self.beam_lights_id = 4
        self.fuel_tank_id = 6
        self.inside_light_id = 9
        self.driver_window = 13
        self.passenger_window = 12

        if msg_id == self.turn_lights_id:
            msg_data_array = bytearray(msg_data)
            msg_data_list = [byte for byte in msg_data_array]
            print(msg_data_list)
            print("test swiatel awaryjnych")
            # if msg_data ==

            # wylaczone swiatla 00 40 80
            # zapalone swiatla 1F 40 80
    # def send_can_frames(self):
    #     if self.can_bus:
    #         with can.bus() as bus:
    #             message = can.Message(arbitration_id=0x00, data=[0],is_extended_id=False)
    #         try:
    #             bus.send(message)
    #             print(f"Message sent!")
    #         except:
    #             print(f"Message not sent...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CANMonitorApp()
    window.show()
    sys.exit(app.exec_())

