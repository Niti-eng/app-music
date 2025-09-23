
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QStackedWidget, QMessageBox, QMainWindow
from PyQt6.QtCore import Qt, QUrl, QTimer, QRect
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6 import uic

class Control_Data_Store:
    pass

#แอปฟังเพลงของผมเอง
class login_App_music(QDialog):
    def __init__(self, stacked_widget_login_page):
        super().__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        uic.loadUi("music .ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_login_page
        #ตั้งค่าปุ่มlogin กับ make_profile
        self.loginbutton.clicked.connect(self.loginfunction)
        self.make_profile.clicked.connect(self.Go_Create_profile)
        self.loginbutton.clicked.connect(self.login_to_home)
        #ตั้งค่าขนาดหน้าจอ
        self.resize(1920, 1080)
        self.setMinimumSize(800, 600)

        QTimer.singleShot(0, self.set_ui_login)

    def set_ui_login(self):

        windows_width = self.width()
        windows_height = self.height()

        #จัดตำแหน่งข้อความคำว่า ล็อคอิน
        Login = self.login_box
        #จัดเก็บความกว้างและยาวของกล่องกลุ่มข้อมความ
        login_box_w = Login.width()
        login_box_h = Login.height()
        #จัดตำแหน่งโดยให้อยู่ตรงกลางหน้าจอในขนาดที่เราใช้อยู่
        x_login_box = (windows_width - login_box_w) // 2
        y_login_box = (windows_height - login_box_h) // 2
        #นำตำแหน่งที่คำนวณไปใช้
        Login.setGeometry(QRect(x_login_box, y_login_box, login_box_w, login_box_h))
        #เอาเส้นออก
        self.login_box.setStyleSheet("QGroupBox { border: none; }")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_ui_login()
        
    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        QMessageBox.information(self, "Login info", f"Username: {username}\nPassword: {password}")
        print("name", username, "pass", password)

    def Go_Create_profile(self):
        #แสดงหน้า sign up
        self.stacked_widget.setCurrentIndex(1)

    def login_to_home(self):
        #แสดงหน้า Home_page
        self.stacked_widget.setCurrentIndex(2)

class Create_profile(QDialog):
    def __init__(self, stacked_widget_Create_profile):
        super().__init__()
        uic.loadUi("music sign up.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_Create_profile  
        
        self.signup_button.clicked.connect(self.create_function)
        self.back_to_login.clicked.connect(self.go_back_to_login)

    def set_ui_sign_up(self):

        windows_width = self.width()
        windows_height = self.height()

        sign_up = self.sign_up_box
        #จัดเก็บความกว้างและยาวของกล่องกลุ่มข้อมความ
        sign_up_box_w = sign_up.width()
        sign_up_box_h = sign_up.height()
        #จัดตำแหน่งโดยให้อยู่ตรงกลางหน้าจอในขนาดที่เราใช้อยู่
        x_sign_up_box = (windows_width - sign_up_box_w) // 2
        y_sign_up_box = (windows_height - sign_up_box_h) // 2
        y_sign_up_box = y_sign_up_box - int(windows_height * 0.20)
        #นำตำแหน่งที่คำนวณไปใช้
        sign_up.setGeometry(QRect(x_sign_up_box, y_sign_up_box, sign_up_box_w, sign_up_box_h))
        #เอาเส้นออก
        self.sign_up_box.setStyleSheet("QGroupBox { border: none; }")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_ui_sign_up()

    def go_back_to_login(self):
        self.stacked_widget.setCurrentIndex(0) 

    def create_function(self):
        make_username = self.make_username.text()
        if self.make_password.text() == self.confirm_password.text():
            make_password = self.make_password.text()
            print("sucess profile", make_username, "and password", make_password)
        else:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            print("wrong password")


class Home_page(QMainWindow):
    def __init__(self, stacked_widget_home_page):
        super().__init__()
        uic.loadUi("music Home start.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_home_page
        #self.go_to_home.clicked.connect(self.)
        self.go_to_library.clicked.connect(self.home_to_library)
        self.go_to_setting.clicked.connect(self.home_to_setting)

        
        self.bar_app.setFixedHeight(70)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bar_app.setGeometry(0, 0, self.width(), 70)

    def home_to_library(self):
        self.stacked_widget.setCurrentIndex(3)

    def home_to_setting(self):
       self.stacked_widget.setCurrentIndex(4)

class library_page(QMainWindow):
    def __init__(self, stacked_widget_library_page):
        super().__init__()
        uic.loadUi("music library.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_library_page
        self.go_to_home.clicked.connect(self.library_to_home)
        #self.go_to_library.clicked.connect(self.)
        self.go_to_setting.clicked.connect(self.library_to_setting)

    def library_to_home(self):
        self.stacked_widget.setCurrentIndex(2)

    def library_to_setting(self):
         self.stacked_widget.setCurrentIndex(4)

class setting_page(QMainWindow):
    def __init__(self, stacked_widget_setting_page):
        super().__init__()
        uic.loadUi("music setting.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_setting_page
        self.go_to_home.clicked.connect(self.setting_to_home)
        self.go_to_library.clicked.connect(self.setting_to_library)
        #self.go_to_setting.clicked.connect(self.)

    def setting_to_home(self):
        self.stacked_widget.setCurrentIndex(2)

    def setting_to_library(self):
        self.stacked_widget.setCurrentIndex(3)


app = QApplication(sys.argv)
#สร้างตัวแปรเก็บสแต็ก
stacked_widget = QStackedWidget()

#stacked_widget index 0 LOGIN
login_page = login_App_music(stacked_widget)
stacked_widget.addWidget(login_page)

#stacked_widget index 1 SIGN UP
sign_up = Create_profile(stacked_widget)
stacked_widget.addWidget(sign_up)

#stacked_widget index 2 HOME
Home = Home_page(stacked_widget)
stacked_widget.addWidget(Home)

#stacked_widget index 3 LIBRARY
library = library_page(stacked_widget)
stacked_widget.addWidget(library)

#stacked_widget index 4 SETTING
setting = setting_page(stacked_widget)
stacked_widget.addWidget(setting)

stacked_widget.show()
sys.exit(app.exec())


