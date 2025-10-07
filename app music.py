
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
    # เก็บเพลงที่เอาเข้ามา ชั่วคราว
    music_list = []
    file_types = "Music Files (*.mp3 *.wav)"
    # เก็บเพลงเล่นก่อนหลัง
    music_history = []

    # เก็บ profile ที่กำลังใช้
    user_now = None
    # เก็บรหัสผ่านของ profile นี้
    pass_now = None
    # เก็บ folder path
    global_folder_path = None
    # โหมดเริ่มต้น
    start_mode = None

class Control_Data_Store:
    instance_Control_Data_Store = None
    def __new__(cls):
        if cls.instance_Control_Data_Store is None:
            cls.instance_Control_Data_Store = super(Control_Data_Store, cls).__new__(cls)
            # เก็บ username ทั้งหมดใน user and pass store.db
            cls.all_username = []
            # เก็บเพลงทั้งหมดของ profile นั้นๆ
            cls.all_music_profile = []
        return cls.instance_Control_Data_Store
    
    # สร้างฐานข้อมูล profile ที่ผู้ใช้สร้าง
    def store_profile(self):
        self.user = globals_var.user_now
        self.password = globals_var.pass_now
        self.folder_path = globals_var.global_folder_path
        self.mode = globals_var.start_mode

        profile_store = f"{self.user}_profile_store.db"
        # เชื่อฐายข้อมล
        conn = sqlite3.connect(profile_store)
        cursor = conn.cursor()
        # สร้างตาราง profile
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            music_folder_path TEXT,
            mode TEXT)  """)
         # เพิ่มข้อมูล
        cursor.execute("""INSERT INTO profile_info (username, password, music_folder_path, mode)VALUES (?, ?, ?, ?)""", (self.user, self.password, self.folder_path, self.mode))
        conn.commit()
        conn.close()
        return True
        pass

    # เช็คว่ามี username ซ้ำมั้ย
    def check_username(self, make_username, make_password, confirm_password):

        # เช็คว่ารหัสมีอย่างน้อย8ตัวมั้ย
        if len(make_password) < 8:
            QMessageBox.warning(None, "Error", "รหัสผ่านต้องมีอย่างน้อย8ตัว")
            return False
        
        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        # ดึง username ทั้งหมด
        cursor.execute("SELECT username FROM user_and_password")
        rows = cursor.fetchall()
        self.all_username = [row[0] for row in rows]
        if make_username in self.all_username:
           QMessageBox.warning(None, "Error", f"ชื่อ {make_username} ซ้ำ")
           return False
        # ตรวจสอบว่ารหัสผ่านตรงกันมั้ย
        if make_password != confirm_password:
            QMessageBox.warning(None, "Error", "รหัสผ่านไม่ตรงกัน")
            return False
            # เพิ่ม username ในกรณีไม่ซ้ำกัน
        cursor.execute("INSERT INTO user_and_password (username, password) VALUES (?, ?)", (make_username, make_password))
        conn.commit()
        globals_var.user_now = make_username
        globals_var.pass_now = make_password
        conn.close()
        print(globals_var.user_now)
        return True
    
    def login_check_username_and_password(self, username, password):
        # ตัดช่องว่าง
        self.username = username
        self.password = password

        if not self.username:
            QMessageBox.warning(None, "Error", "กรุณาใส่ชื่อ")
            return False

        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        # ดึง username ทั้งหมด
        cursor.execute("SELECT username FROM user_and_password")
        rows = cursor.fetchall()
        self.all_username = [row[0] for row in rows]
        # ดูว่ามี username นี้มั้ย
        # ถ้าไม่มี
        if self.username not in self.all_username:
            QMessageBox.warning(None, "Error", "ไม่มีชื่อนี้")
            conn.close()
            return False
        # ถ้ามี
        if self.username in self.all_username:
            if not self.password:
               QMessageBox.warning(None, "Error", "กรุณาใส่รหัสผ่านด้วย")
               return False
            cursor.execute("SELECT password FROM user_and_password WHERE username = ?", (self.username,))
            #ดึงแถว
            row = cursor.fetchone()
            check_password = row[0]
            if self.password != check_password:
                QMessageBox.warning(None, "Error", "รหัสผ่านไม่ถูกต้อง")
                conn.close()
                return False
            elif self.password == check_password:
                QMessageBox.warning(None, "Event", f"ยินดีตอนรับสู่แอพฟังเพลง {username}")
                globals_var.user_now = self.username
                globals_var.pass_now = self.password
                conn.close()
                print(globals_var.user_now)
                print(globals_var.pass_now)
                return True
    def delete_profile_in_DB(self, username):
        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        # เริ่มลบ profile
        # ลบ username และ password
        cursor.execute("DELETE FROM user_and_password WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True

class control_music:
    instance_control_music = None
    def __new__(cls):
        if cls.instance_control_music is None:
            cls.instance_control_music = super(control_music, cls).__new__(cls)
            # เก็บ path เพลง
            cls.instance_control_music.current_song_path = None
            # เก็บเพลงที่กำลังเล่น
            cls.instance_control_music.music_playing = None 
            cls.instance_control_music.player = QMediaPlayer()
            cls.instance_control_music.audio_output = QAudioOutput()
            # ทำให้ player สามารถควบคุมเพลงได้
            cls.instance_control_music.player.setAudioOutput(cls.instance_control_music.audio_output)
            # ตั้งค่าเสียง
            cls.instance_control_music.audio_output.setVolume(1.0)
            # เก็บ set_volum ของทุกหน้า
            cls.volume_sliders = []
        return cls.instance_control_music
    
    def register_slider(self, set_volum: QSlider):
        self.volume_sliders.append(set_volum)
        # ทำให้ set_volum ของทุกหน้ามีค่าเท่ากันของเสียงจริง
        set_volum.setValue(int(self.audio_output.volume() * 100))
        # เชื่อม set_volum เข้ากับฟังชั่น change_volum
        set_volum.valueChanged.connect(lambda val: self.change_volum(val))

    def change_volum(self, user_scoll_volum):
        self.audio_output.setVolume(float(user_scoll_volum / 100.0))
        # update set_volum ของทุกหน้าให้เท่ากัน
        for slider in self.volume_sliders:
            if slider.value() != user_scoll_volum:
                slider.setValue(user_scoll_volum)

    def check_music_playing(self, song_path):
        if not os.path.exists(song_path):
            # ไม่มีเพลงเล่น current_song_path เป็นเท็จ
            self.music_playing = False
            self.current_song_path = None
            return
        # มีเพลงเล่น current_song_path เป็นจริง
        self.current_song_path = song_path
        self.music_playing = True

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

    def auto_update_music_playing(self, scoll):
        player = self.player

        player.durationChanged.connect(lambda long_music: scoll.setRange(0, long_music))
        player.positionChanged.connect(scoll.setValue)
        scoll.sliderReleased.connect(lambda: player.setPosition(scoll.value()))

    def user_update_music_playing(self, user_scoll):
        self.player.setPosition(user_scoll)

    def setup_slider_control(self):
        scoll = self.scoll_music
        player = self.player

        self.slider_dragging = False

        # เริ่มลาก scoll
        scoll.sliderPressed.connect(lambda: setattr(self, "slider_dragging", True))
        # ปล่อย scoll
        scoll.sliderReleased.connect(lambda: [
        player.setPosition(scoll.value()),  # player กระโดด scoll ที่ user เลือก
        setattr(self, "slider_dragging", False)])

        player.positionChanged.connect(update_slider)
        # อัปเดต scoll_music ตามเพลง เฉพาะเมื่อไม่ได้ลาก
        def update_slider(pos):
            if not self.slider_dragging:
               scoll.setValue(pos)
        # ตั้งค่า range ตามความยาวเพลง
        player.durationChanged.connect(lambda duration: scoll.setRange(0, duration))

    def user_restart_music(self):
        if self.music_playing:
            self.player.stop()
            self.player.play()
            self.music_playing = True

    def user_play_music(self):
        if not self.music_playing:
           self.player.play()
           self.music_playing = True

    def user_stop_music(self):
        if self.music_playing:
           self.player.pause()
           self.music_playing = False

    def user_skip_music(self):
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
        login_check = Control_Data_Store().login_check_username_and_password(username, password)

        if  login_check:
            self.login_to_home()

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
        self.signup_button.clicked.connect(self.create_profile)
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
              # สร้างQGraphicsScene
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

    def create_profile(self):
        make_username = self.make_username.text()
        make_password = self.make_password.text()
        confirm_password = self.confirm_password.text()
        #เรียกใช้ฟังชั่น check_username
        if Control_Data_Store().check_username(make_username, make_password, confirm_password):
            QMessageBox.information(self, "Info", f"สร้างโปรไฟล์แล้ว ชื่อของคุณ {make_username}")
            # ไปหน้า home_page
            self.after_sign_up()

    
    #หลังจากลงทะเบียนแล้วก็ไปหน้าโฮมเลย
    def after_sign_up(self):
        self.stacked_widget.setCurrentIndex(2)

class Home_page(QMainWindow):
    def __init__(self, stacked_widget_home_page):
        super().__init__()
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
        self.list_widget.itemClicked.connect(lambda item: control_music().play_selected_music(item))


        self.go_to_library.clicked.connect(self.home_to_library)
        self.go_to_setting.clicked.connect(self.home_to_setting)
        self.add_music.clicked.connect(lambda: self.add_music_file_to_list (self.list_widget, globals_var.music_list))
        self.edit_profile.clicked.connect(self.open_edit_profile_dialog)


        #เลื่อนเพลงไปข้างหน้าและย้อนกลับ
        self.scoll_music.sliderMoved.connect(lambda user_scoll: control_music().user_update_music_playing(user_scoll))

        # ซิงค์เสียงให้เสียงเท่ากันทุกหน้า
        control_music().register_slider(self.set_volum)
        # ปรับระดับเสียง
        self.set_volum.valueChanged.connect(lambda volum: control_music().change_volum(volum))

        # เรียกใช้ฟังชั่น update_music_playing เพื่ออัปเดทว่าเพลงเล่นถึงไหนแล้ว
        control_music().auto_update_music_playing(self.scoll_music)

        # เริ่มเพลงใหม่ เชื่อม user_restart_music
        self.start_music_again.clicked.connect(control_music().user_restart_music)

        # เล่นเพลงต่อ play_music
        self.play_music.clicked.connect(control_music().user_play_music)

        # หยุดเพลง stop_music
        self.stop_music.clicked.connect(control_music().user_stop_music)

        # ข้ามเพลง skip_music
        self.skip_music.clicked.connect(control_music().user_skip_music)



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
        # เก็บ path โฟร์เดอร์เป็นสากล
        globals_var.global_folder_path = folder_path
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

class library_page(QMainWindow):
    def __init__(self, stacked_widget_library_page):
        super().__init__()
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
        self.list_widget.itemClicked.connect(lambda item: control_music().play_selected_music(item))

        # หา QListWidget ที่ชื่อ show_all_music จาก UI
        self.list_widget = self.findChild(QListWidget, "show_all_music")

        self.go_to_home.clicked.connect(self.library_to_home)
        self.go_to_setting.clicked.connect(self.library_to_setting)
        self.edit_profile.clicked.connect(self.open_edit_profile_dialog)
        

        #เลื่อนเพลงไปข้างหน้าและย้อนกลับ
        self.scoll_music.sliderMoved.connect(lambda user_scoll: control_music().user_update_music_playing(user_scoll))

        # ซิงค์เสียงให้เสียงเท่ากันทุกหน้า
        control_music().register_slider(self.set_volum)
        # ปรับระดับเสียง
        self.set_volum.valueChanged.connect(lambda volum: control_music().change_volum(volum))

        # เรียกใช้ฟังชั่น update_music_playing เพื่ออัปเดทว่าเพลงเล่นถึงไหนแล้ว
        control_music().auto_update_music_playing(self.scoll_music)

        # เริ่มเพลงใหม่ เชื่อม user_restart_music
        self.start_music_again.clicked.connect(control_music().user_restart_music)

        # เล่นเพลงต่อ play_music
        self.play_music.clicked.connect(control_music().user_play_music)

        # หยุดเพลง stop_music
        self.stop_music.clicked.connect(control_music().user_stop_music)

        # ข้ามเพลง skip_music
        self.skip_music.clicked.connect(control_music().user_skip_music)

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
        self.edit_profile.clicked.connect(self.open_edit_profile_dialog)
        self.del_profile.clicked.connect(self.delete_profile)


        #เลื่อนเพลงไปข้างหน้าและย้อนกลับ
        self.scoll_music.sliderMoved.connect(lambda user_scoll: control_music().user_update_music_playing(user_scoll))

        # ซิงค์เสียงให้เสียงเท่ากันทุกหน้า
        control_music().register_slider(self.set_volum)
        # ปรับระดับเสียง
        self.set_volum.valueChanged.connect(lambda volum: control_music().change_volum(volum))

        # เรียกใช้ฟังชั่น update_music_playing เพื่ออัปเดทว่าเพลงเล่นถึงไหนแล้ว
        control_music().auto_update_music_playing(self.scoll_music)

        # เริ่มเพลงใหม่ เชื่อม user_restart_music
        self.start_music_again.clicked.connect(control_music().user_restart_music)

        # เล่นเพลงต่อ play_music
        self.play_music.clicked.connect(control_music().user_play_music)

        # หยุดเพลง stop_music
        self.stop_music.clicked.connect(control_music().user_stop_music)

        # ข้ามเพลง skip_music
        self.skip_music.clicked.connect(control_music().user_skip_music)


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

        # จัดตำแหน่ง del_profile
        self.del_profile.setGeometry(del_music_x, int(del_music_y + 300), 71, 32)

    def delete_profile(self):
        username = globals_var.user_now

        check_del = Control_Data_Store().delete_profile_in_DB(username)
        if check_del:
            self.stacked_widget.setCurrentIndex(0)

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


