import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QDialog, QGridLayout, QWidget, \
    QHBoxLayout, QTabWidget, QVBoxLayout, QGroupBox, QLabel, QStyleFactory, QComboBox
from PyQt5.QtCore import QTimer
import can


class CANMonitorApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Monitor")
        self.setGeometry(300, 150, 600, 400)
        self.text_edit = QTextEdit()
        self.timer = QTimer(self)
        self.can_bus = None


        self.pixmap = QPixmap('kierunkowskaz lewy 50.png')

        # Create main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create and apply grid layout in main widget
        main_layout = QGridLayout()
        self.central_widget.setLayout(main_layout)

        # Create text_edit panel (CAN analyzer) and buttons
        text_edit_groupbox = self. create_can_analyzer_groupbox()
        main_layout.addWidget(text_edit_groupbox, 0, 0)

        buttons_groupbox = self.create_button_groupbox()
        main_layout.addWidget(buttons_groupbox, 1, 0)

    def create_can_analyzer_groupbox(self):
        text_edit_groupbox = QGroupBox("CAN frames monitor")
        text_edit_layout = QGridLayout()
        text_edit_groupbox.setLayout(text_edit_layout)

        text_edit_layout.addWidget(self.text_edit)

        return text_edit_groupbox

    def create_button_groupbox(self):
        buttons_groupbox = QGroupBox()
        buttons_layout = QHBoxLayout()
        buttons_groupbox.setLayout(buttons_layout)

        start_button = QPushButton("Start", self)
        start_button.clicked.connect(self.start_can_monitor)

        stop_button = QPushButton("Stop", self)
        stop_button.clicked.connect(self.stop_can_monitor)

        clear_button = QPushButton("Clear window", self)
        clear_button.clicked.connect(self.clear_can_monitor)

        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(stop_button)
        buttons_layout.addWidget(clear_button)

        return buttons_groupbox

    def start_can_monitor(self):
        if not self.can_bus:
            try:
                self.can_bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=125000)
                self.text_edit.append("CAN Monitor started...")
                self.timer.timeout.connect(self.receive_can_frames)
                self.timer.start(3000)
            except Exception as e:
                self.text_edit.append("Error: " + str(e))

    def stop_can_monitor(self):
        if self.can_bus:
            self.can_bus.shutdown()
            self.can_bus = None
            self.timer.stop()
            self.text_edit.append("CAN Monitor stopped.")

    def clear_can_monitor(self):
        if not self.can_bus:
            self.text_edit.clear()

    def receive_can_frames(self):
        if self.can_bus:
            try:
                msg = self.can_bus.recv()
                msg_timestamp = msg.timestamp
                msg_id = msg.arbitration_id
                msg_data = msg.data
                msg_dlc = msg.dlc
                msg_bitrate = msg.bitrate_switch

                self.analyze_can_frame(msg_timestamp, msg_id, msg_data)

            except Exception as exc:
                self.text_edit.append("Error receiving CAN frame: " + str(exc))

    def analyze_can_frame(self, msg_timestamp, msg_id, msg_data):
        self.turn_lights_id = 2
        self.brake_lights_id = 3
        self.beam_lights_id = 4
        self.fuel_tank_id = 6
        self.inside_light_id = 9
        self.driver_window = 13
        self.passenger_window = 12

        msg_data_array = bytearray(msg_data)
        msg_data_list = [byte for byte in msg_data_array]
        print("ID={}, data={}".format(msg_id, msg_data_list))
        self.text_edit.append("Time: , ID={}, Data={}".format(msg_id, msg_data_list))

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
