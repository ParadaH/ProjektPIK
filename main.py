import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QDialog, QGridLayout, QWidget, \
    QHBoxLayout, QTabWidget, QVBoxLayout, QGroupBox, QLabel, QStyleFactory, QComboBox, QProgressBar, \
    QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint
import can


class CANMonitorApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Analyzer")
        self.setGeometry(300, 150, 600, 400)
        self.text_edit = QTextEdit()
        self.timer = QTimer(self)
        self.can_bus = None

        # Create main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create and apply grid layout in main widget
        main_layout = QGridLayout()
        self.central_widget.setLayout(main_layout)

        # Create text_edit panel (CAN analyzer) and buttons
        text_edit_groupbox = self. create_can_analyzer_groupbox()
        main_layout.addWidget(text_edit_groupbox, 0, 0, 4, 2)

        buttons_groupbox = self.create_button_groupbox()
        main_layout.addWidget(buttons_groupbox, 4, 0, 1, 2)

        car_lights_groupbox = self.create_car_lights_groupbox()
        main_layout.addWidget(car_lights_groupbox, 0, 3, 1, 2)

        car_miniatures_groupbox = self.create_car_miniatures_groupbox()
        main_layout.addWidget(car_miniatures_groupbox,1, 3, 3, 2)

        left_window_groupbox = self.create_left_window_groupbox()
        main_layout.addWidget(left_window_groupbox, 4, 3, 1, 1)

        right_window_groupbox = self.create_right_window_groupbox()
        main_layout.addWidget(right_window_groupbox, 4, 4)



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

    def create_car_lights_groupbox(self):
        car_lights_groupbox = QGroupBox("Car lights")
        car_lights_layout = QHBoxLayout()
        car_lights_groupbox.setLayout(car_lights_layout)

        left_turn_label = QLabel()
        right_turn_label = QLabel()
        main_beam_lights_label = QLabel()
        dipped_beam_lights_label = QLabel()

        # Set path to icon
        left_turn_lights = QPixmap('left_turn_light.png')
        right_turn_lights = QPixmap('right_turn_light.png')
        main_beam_lights = QPixmap('main_beam_lights.png')
        dipped_beam_lights = QPixmap('dipped_beam_lights.png')

        # Load image icon
        right_turn_label.setPixmap(right_turn_lights)
        left_turn_label.setPixmap(left_turn_lights)
        main_beam_lights_label.setPixmap(main_beam_lights)
        dipped_beam_lights_label.setPixmap(dipped_beam_lights)

        car_lights_layout.addWidget(main_beam_lights_label)
        car_lights_layout.addWidget(left_turn_label)
        car_lights_layout.addWidget(right_turn_label)
        car_lights_layout.addWidget(dipped_beam_lights_label)

        return car_lights_groupbox

    def create_car_miniatures_groupbox(self):
        car_miniature_groupbox = QGroupBox("Car")
        car_miniature_layout = QHBoxLayout()
        car_miniature_groupbox.setLayout(car_miniature_layout)

        car_label = QLabel()
        car_icon = QPixmap('porsche.png')
        car_label.setPixmap(car_icon)

        car_miniature_layout.addStretch(1)
        car_miniature_layout.addWidget(car_label)
        car_miniature_layout.addStretch(1)

        return car_miniature_groupbox

    def create_left_window_groupbox(self):
        left_window_groupbox = QGroupBox("Left window")
        left_window_layout = QVBoxLayout()
        left_window_groupbox.setLayout(left_window_layout)

        left_window = QProgressBar()
        left_window.setOrientation(0)
        left_window.setMinimum(0)
        left_window.setMaximum(100)
        left_window.setValue(100)

        left_window_layout.addWidget(left_window)

        return left_window_groupbox

    def create_right_window_groupbox(self):
        right_window_groupbox = QGroupBox("Right window")
        right_window_layout = QVBoxLayout()
        right_window_groupbox.setLayout(right_window_layout)

        right_window = QProgressBar()
        right_window.setOrientation(0)
        right_window.setMinimum(0)
        right_window.setMaximum(100)
        right_window.setValue(33)

        right_window_layout.addWidget(right_window)

        return right_window_groupbox

#    def blink_light(self):


    def start_can_monitor(self):
        if not self.can_bus:
            try:
                self.can_bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
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
