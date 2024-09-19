import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QGridLayout, QWidget, \
    QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QProgressBar, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer
import can


class CANMonitorApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAN Analyzer")
        self.setGeometry(300, 150, 600, 400)
        self.text_edit = QTextEdit()
        self.timer = QTimer(self)
        self.turn_lights = QTimer(self)
        self.can_bus = None
        self.driver_window = QProgressBar()
        self.passenger_window = QProgressBar()
        self.fuel_tank = QProgressBar()

        # Create main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create and apply grid layout in main widget
        main_layout = QGridLayout()
        self.central_widget.setLayout(main_layout)

        # Create text_edit panel (CAN analyzer) and buttons
        text_edit_groupbox = self. create_can_analyzer_groupbox()
        main_layout.addWidget(text_edit_groupbox, 0, 0, 4, 3)

        buttons_groupbox = self.create_button_groupbox()
        main_layout.addWidget(buttons_groupbox, 4, 0, 1, 3)

        car_lights_groupbox = self.create_car_lights_groupbox()
        main_layout.addWidget(car_lights_groupbox, 0, 3, 1, 2)

        car_miniature_groupbox = self.create_car_miniature_groupbox()
        main_layout.addWidget(car_miniature_groupbox,1, 3, 3, 2)

        driver_window_groupbox = self.create_driver_window_groupbox()
        main_layout.addWidget(driver_window_groupbox, 4, 3, 1, 1)

        passenger_window_groupbox = self.create_passenger_window_groupbox()
        main_layout.addWidget(passenger_window_groupbox, 4, 4, 1, 1)

        fuel_tank_groupbox = self.create_fuel_tank_indicator_groupbox()
        main_layout.addWidget(fuel_tank_groupbox, 0, 5, 5, 1)

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

    def create_test_buttons_groupbox(self):
        buttons_groupbox = QGroupBox("Przyciski testowe")
        buttons_layout = QHBoxLayout()
        buttons_groupbox.setLayout(buttons_layout)

        test1 = QPushButton("Set driver window to 50%", self)
        test2 = QPushButton("Set driver window to 75%", self)
        test3 = QPushButton("Turn on main beam lights", self)
        test4 = QPushButton("Turn off main beam lights", self)

        value1 = int('80', 16)
        value2 = int('C0', 16)
        test1.clicked.connect(lambda: self.update_progress_bar(0, value1))
        test2.clicked.connect(lambda: self.update_progress_bar(0, value2))
        test3.clicked.connect(lambda: self.update_lights_status(0, 3))
        test4.clicked.connect(lambda: self.update_lights_status(0, 1))
        buttons_layout.addWidget(test1)
        buttons_layout.addWidget(test2)
        buttons_layout.addWidget(test3)
        buttons_layout.addWidget(test4)

        return buttons_groupbox

    def create_car_lights_groupbox(self):
        car_lights_groupbox = QGroupBox("Car lights")
        car_lights_layout = QHBoxLayout()
        car_lights_groupbox.setLayout(car_lights_layout)

        self.left_turn_label = QLabel()
        self.right_turn_label = QLabel()
        self.main_beam_lights_label = QLabel()
        self.dipped_beam_lights_label = QLabel()
        self.stop_light_label = QLabel()

        # Set path to icon
        self.left_turn_lights = QPixmap('left_turn_light.png')
        self.right_turn_lights = QPixmap('right_turn_light.png')
        self.main_beam_lights = QPixmap('main_beam_lights.png')
        self.dipped_beam_lights = QPixmap('dipped_beam_lights.png')
        self.stop_light = QPixmap('swiatlo stop.png')

        # Load image icon
        self.right_turn_label.setPixmap(self.right_turn_lights)
        self.left_turn_label.setPixmap(self.left_turn_lights)
        self.main_beam_lights_label.setPixmap(self.main_beam_lights)
        self.dipped_beam_lights_label.setPixmap(self.dipped_beam_lights)
        self.stop_light_label.setPixmap(self.stop_light)

        self.opacity_effects = []
        self.opacities = []

        labels = [self.left_turn_label, self.right_turn_label, self.main_beam_lights_label,
                  self.dipped_beam_lights_label, self.stop_light_label]

        for label in labels:
            opacity_effect = QGraphicsOpacityEffect()
            label.setGraphicsEffect(opacity_effect)
            opacity_effect.setOpacity(0.2)

            self.opacity_effects.append(opacity_effect)
            self.opacities.append(0.2)

        car_lights_layout.addWidget(self.main_beam_lights_label)
        car_lights_layout.addWidget(self.left_turn_label)
        car_lights_layout.addWidget(self.right_turn_label)
        car_lights_layout.addWidget(self.dipped_beam_lights_label)
        car_lights_layout.addWidget(self.stop_light_label)

        return car_lights_groupbox

    def create_car_miniature_groupbox(self):
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

    def create_driver_window_groupbox(self):
        driver_window_groupbox = QGroupBox("Driver's window")
        driver_window_layout = QVBoxLayout()
        driver_window_groupbox.setLayout(driver_window_layout)

        self.driver_window.setOrientation(0)
        self.driver_window.setMinimum(0)
        self.driver_window.setMaximum(200)
        self.driver_window.setValue(200)

        driver_window_layout.addWidget(self.driver_window)

        return driver_window_groupbox

    def create_passenger_window_groupbox(self):
        passenger_window_groupbox = QGroupBox("Passenger's window")
        passenger_window_layout = QVBoxLayout()
        passenger_window_groupbox.setLayout(passenger_window_layout)

        self.passenger_window.setOrientation(0)
        self.passenger_window.setMinimum(0)
        self.passenger_window.setMaximum(200)
        self.passenger_window.setValue(200)

        passenger_window_layout.addWidget(self.passenger_window)

        return passenger_window_groupbox

    def create_fuel_tank_indicator_groupbox(self):
        fuel_tank_indicator_groupbox = QGroupBox("Petrol Tank Indicator")
        fuel_tank_layout = QVBoxLayout()
        fuel_tank_indicator_groupbox.setLayout(fuel_tank_layout)

        self.fuel_tank.setOrientation(0)
        self.fuel_tank.setMinimum(0)
        self.fuel_tank.setMaximum(255)
        self.fuel_tank.setValue(255)

        fuel_tank_layout.addWidget(self.fuel_tank)

        return fuel_tank_indicator_groupbox

    def update_progress_bar(self, progressbar_id, value):
        print(progressbar_id, value)
        if progressbar_id == 0:
            value = int(value[1])
            self.driver_window.setValue(value)
        if progressbar_id == 1:
            value = int(value[1])
            self.passenger_window.setValue(value)
        if progressbar_id == 2:
            value = int(value[0])
            self.fuel_tank.setValue(value)

    def update_lights_status(self, lights_id, value):
        if lights_id == 0:
            if value == 3:
                self.opacity_effects[2].setOpacity(1.0) # main_beam_lights ON
            if value == 1:
                self.opacity_effects[2].setOpacity(0.2) # main_beam_lights OFF
        if lights_id == 1:
            if value == 1:
                self.opacity_effects[3].setOpacity(1.0) # dipped_beam_lights ON
            if value == 0:
                self.opacity_effects[3].setOpacity(0.2) # dipped_beam_lights OFF
        if lights_id == 2:
            if value == 1:
                self.opacity_effects[1].setOpacity(1.0)  # right_turn_lights ON
            if value == 0:
                self.opacity_effects[1].setOpacity(0.2)  # right_turn_lights OFF
        if lights_id == 3:
            if value == 1:
                self.opacity_effects[0].setOpacity(1.0) # left_turn_lights ON
            if value == 0:
                self.opacity_effects[0].setOpacity(0.2) # left_turn_lights OFF
        if lights_id == 4:
            if value == 1:
                self.opacity_effects[0].setOpacity(1.0)
            if value == 0:
                self.opacity_effects[0].setOpacity(0.2)

    def start_can_monitor(self):
        if not self.can_bus:
            try:
                self.can_bus = can.interface.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000)
                self.text_edit.append("CAN Monitor started...")
                self.timer.timeout.connect(self.receive_can_frames)
                self.timer.start(250)
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
        self.driver_window_id = 12
        self.passenger_window_id = 13

        msg_data_array = bytearray(msg_data)
        msg_data_list = [byte for byte in msg_data_array]
        # print("ID={}, data={}".format(msg_id, msg_data_list))
        self.text_edit.append("Time: {}, ID={}, Data={}".format(msg_timestamp, msg_id, msg_data_list))

        if msg_id == self.turn_lights_id:
            # Turn lights
            if msg_data_list == [37, 64, 128]:
                self.update_lights_status(2, 1)
            if msg_data_list == [32, 64, 128]:
                self.update_lights_status(2, 0)
            if msg_data_list == [58, 64, 128]:
                self.update_lights_status(3, 1)
            if msg_data_list == [48, 64, 128]:
                self.update_lights_status(3, 0)

            # Emergency lights
            if msg_data_list == [31, 64, 128]:
                self.update_lights_status(2, 1)
                self.update_lights_status(3, 1)
            if msg_data_list == [0, 64, 128]:
                self.update_lights_status(2, 0)
                self.update_lights_status(3, 0)

        if msg_id == self.fuel_tank_id:
            self.update_progress_bar(2, msg_data_list)

        if msg_id == self.driver_window_id:
            self.update_progress_bar(0, msg_data_list)

        if msg_id == self.passenger_window:
            print('Test okna pasazera. Dane:', msg_data_list)
            passenger_window_level = int(f'msg_data_list[0]', 16)
            print(passenger_window_level)
            self.update_progress_bar(1, passenger_window_level)

        if msg_id == self.beam_lights_id:
            if msg_data_list[0] == 1:
                self.update_lights_status(1, 1) # dipped_beam_lights ON
                self.update_lights_status(0, 1) # main_beam_lights OFF

            if msg_data_list[0] == 0:
                self.update_lights_status(1, 0) # dipped_beam_lights OFF

            if msg_data_list[0] == 3:
                self.update_lights_status(0, 3) # main_beam_lights ON

        if msg_id == self.brake_lights_id:
            if msg_data_list[0] == 1:
                self.update_lights_status(4, 1)
            if msg_data_list[0] == 0:
                self.update_lights_status(4, 0)

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
