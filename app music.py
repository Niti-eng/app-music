
import sqlite3
import sys, random
import os
import queue
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QStackedWidget, QMessageBox, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QGroupBox
from PyQt6.QtCore import Qt, QUrl, QTimer, QRect
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QColor, QImage, QPainter, QRadialGradient, QIcon

class globals_var:
    music_list = []
    file_types = "Music Files (*.mp3 *.wav)"

    user_now = None

class Control_Data_Store:
    def __init__(self, db_filename_1="user_and_pass_store.db"):
        self.db_filename_1 = db_filename_1
        self.conn = None
        self.cursor = None
        self.connect_db()

    # ฟังก์ชันเชื่อมฐานข้อมูล
    def connect_db(self):
        self.conn = sqlite3.connect(self.db_filename_1)
        self.cursor = self.conn.cursor()
        self.create_table()

    # ฟังก์ชันสร้าง table ถ้ายังไม่มี
    def create_table_user_and_pass_store(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_and_password (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    # ฟังก์ชันบันทึก user
    def save_user_and_pass_store(self, username, password):
        try:
            self.cursor.execute("""
                INSERT INTO user_and_password (username, password)
                VALUES (?, ?)
            """, (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    # ฟังก์ชันอ่าน user ทั้งหมด
    def get_all_user_and_pass_store(self):
        self.cursor.execute("SELECT username, password FROM user_and_password")
        return self.cursor.fetchall()

    # ฟังก์ชันปิดการเชื่อมต่อ DB
    def close_db_user_and_pass_store(self):
        if self.conn:
            self.conn.close()
        

class control_music:
    # เก็บ path เพลง
    current_song_path = None
    # เก็บเพลงที่กำลังเล่น
    music_playing = None 
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    # ตั้งค่าเสียง
    audio_output.setVolume(50)

    @classmethod
    def check_music_playing(cls, song_path):
        if not os.path.exists(song_path):
            # ไม่มีเพลงเล่น current_song_path เป็นเท็จ
            cls.music_playing = False
            cls.current_song_path = None
            return
        # มีเพลงเล่น current_song_path เป็นจริง
        cls.current_song_path = song_path
        cls.music_playing = True

    def play_selected_music(self, item):
        song_path = None
        for path in globals_var.music_list:
            if os.path.basename(path) == item.text():
               song_path = path
               break
        if not song_path:
           QMessageBox.warning(self, "Error", "ไม่พบไฟล์เพลง")
           self.music_playing = False
           return
        self.check_music_playing(song_path)
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
           self.player.stop()
        self.player.setSource(QUrl.fromLocalFile(self.current_song_path))
        self.player.play()

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
        #จัดเก็บความกว้างและยาวของกล่องกลุ่มข้อความ
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

#image_type = [".png", ".jpg", ".jpeg"]

class Home_page(QMainWindow, control_music):
    def __init__(self, stacked_widget_home_page):
        super().__init__()
        # เรียก class control_music
        control_music.__init__(self)
        uic.loadUi("music Home start.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_home_page

        # เก็บใน centralWidget
        self.Right_bar.setParent(self.centralWidget())
        self.down_bar.setParent(self.centralWidget())
        self.Media.setParent(self.centralWidget())
        self.name_song.setParent(self.centralWidget())
        self.play_music_box.setParent(self.centralWidget())
        self.artis_name_song.setParent(self.centralWidget())
        self.out_profile.setParent(self.centralWidget())

        # หา object music_you_add
        self.list_widget = self.findChild(QListWidget, "music_you_add")
        # เล่นเพลงเมื่อกด music_you_add
        self.list_widget.itemClicked.connect(self.play_selected_music)


        #self.go_to_home.clicked.connect(self.)
        self.go_to_library.clicked.connect(self.home_to_library)
        self.go_to_setting.clicked.connect(self.home_to_setting)
        self.add_music.clicked.connect(lambda: self.add_music_file_to_list (self.list_widget, globals_var.music_list))
        self.edit_profile.clicked.connect(self.open_edit_profile_dialog)

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

        #จัดตำแหน่งdown_bar
        down_bar_h = 100
        down_bar_y = self.height() - down_bar_h
        self.down_bar.setGeometry(0, down_bar_y, int(self.width()), down_bar_h)

        #จัดตำแหน่งRight_bar
        bar_h = int(self.height() * 0.85)
        Right_bar = int(self.height() * 0.85)
        Right_bar_x = int(self.width() * 1.0 - 470)
        self.Right_bar.setGeometry(Right_bar_x, 70, 470, bar_h)

        # จัดตำแหน่งMedia
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)

        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 91, 41)

        # จัดตำแหน่ง artis_name_song
        self.artis_name_song.setGeometry(int(show_music_x + 250), 470, 91, 41)

        # จัดตำแหน่ง play_music_box
        play_music_box_w = int(self.width() - 661) // 2
        self.play_music_box.setGeometry(int(play_music_box_w), int(down_bar_y + 5), 661, 91)

        # จัดตำแหน่ง add_music
        add_music_x = int(self.width() - 61) // 7
        self.add_music.setGeometry( add_music_x, 80, 61, 32)

        # จัดตำแหน่ง lastly_add
        self.lastly_add.setGeometry( int(add_music_x - 35), 150, 61, 32)

        # จัดตำแหน่ง music_you_add
        music_you_add_w = int(self.width() * 0.35 - 25)
        self.music_you_add.setGeometry( int(add_music_x - 35), 175, music_you_add_w, 51)

        # จัดตำแหน่ง edit_profile
        margin_right = 100
        margin_top = 10
        button_w = 50
        button_h = 50
        edit_profile_x = self.width() - button_w - margin_right
        edit_profile_y = margin_top
        self.edit_profile.setGeometry( edit_profile_x, edit_profile_y, button_w, button_h)
        # ทำให้ปุ่มเป็นวงกลม
        self.edit_profile.setStyleSheet(f"""
        QPushButton {{
        border-radius: {button_w // 2}px;  /*ครึ่งหนึ่งของความกว้าง*/
        background-color: #e74c3c;         /*สีพื้นหลัง*/
        border: 0.5px solid #85c1e9;        /*ขอบ*/
        }}
           """)

        # จัดตำแหน่ง out_profile
        self.out_profile.setGeometry( int(edit_profile_x + 50), int(edit_profile_y + 15), 101, 16)

        # จัดตำแหน่ง text_flie_type
        self.text_flie_type.setGeometry( int(add_music_x + 80), 80, 181, 16)

        # จัดตำแหน่ง text_se_foder
        self.text_se_foder.setGeometry( int(add_music_x + 80), 100, 181, 16)

        # จัดตำแหน่ง set_volum
        set_volum_w = int(self.width() * 0.08)
        self.set_volum.setGeometry(int(play_music_box_w + 665), int(down_bar_y + 20), set_volum_w, 25)

        # จัดตำแหน่ง text_set_volum
        self.text_set_volum.setGeometry(int(play_music_box_w + 665), int(down_bar_y + 40), set_volum_w, 25)

    def add_music_file_to_list(self, list_widget, music_list):
        # ให้ผู้ใช้เลือกโฟลเดอร์
        folder_path = QFileDialog.getExistingDirectory(None, "เลือกโฟลเดอร์")
        if not folder_path:
           return  # ถ้าไม่เลือกอะไรเลย
        dup_music = []  # เก็บชื่อเพลงซ้ำ
        # กำหนดนามสกุล
        allow_music = [".mp3", ".wav"]
        # วนไฟล์ทั้งหมดในโฟลเดอร์
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            ext = os.path.splitext(file_name)[1].lower()
            # ตรวจสอบว่ามีนามสกุลที่เรากำหนดหรือไม่
            if ext not in allow_music:
               continue
            # ตรวจสอบว่าเพลงซ้ำใน list_widget มั้ย
            exists = any(list_widget.item(i).text() == file_name for i in range(list_widget.count()))
            if exists:
              dup_music.append(file_name)
            else:
              # เพิ่มเพลงลง QListWidget และ list ของเรา
              music_list.append(file_path)
              list_widget.insertItem(0, file_name)
        # ถ้ามีเพลงซ้ำ แสดงหน้าต่างแจ้งเตือน
        if dup_music:
           show_dup_music = "\n".join(dup_music)
           QMessageBox.warning(self,
            "เพลงซ้ำ",
            f"เพลงที่จะไม่ถูกเพิ่ม:\n{show_dup_music}")

    def open_edit_profile_dialog(self):
        open_edit = QDialog(self)
        uic.loadUi("sign up edit profile.ui", open_edit)
        open_edit.exec()

    def home_to_library(self):
        library.update_music_list()
        self.stacked_widget.setCurrentIndex(3)

    def home_to_setting(self):
       self.stacked_widget.setCurrentIndex(4)

class library_page(QMainWindow, control_music):
    def __init__(self, stacked_widget_library_page):
        super().__init__()
        # เรียก class control_music
        control_music.__init__(self)
        uic.loadUi("music library.ui", self)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_library_page
        
        # เก็บใน centralWidget
        self.Right_bar.setParent(self.centralWidget())
        self.down_bar.setParent(self.centralWidget())
        self.Media.setParent(self.centralWidget())
        self.name_song.setParent(self.centralWidget())
        self.play_music_box.setParent(self.centralWidget())
        self.artis_name_song.setParent(self.centralWidget())
        self.edit_profile.setParent(self.centralWidget())
        self.out_profile.setParent(self.centralWidget())

        # หา object show_all_music
        self.list_widget = self.findChild(QListWidget, "show_all_music")
        # เล่นเพลงเมื่อกด show_all_music
        self.list_widget.itemClicked.connect(self.play_selected_music)

        # หา QListWidget ที่ชื่อ show_all_music จาก UI
        self.list_widget = self.findChild(QListWidget, "show_all_music")

        self.go_to_home.clicked.connect(self.library_to_home)
        #self.go_to_library.clicked.connect(self.)
        self.go_to_setting.clicked.connect(self.library_to_setting)
        self.edit_profile.clicked.connect(self.open_edit_profile_dialog)

        self.bar_app.setFixedHeight(70)

    def update_music_list(self):
        for song_path in globals_var.music_list:
            song_name = os.path.basename(song_path)
            # ตรวจสอบว่ามีใน QListWidget หรือยัง
            exists = any(self.list_widget.item(i).text() == song_name for i in range(self.list_widget.count()))
            if not exists:
               self.list_widget.addItem(song_name)

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

        #จัดตำแหน่งdown_bar
        down_bar_h = 100
        down_bar_y = self.height() - down_bar_h
        self.down_bar.setGeometry(0, down_bar_y, int(self.width()), down_bar_h)

        #จัดตำแหน่งRight_bar
        bar_h = int(self.height() * 0.85)
        Right_bar_x = int(self.width() * 1.0 - 470)
        self.Right_bar.setGeometry(Right_bar_x, 70, 470, bar_h)

        # จัดตำแหน่งMedia
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)

        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 91, 41)

        # จัดตำแหน่ง artis_name_song
        self.artis_name_song.setGeometry(int(show_music_x + 250), 470, 91, 41)

        # จัดตำแหน่ง play_music_box
        play_music_box_w = int(self.width() - 661) // 2
        self.play_music_box.setGeometry(int(play_music_box_w), int(down_bar_y + 5), 661, 91)

        # จัดตำแหน่ง t_show_all_music
        t_show_all_music_x = int(self.width() * 0.1)
        self.t_show_all_music.setGeometry(t_show_all_music_x, 90, 71, 21)

        # จัดตำแหน่ง show_all_music
        show_all_music_w = int(self.width() * 1 - 650)
        show_all_music_h = int(self.height() * 1 - 300)
        self.show_all_music.setGeometry(t_show_all_music_x, 120, show_all_music_w, show_all_music_h)

         # จัดตำแหน่ง edit_profile
        margin_right = 100
        margin_top = 10
        button_w = 50
        button_h = 50
        edit_profile_x = self.width() - button_w - margin_right
        edit_profile_y = margin_top
        self.edit_profile.setGeometry( edit_profile_x, edit_profile_y, button_w, button_h)
        # ทำให้ปุ่มเป็นวงกลม
        self.edit_profile.setStyleSheet(f"""
        QPushButton {{
        border-radius: {button_w // 2}px;  /*ครึ่งหนึ่งของความกว้าง*/
        background-color: #e74c3c;         /*สีพื้นหลัง*/
        border: 0.5px solid #85c1e9;        /*ขอบ*/
        }}
           """)
        
        # จัดตำแหน่ง out_profile
        self.out_profile.setGeometry( int(edit_profile_x + 50), int(edit_profile_y + 15), 101, 16)

        # จัดตำแหน่ง set_volum
        set_volum_w = int(self.width() * 0.08)
        self.set_volum.setGeometry(int(play_music_box_w + 665), int(down_bar_y + 20), set_volum_w, 25)

        # จัดตำแหน่ง text_set_volum
        self.text_set_volum.setGeometry(int(play_music_box_w + 665), int(down_bar_y + 40), set_volum_w, 25)

    def open_edit_profile_dialog(self):
        open_edit = QDialog(self)
        uic.loadUi("sign up edit profile.ui", open_edit)
        open_edit.exec()

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
        self.Right_bar.setParent(self.centralWidget())
        self.down_bar.setParent(self.centralWidget())
        self.Media.setParent(self.centralWidget())
        self.name_song.setParent(self.centralWidget())
        self.play_music_box.setParent(self.centralWidget())
        self.artis_name_song.setParent(self.centralWidget())
        self.edit_profile.setParent(self.centralWidget())
        self.out_profile.setParent(self.centralWidget())

        self.go_to_home.clicked.connect(self.setting_to_home)
        self.go_to_library.clicked.connect(self.setting_to_library)
        #self.go_to_setting.clicked.connect(self.)
        self.edit_profile.clicked.connect(self.open_edit_profile_dialog)

        self.bar_app.setFixedHeight(70)

    #กำหนดตำแหน่งต่างๆในหน้า
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bar_app.setGeometry(0, 0, self.width(), 70)

        #จัดตำแหน่งdown_bar
        down_bar_h = 100
        down_bar_y = self.height() - down_bar_h
        self.down_bar.setGeometry(0, down_bar_y, int(self.width()), down_bar_h)

        #จัดตำแหน่งRight_bar
        bar_h = int(self.height() * 0.85)
        Right_bar_x = int(self.width() * 1.0 - 470)
        self.Right_bar.setGeometry(Right_bar_x, 70, 470, bar_h)

        # จัดตำแหน่งMedia
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)

        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 91, 41)

        # จัดตำแหน่ง artis_name_song
        self.artis_name_song.setGeometry(int(show_music_x + 250), 470, 91, 41)

        # จัดตำแหน่ง play_music_box
        play_music_box_w = int(self.width() - 661) // 2
        self.play_music_box.setGeometry(int(play_music_box_w), int(down_bar_y + 5), 661, 91)

        #เก็บค่าความกว้างยาวของเมนู
        manu_box_w = self.manu_box.width()
        manu_box_h = self.manu_box.height()
        #กำหนดให้อยู่ตรงกลางแนวนอนและความห่างจากขอบบน
        x = (self.width() - manu_box_w) // 2
        y = 5
        #แสดงเมนู
        self.manu_box.setGeometry(x, y, manu_box_w, manu_box_h)

         # จัดตำแหน่ง edit_profile
        margin_right = 100
        margin_top = 10
        button_w = 50
        button_h = 50
        edit_profile_x = self.width() - button_w - margin_right
        edit_profile_y = margin_top
        self.edit_profile.setGeometry( edit_profile_x, edit_profile_y, button_w, button_h)
        # ทำให้ปุ่มเป็นวงกลม
        self.edit_profile.setStyleSheet(f"""
        QPushButton {{
        border-radius: {button_w // 2}px;  /*ครึ่งหนึ่งของความกว้าง*/
        background-color: #e74c3c;         /*สีพื้นหลัง*/
        border: 0.5px solid #85c1e9;        /*ขอบ*/
        }}
           """)
        
        # จัดตำแหน่ง out_profile
        self.out_profile.setGeometry( int(edit_profile_x + 50), int(edit_profile_y + 15), 101, 16)

        # จัดตำแหน่ง set_volum
        set_volum_w = int(self.width() * 0.08)
        self.set_volum.setGeometry(int(play_music_box_w + 665), int(down_bar_y + 20), set_volum_w, 25)

        # จัดตำแหน่ง text_set_volum
        self.text_set_volum.setGeometry(int(play_music_box_w + 665), int(down_bar_y + 40), set_volum_w, 25)

        # จัดตำแหน่ง del_music_y
        del_music_x = int(self.width() * 0.1 )
        del_music_y = int(self.height() * 0.15 )
        self.del_music.setGeometry(del_music_x, del_music_y, 61, 32)
        
        # จัดตำแหน่ง del_music_all
        self.del_music_all.setGeometry(int(del_music_x + 150), del_music_y, 91, 32)

        # จัดตำแหน่ง text_mode
        self.text_mode.setGeometry(del_music_x, int(del_music_y + 100), 99, 20)

        # จัดตำแหน่ง mode_hot
        self.mode_hot.setGeometry(del_music_x, int(del_music_y + 130), 99, 20)

        # จัดตำแหน่ง mode_night
        self.mode_night.setGeometry(del_music_x, int(del_music_y + 160), 99, 20)

    def open_edit_profile_dialog(self):
        open_edit = QDialog(self)
        uic.loadUi("sign up edit profile.ui", open_edit)
        open_edit.exec()
    
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


