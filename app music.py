
import sys, random
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QStackedWidget, QMessageBox, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QGroupBox
from PyQt6.QtCore import Qt, QUrl, QTimer, QRect
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QColor, QImage, QPainter, QRadialGradient

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

        #ปุ่มตรวจสอบรหัสผ่าน
        self.signup_button.clicked.connect(self.create_function)
        #ปุ่มเลือกภาพโปรไฟล์
        self.add_picture_pro.clicked.connect(self.add_picture_to_profile)
        #ปุ่มกลับหน้าล็อคอิน 
        self.back_to_login.clicked.connect(self.go_back_to_login)
        #เก็บpathรูปภาพ
        self.profile_image_path = None

    def set_ui_sign_up(self):

        windows_width = self.width()
        windows_height = self.height()

        sign_up = self.sign_up_box
        #จัดเก็บความกว้างและยาวของกล่องกลุ่มข้อความ
        sign_up_box_w = sign_up.width()
        sign_up_box_h = sign_up.height()
        #จัดตำแหน่งโดยให้อยู่ตรงกลางหน้าจอในขนาดที่เราใช้อยู่
        x_sign_up_box = (windows_width - sign_up_box_w) // 2
        y_sign_up_box = (windows_height - sign_up_box_h) // 2 - int(windows_height * 0.20)
        #ป้องกันค่าy_sign_up_boxติดลบ
        y_sign_up_box = max(0, y_sign_up_box) 
        #นำตำแหน่งที่คำนวณไปใช้
        sign_up.setGeometry(QRect(x_sign_up_box, y_sign_up_box, sign_up_box_w, sign_up_box_h))
        #เอาเส้นออก
        self.sign_up_box.setStyleSheet("QGroupBox { border: none; }")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_ui_sign_up()

    def go_back_to_login(self):
        self.stacked_widget.setCurrentIndex(0)

    def add_picture_to_profile(self):
        file_name, _ = QFileDialog.getOpenFileName (
            self,
            "Select Profile Picture",
            "",
            "Images (*.png *.jpg *.jpeg)"   )
        if file_name:
           self.profile_image_path = file_name
        self.open_edit_profile_ui()

    def open_edit_profile_ui(self):
        edit_dialog = QDialog(self)
        uic.loadUi("sign up edit profile.ui", edit_dialog)

        if self.profile_image_path:
           #หาQGraphicsView จาก ui ก่อน
           graphics_view = edit_dialog.findChild(QGraphicsView, "edit_picture_profile")
           slider = edit_dialog.findChild(QSlider, "L_D_pickture")

           if graphics_view:
              # ร้างQGraphicsScene
              scene = QGraphicsScene()
              #โหลดรูป
              original_pixmap = QPixmap(self.profile_image_path)
              #แปลงเป็น item
              item = QGraphicsPixmapItem(original_pixmap)
              scene.addItem(item)
              #ตั้งsceneให้กับQGraphicsView
              graphics_view.setScene(scene)
              graphics_view.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)

        edit_pic_box = edit_dialog.findChild(QGroupBox, "sign_up_edit_pic_Box")
        if edit_pic_box:
           dialog_width = 900
           dialog_height = 600
           box_width = edit_pic_box.width()
           box_height = edit_pic_box.height()
           x = (dialog_width - box_width) // 2
           y = (dialog_height - box_height) // 2
           edit_pic_box.setGeometry(QRect(x, y, box_width, box_height))

        edit_dialog.setFixedSize(900, 600)
        edit_dialog.exec()

    def create_function(self):
        make_username = self.make_username.text()
        if self.make_password.text() == self.confirm_password.text():
            make_password = self.make_password.text()
            print("sucess profile", make_username, "and password", make_password)
            
            #ไปdef after_sign_up
            self.after_sign_up()
        else:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            print("wrong password")
    
    #หลังจากลงทะเบียนแล้วก็ไปหน้าโฮมเลย
    def after_sign_up(self):
        self.stacked_widget.setCurrentIndex(2)

image_exts = [".png", ".jpg", ".jpeg"]
video_exts = [".mp4", ".mov"]
class MediaViewer_play_music(QWidget):
    def __init__(self, Media: QWidget):
        super().__init__(Media)  # ให้ parent เป็น QWidget ที่ชื่อ Media
        self.setGeometry(0, 0, Media.width(), Media.height())

        # stacked widget
        from PyQt6.QtWidgets import QStackedLayout
        self.stack = QStackedLayout(self)
        self.setLayout(self.stack)

        # widget สำหรับรูปภาพ
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.stack.addWidget(self.image_label)

        # widget สำหรับวิดีโอ
        self.video_widget = QVideoWidget()
        self.stack.addWidget(self.video_widget)

        # player สำหรับวิดีโอ
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        # ปิดเสียงวิดีโอ
        self.audio_output.setVolume(0)
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

    def load_file(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in image_exts:
            self.player.stop()
            pixmap = QPixmap(path)
            self.image_label.setPixmap(pixmap)
            self.stack.setCurrentWidget(self.image_label)
        elif ext in video_exts:
            self.stack.setCurrentWidget(self.video_widget)
            self.player.setSource(QUrl.fromLocalFile(path))
            self.player.play()
        else:
            print("ไฟล์ไม่รองรับ")

class Home_page(QMainWindow):
    def __init__(self, stacked_widget_home_page):
        super().__init__()
        uic.loadUi("music Home start.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_home_page
        # เก็บใน centralWidget
        self.Left_bar.setParent(self.centralWidget())
        self.Right_bar.setParent(self.centralWidget())
        self.down_bar.setParent(self.centralWidget())
        self.Media.setParent(self.centralWidget())
        self.name_song.setParent(self.centralWidget())

        #self.go_to_home.clicked.connect(self.)
        self.go_to_library.clicked.connect(self.home_to_library)
        self.go_to_setting.clicked.connect(self.home_to_setting)

        self.bar_app.setFixedHeight(70)

    #กำหนดตำแหน่งต่างๆในหน้า
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bar_app.setGeometry(0, 0, self.width(), 70)

        #เก็บค่าความกว้างยาวของเมนู
        manu_box_w = self.manu_box.width()
        manu_box_h = self.manu_box.height()
        #กำหนดให้อยู่ตรงกลางแนวนอนและความห่างจากขอบบน
        x = (self.width() - manu_box_w) // 2
        y = 5
        #แสดงเมนู
        self.manu_box.setGeometry(x, y, manu_box_w, manu_box_h)

        #จัดตำแหน่งLeft_bar
        Left_bar_h = int(self.height() * 0.85)
        self.Left_bar.setGeometry(0, 70, 65, Left_bar_h)

        #จัดตำแหน่งdown_bar
        down_bar_h = 100
        down_bar_y = self.height() - down_bar_h
        self.down_bar.setGeometry(0, down_bar_y, int(self.width()), down_bar_h)

        #จัดตำแหน่งRight_bar
        Right_bar = int(self.height() * 0.85)
        Right_bar_x = int(self.width() * 1.0 - 470)
        self.Right_bar.setGeometry(Right_bar_x, 70, 470, Left_bar_h)

        # จัดตำแหน่งMedia
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)

        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 91, 41)


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
        # เก็บใน centralWidget
        self.Left_bar.setParent(self.centralWidget())
        self.Right_bar.setParent(self.centralWidget())
        self.down_bar.setParent(self.centralWidget())
        self.Media.setParent(self.centralWidget())
        self.name_song.setParent(self.centralWidget())

        self.go_to_home.clicked.connect(self.library_to_home)
        #self.go_to_library.clicked.connect(self.)
        self.go_to_setting.clicked.connect(self.library_to_setting)

        self.bar_app.setFixedHeight(70)

    #กำหนดตำแหน่งต่างๆในหน้า
    def resizeEvent(self, event):
        super().resizeEvent(event)
          #เก็บค่าความกว้างยาวของเมนู
        manu_box_w = self.manu_box.width()
        manu_box_h = self.manu_box.height()
        #กำหนดให้อยู่ตรงกลางแนวนอนและความห่างจากขอบบน
        x = (self.width() - manu_box_w) // 2
        y = 5
        #แสดงเมนู
        self.manu_box.setGeometry(x, y, manu_box_w, manu_box_h)

        self.bar_app.setGeometry(0, 0, self.width(), 70)

        #จัดตำแหน่งLeft_bar
        Left_bar_h = int(self.height() * 0.85)
        self.Left_bar.setGeometry(0, 70, 65, Left_bar_h)

        #จัดตำแหน่งdown_bar
        down_bar_h = 100
        down_bar_y = self.height() - down_bar_h
        self.down_bar.setGeometry(0, down_bar_y, int(self.width()), down_bar_h)

        #จัดตำแหน่งRight_bar
        Right_bar = int(self.height() * 0.85)
        Right_bar_x = int(self.width() * 1.0 - 470)
        self.Right_bar.setGeometry(Right_bar_x, 70, 470, Left_bar_h)

        # จัดตำแหน่งMedia
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)

        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 91, 41)

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
        # เก็บใน centralWidget
        self.Left_bar.setParent(self.centralWidget())
        self.Right_bar.setParent(self.centralWidget())
        self.down_bar.setParent(self.centralWidget())
        self.Media.setParent(self.centralWidget())
        self.name_song.setParent(self.centralWidget())

        self.go_to_home.clicked.connect(self.setting_to_home)
        self.go_to_library.clicked.connect(self.setting_to_library)
        #self.go_to_setting.clicked.connect(self.)

        self.bar_app.setFixedHeight(70)

    #กำหนดตำแหน่งต่างๆในหน้า
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bar_app.setGeometry(0, 0, self.width(), 70)

        #จัดตำแหน่งLeft_bar
        Left_bar_h = int(self.height() * 0.85)
        self.Left_bar.setGeometry(0, 70, 65, Left_bar_h)

        #จัดตำแหน่งdown_bar
        down_bar_h = 100
        down_bar_y = self.height() - down_bar_h
        self.down_bar.setGeometry(0, down_bar_y, int(self.width()), down_bar_h)

        #จัดตำแหน่งRight_bar
        Right_bar = int(self.height() * 0.85)
        Right_bar_x = int(self.width() * 1.0 - 470)
        self.Right_bar.setGeometry(Right_bar_x, 70, 470, Left_bar_h)

        # จัดตำแหน่งMedia
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)

        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 91, 41)

        #เก็บค่าความกว้างยาวของเมนู
        manu_box_w = self.manu_box.width()
        manu_box_h = self.manu_box.height()
        #กำหนดให้อยู่ตรงกลางแนวนอนและความห่างจากขอบบน
        x = (self.width() - manu_box_w) // 2
        y = 5
        #แสดงเมนู
        self.manu_box.setGeometry(x, y, manu_box_w, manu_box_h)

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


