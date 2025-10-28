
import sqlite3
import sys, random, time
import os

from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1
from mutagen.easyid3 import EasyID3

from rx.subject import BehaviorSubject
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QStackedWidget, QMessageBox, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QGroupBox, QGraphicsRectItem
from PyQt6.QtCore import Qt, QUrl, QTimer, QRect, QRectF, pyqtSignal, QSize
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QColor, QImage, QPainter, QRadialGradient, QIcon, QPen, QFont, QBitmap, QBrush

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
    # ตัวแปรที่ใช้แสดง ภาพ proflie ขณะใช้
    show_profile = None
    # เก็บ folder path เพลง
    global_folder_path = None

    # ตัวแปรใช้เก็บตำแหน่งเพลง เพื่อให้รู้ว่ากำลังเล่นเพลงที่ตำแหน่งไหน
    index_music = None

    # เก็บเวลากดปุ่มครั้งแรก
    first_press = 0
    # กำหนดเวลาสำหรับ double_click
    double_click = 0.3

    # ตัวแปรสำหรับเช็คค่า index_music เมื่อมีการเปลี่ยนแปลง
    check_index_music = BehaviorSubject(0)
    # อัปเดท name_song เมื่อค่ามีการเปลี่ยน
    def update_name_song(check_index_music, name_song):
        if check_index_music == globals_var.index_music:
           # สร้างตัวแปรสำหรับปรับขนาดของ name_song
           size = QFont()
           # แสดงชื่อเพลง
           size.setPointSize(20)
           name_song.setFont(size)
           # กำหนดข้อความ name_song โดยเอามาแค่ชื่อเพลง
           name_song.setText(os.path.splitext(globals_var.music_history[globals_var.index_music])[0])

    # ตัวแปรเก็บค่าชื่อของศิลปิน
    artist_name = None
    # อัปเดท artis_name_song เมื่อค่ามีการเปลี่ยน
    def update_artis_name_song(check_index_music, artis_name_song):
        if check_index_music == globals_var.index_music:
           # สร้างตัวแปรสำหรับปรับขนาดของ name_song
           size = QFont()
           # แสดงชื่อศิลปิน
           size.setPointSize(15)
           artis_name_song.setFont(size)
           # ใช้สำหรับเข้าอ่านเมต้าดาต้าของเพลงนั้นๆ
           path_music = os.path.join(globals_var.global_folder_path ,globals_var.music_history[globals_var.index_music])
           print(path_music)
           # ตรวจว่าเป็นไฟล์ mp3 หรือ wav ก่อนอ่านเมต้าดาต้า
           if path_music.lower().endswith(".mp3"):
               # เก็บเมต้าดาต้าของเพลง
               meta_music = EasyID3(path_music)
               # เก็บชื่อศิลปิน
               artist = meta_music.get("artist", ["Unknown Artist"])[0]
               print(f"artist is {artist}")
               # แสดงชื่อศิลปิน
               size.setPointSize(15)
               artis_name_song.setFont(size)
               # แสดงชื่อศิลปิน
               artis_name_song.setText(artist)
           elif path_music.lower().endswith(".wav"):
               meta_music = File(path_music)
               artist = meta_music.get("artist", ["Unknow Artist"])[0]
               size.setPointSize(15)
               artis_name_song.setFont(size)
               # แสดงชื่อศิลปิน
               artis_name_song.setText(artist)

    # อัปเดท Media(ปกเพลง) เมื่อค่ามีการเปลี่ยน
    def update_Media(check_index_music, Media):
        if check_index_music == globals_var.index_music:
            # ใช้สำหรับเข้าอ่านเมต้าดาต้าของเพลงนั้นๆ
           path_music = os.path.join(globals_var.global_folder_path ,globals_var.music_history[globals_var.index_music])
           print(path_music)

           # ตรวจว่าเป็นไฟล์ mp3 หรือ wav ก่อนอ่านเมต้าดาต้า
           if path_music.lower().endswith(".mp3"):
              # เก็บข้อมูลเมต้าของเพลง
              meta_music = ID3(path_music)
              apic_picture = meta_music.getall("APIC")
              # แสดงภาพถ้ามี
              if apic_picture:
                 # เก็บภาพเป็น ไบ
                 show_picture_music = apic_picture[0].data

                 # ลบ layout เก่าออกถ้ามี
                 if Media.layout() is not None:
                    QWidget().setLayout(Media.layout())

                 # โหลดภาพจาก show_picture_music
                 pixmap = QPixmap()
                 pixmap.loadFromData(show_picture_music)
                 pixma_sc = pixmap.scaled(Media.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                 # แสดงภาพใน Media
                 lebel = QLabel(Media)
                 # จัดตรงกลาง
                 lebel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                 lebel.setPixmap(pixma_sc)
                 layout = QVBoxLayout(Media)
                 layout.addWidget(lebel)
           elif path_music.lower().endswith(".wav"):
               return True

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
    
    def update_path_folder():
        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        # อัปข้อมูลของ path folder ใน db
        cursor.execute("UPDATE user_and_password SET folder_path = ? WHERE username = ?", (globals_var.global_folder_path, globals_var.user_now))
        conn.commit()
        conn.close()

    def read_path_folder():
        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        cursor.execute("SELECT folder_path FROM user_and_password WHERE username = ?", (globals_var.user_now,))
        # ดึง folder_path มาเก็บ
        folder_path_keep = cursor.fetchone()
        # แปลงข้อมูลเป็น str
        if folder_path_keep:
            result = folder_path_keep[0]
            # เก็บ path folder
            globals_var.global_folder_path = result
            print(globals_var.global_folder_path)
        conn.close()

    def add_music_in_DB(self, music_list):
        conn = sqlite3.connect(f"{globals_var.user_now} music path.db")
        cursor = conn.cursor()

        # ตรวจสอบว่ามีข้อมูลในตาราง music_path มั้ย
        cursor.execute("SELECT COUNT(*) FROM music_path")
        count = cursor.fetchone()[0]

        if count == 0:
           for path in music_list:
               cursor.execute("INSERT INTO music_path (music_path) VALUES (?)", (path,))
        
        elif count != 0 :
           # เก็บ path เพลง ใหม่ที่ถูกเพิ่มเข้ามา
           new_path = []
           # ดึง path เพลงออกมาตรวจ
           for path in music_list:
               cursor.execute("SELECT 1 FROM music_path WHERE music_path = ?", (path,))
               # เพิ่ม path เพลงที่ยังไม่มี ลงใน new_path
               if not cursor.fetchall():
                  new_path.append((path,))
            # เพิ่ม new_path ลง DB
           if new_path:
              cursor.executemany("INSERT INTO music_path (music_path) VALUES (?)", new_path)
        conn.commit()
        conn.close()

    def delete_some_music(self):
        show_de = QDialog()
        uic.loadUi("delete some music .ui", show_de)
        show_de.setFixedSize(866, 165) 
        # อ่าน name_music_de เมื่อผู้ใช้กดปุ่ม summit_de_music ไปที่ฟังชั่น delete_music
        show_de.summit_de_music.clicked.connect(lambda: self.delete_music(show_de.name_music_de.text()))
        # แสดงหน้าต่าง
        show_de.exec()
    # ลบเพลง
    def delete_music(self, name_music):
        # ดูว่าผู้ใช้ได้ส่งชื่อเพลงมามั้ย
        if name_music == "":
            QMessageBox.warning(None, "Error", "ใส่ชื่อเพลงด้วย")
            return False
        conn = sqlite3.connect(f"{globals_var.user_now} music path.db")
        cursor = conn.cursor()

        # ใช้ตรวจว่าเจอเพลงมั้ย
        found = False
        # หาชื่อเพลงที่ตรงกัน
        for path_music in globals_var.music_list:
            # เก็บชื่อเพลง เอามาแค่ชื่อไม่มีนาสกุล
            song_name = os.path.splitext(os.path.basename(path_music))[0]
            # เก็บชื่อเพลงแบบมีนามสกุล สำหรับลบการแสดงเพลงในหน้า บ้าน และ ห้องสมุด
            name_de = os.path.basename(path_music)
            # เช็คว่าชื่อเพลงตรงกับที่กรอกมั้ย
            if song_name == name_music:
                print(path_music)
                print(name_de)
                # ลบ path ใน music_list
                globals_var.music_list.remove(path_music)
                # เอาชื่อเพลงที่แสดงออก
                Home.delete_name_music(name_de)
                library.delete_name_music(name_de)
                # ลบ path ของเพลงนั้น
                cursor.execute("DELETE FROM music_path WHERE music_path = ?",(path_music,))
                conn.commit()
                QMessageBox.warning(None, "suces", f"ลบ{song_name}แล้ว")
                conn.close()
                return True
        if not found:
            QMessageBox.warning(None, "Error", f"ไม่เจอเพลงชื่อ {name_music}")
            conn.close()
            return False
        conn.close()

    def delete_all_music(self):
        conn = sqlite3.connect(f"{globals_var.user_now} music path.db")
        cursor = conn.cursor()
        # ลบข้อมูลทั้งหมดในตาราง
        cursor.execute("DELETE FROM music_path")
        conn.commit()
        conn.close()
        globals_var.music_list = []
    
    def add_path_music_in_music_list_when_start(self, user_now):
        conn = sqlite3.connect(f"{user_now} music path.db")
        cursor = conn.cursor()
        # ดึง path เพลงทั้งหมด
        cursor.execute("SELECT * FROM music_path")
        rows = cursor.fetchall()
        # แปลงเก็บใน music_list
        for row in rows:
            globals_var.music_list.append(row[1])
        conn.close()
    
    def make_music_path_store(self, make_username):
        conn_ = sqlite3.connect(f"{make_username} music path.db")
        cursor = conn_.cursor()
        # สร้างตารางเก็บ path เพลง
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS music_path (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        music_path TEXT NOT NULL ) """)
        conn_.commit()
        conn_.close()

    # เช็คว่ามี username ซ้ำมั้ย
    def check_username(self, make_username, make_password, confirm_password):
        
        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        # ดึง username ทั้งหมด
        cursor.execute("SELECT username FROM user_and_password")
        rows = cursor.fetchall()
        self.all_username = [row[0] for row in rows]
        if make_username in self.all_username:
           QMessageBox.warning(None, "Error", f"ชื่อ {make_username} ซ้ำ")
           conn.close()
           return False
        elif make_username == "":
            QMessageBox.warning(None, "Error", "ยังไม่ได้ใส่ชื่อ")
            conn.close()
            return False
        # เช็คว่ารหัสมีอย่างน้อย8ตัวมั้ย
        if len(make_password) < 8:
            QMessageBox.warning(None, "Error", "รหัสผ่านต้องมีอย่างน้อย8ตัว")
            conn.close()
            return False
        # ตรวจสอบว่ารหัสผ่านตรงกันมั้ย
        if make_password != confirm_password:
            QMessageBox.warning(None, "Error", "รหัสผ่านไม่ตรงกัน")
            conn.close()
            return False
        cursor.execute("INSERT INTO user_and_password (username, password) VALUES (?, ?)",(make_username, make_password))
        conn.commit()
        conn.close()
        globals_var.user_now = make_username
        globals_var.pass_now = make_password
        print(globals_var.user_now)
        print(globals_var.pass_now)
        self.make_music_path_store(make_username)
        return True
    
    def login_check_username_and_password(self, username, password):
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
               conn.close()
               return False
            # ดึงรหัสมาตรวจดู
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

                # เรียก path folder
                Control_Data_Store.read_path_folder()
                print(globals_var.user_now)
                print(globals_var.pass_now)
                conn.close()

                # เอา path เพลงไปเก็บใน music_list
                if not globals_var.music_list:
                   self.add_path_music_in_music_list_when_start(globals_var.user_now)
                return True

    def delete_profile_in_DB(self, username):
        conn = sqlite3.connect("user and pass store.db")
        cursor = conn.cursor()
        # เริ่มลบ profile
        # ลบ username และ password
        cursor.execute("DELETE FROM user_and_password WHERE username = ?", (username,))
        conn.commit()
        # ถ้ามีการเชื่อต่อฐานข้อมูลให้ปิด
        if conn:
            conn.close()
        # ลบไฟล์ db ของ profile นั้น
        if os.path.exists(f"{username} music path.db"):
           os.remove(f"{username} music path.db")
           return True
        else:
            return False

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
            # ไม่มีเพลงเล่น music_playing เป็นเท็จ
            self.music_playing = False
            self.current_song_path = None
            return
        # มีเพลงเล่น music_playing เป็นจริง
        self.current_song_path = song_path
        self.music_playing = True

    def play_selected_music(self, item):
        #ล้างประวัติเพลงเมื่อผู้ใช้กดเลือเพลงใหม่
        globals_var.music_history = []
        song_path = None
        #หาเพลง
        for path in globals_var.music_list:
            if os.path.basename(path) == item.text():
               song_path = path
               break
        self.check_music_playing(song_path)
        #เก็บประวัติเพลงไว้ใน music_history
        globals_var.music_history.append(os.path.basename(self.current_song_path))
        print(f"play {globals_var.music_history}")

        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
           self.player.stop()
        self.player.setSource(QUrl.fromLocalFile(self.current_song_path))
        self.player.play()
        self.music_playing = True
        self.player.mediaStatusChanged.connect(self.check_music_end)
        globals_var.index_music = 0
        # ส่งค่า check_index_music ไปอัตโนมัติเมื่อค่าเปลี่ยน
        globals_var.check_index_music.on_next(globals_var.index_music)
        print(f"index_music {globals_var.index_music}")
        print("play_selected_music")

    def check_music_end(self, status):
        # ทำงานเฉพาะเมื่อเพลงจบ
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
           self.random_play()
           print("check_music_end")

    def random_play(self):
        song_path = random.choice(globals_var.music_list)
        
        self.current_song_path = song_path
        self.player.setSource(QUrl.fromLocalFile(self.current_song_path))
        self.player.play()
        globals_var.music_history.append(os.path.basename(self.current_song_path))
        print(f"random {globals_var.music_history}")
        # ขยับตำแหน่ง index_music
        globals_var.index_music = globals_var.index_music + 1
        # ส่งค่า check_index_music ไปอัตโนมัติเมื่อค่าเปลี่ยน
        globals_var.check_index_music.on_next(globals_var.index_music)
        print(f"index_music {globals_var.index_music}")
        print("random_play")

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

    # เริ่มเพลงใหม่
    def user_restart_music(self):
        if globals_var.index_music is None:
            return False
        now = time.time()
        if now - globals_var.first_press < globals_var.double_click:
            if globals_var.index_music <= 0:
               return False
            # เก็บเวลากดครั้งแรก
            globals_var.index_music = globals_var.index_music - 1
            song_path = None
            for path in globals_var.music_list:
                if os.path.basename(path) == globals_var.music_history[globals_var.index_music]:
                   song_path = path
                   break
            self.player.setSource(QUrl.fromLocalFile(song_path))
            self.player.play()
            print(f"index_music {globals_var.index_music}")
            # ส่งค่า check_index_music ไปอัตโนมัติเมื่อค่าเปลี่ยน
            globals_var.check_index_music.on_next(globals_var.index_music)
       
        elif now - globals_var.first_press > globals_var.double_click:
            if self.music_playing:
               self.player.stop()
               self.player.play()
               self.music_playing = True
        globals_var.first_press = now

    # เล่นเพลงต่อ
    def user_play_music(self):
        if not self.music_playing:
           self.player.play()
           self.music_playing = True

    # หยุดเพลง
    def user_stop_music(self):
        if self.music_playing:
           self.player.pause()
           self.music_playing = False

    # ข้ามเพลง
    def user_skip_music(self):
        if globals_var.index_music is None:
            return False
        if globals_var.index_music + 1 < len(globals_var.music_history):
            globals_var.index_music = globals_var.index_music + 1
            self.player.setSource(QUrl.fromLocalFile(globals_var.music_history[globals_var.index_music]))
            self.player.play()
            print(f"index_music {globals_var.index_music}")
        else:
            self.random_play()


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
        self.setMinimumSize(900, 700)
        #เก็บสแต็ก
        self.stacked_widget = stacked_widget_Create_profile  

        #ปุ่มสร้างโปรไฟล์
        self.signup_button.clicked.connect(self.create_profile)
        #ปุ่มกลับหน้าล็อคอิน 
        self.back_to_login.clicked.connect(self.go_back_to_login)

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
        self.make_username.clear()
        self.make_password.clear()
        self.confirm_password.clear()
        self.stacked_widget.setCurrentIndex(0)

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
        self.show_user.setParent(self.centralWidget())

        # หา object music_you_add
        self.list_widget = self.findChild(QListWidget, "music_you_add")
        # เล่นเพลงเมื่อกด music_you_add
        self.list_widget.itemClicked.connect(lambda item: control_music().play_selected_music(item))


        self.go_to_library.clicked.connect(self.home_to_library)
        self.go_to_setting.clicked.connect(self.home_to_setting)
        self.add_music.clicked.connect(lambda: self.add_music_file_to_list (self.list_widget, globals_var.music_list))

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

        # ออกจากโปรไฟล์ out_profile
        self.out_profile.clicked.connect(self.home_to_loging)

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

        # จัดตำแหน่ง Media
        # ดึง geometry จริงของ Right_bar
        Right_bar_geo = self.Right_bar.geometry()
        space = 50
        show_music_x = Right_bar_geo.x() + space
        self.Media.setGeometry(int(show_music_x + 12), 80, 350, 350)
        # แสดงภาพปกเพลงของ Media
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_Media(check_index_music, self.Media))

        # สร้างตัวแปรสำหรับปรับขนาดของ name_song artis_name_song
        size = QFont()
        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 350, 41)
        if globals_var.index_music is None:
           # ปรับขนาดตัวหนังสือ
           size.setPointSize(15)
           self.name_song.setFont(size)
           # กำหนดข้อความ name_song
           self.name_song.setText("Name song")
        # เปลี่ยนชื่อเพลงทุกครั้งที่ตัวแปร check_index_music เปลี่ยน
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_name_song(check_index_music, self.name_song))
         
        # จัดตำแหน่ง artis_name_song
        self.artis_name_song.setGeometry(int(show_music_x + 12), 490, 350, 41)
        if globals_var.index_music is None:
           # ปรับขนาดตัวหนังสือ
           size.setPointSize(14)
           self.artis_name_song.setFont(size)
           # กำหนดข้อความ artis_name_song
           self.artis_name_song.setText("artist")
        # เปลี่ยนชื่อศิลปินทุกครั้งที่ตัวแปร check_index_music เปลี่ยน
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_artis_name_song(check_index_music, self.artis_name_song))

        # จัดตำแหน่ง show_user
        show_user_top = 10
        show_user_w = 50
        show_user_right = 100
        show_user_y = show_user_top
        show_user_x = self.width() - show_user_w - show_user_right
        self.show_user.setGeometry(int(show_user_x - 30), int(show_user_y + 15), 71, 16)
        size.setPointSize(14)
        # กำหนดข้อความ show_user
        self.show_user.setText(globals_var.user_now)
      
        # จัดตำแหน่ง play_music_box
        play_music_box_w = int(self.width() - 521) // 2
        self.play_music_box.setGeometry(int(play_music_box_w), int(down_bar_y + 5), 521, 91)

        # จัดตำแหน่ง add_music
        add_music_x = int(self.width() - 61) // 7
        self.add_music.setGeometry( add_music_x, 80, 61, 32)

        # จัดตำแหน่ง lastly_add
        self.lastly_add.setGeometry( int(add_music_x - 35), 150, 61, 32)

        # จัดตำแหน่ง music_you_add
        music_you_add_w = int(self.width() * 0.35 - 25)
        self.music_you_add.setGeometry( int(add_music_x - 35), 175, music_you_add_w, 400)

        # จัดตำแหน่ง out_profile
        margin_top = 10
        button_w = 50
        margin_right = 100
        out_profile_y = margin_top
        out_profile_x = self.width() - button_w - margin_right
        self.out_profile.setGeometry( int(out_profile_x + 50), int(out_profile_y + 10), 100, 32)

        # จัดตำแหน่ง text_flie_type
        self.text_flie_type.setGeometry( int(add_music_x + 80), 80, 181, 16)

        # จัดตำแหน่ง text_se_foder
        self.text_se_foder.setGeometry( int(add_music_x + 80), 100, 181, 16)

        # จัดตำแหน่ง set_volum
        set_volum_w = int(self.width() * 0.08)
        self.set_volum.setGeometry(int(play_music_box_w + 521), int(down_bar_y + 20), set_volum_w, 25)

        # จัดตำแหน่ง text_set_volum
        self.text_set_volum.setGeometry(int(play_music_box_w + 521), int(down_bar_y + 40), set_volum_w, 25)

    # ลบ item ใน show_all_music เมื่อ music_list ว่าง
    def de_item_when_music_list_space(self):
        if not globals_var.music_list:
            self.list_widget.clear()
            return True

    def add_music_file_to_list(self, list_widget, music_list):
        # ให้ผู้ใช้เลือกโฟลเดอร์
        folder_path = QFileDialog.getExistingDirectory(None, "เลือกโฟลเดอร์")
        if folder_path:
           # เก็บ path โฟร์เดอร์เป็นสากล
           globals_var.global_folder_path = folder_path
           print(f"foder path is {globals_var.global_folder_path}")
           Control_Data_Store.update_path_folder()
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
            # ตรวจสอบว่าเพลงซ้ำใน music_you_add มั้ย
            exists = any(list_widget.item(i).text() == file_name for i in range(list_widget.count())) or any(os.path.basename(path) == file_name for path in music_list)
            if exists:
              dup_music.append(file_name)
            else:
              # เพิ่มเพลงลง music_you_add และ list ของเรา
              music_list.append(file_path)
              list_widget.insertItem(0, file_name)

        # ถ้ามีเพลงซ้ำ แสดงหน้าต่างแจ้งเตือน
        if dup_music:
           show_dup_music = "\n".join(dup_music)
           QMessageBox.warning(self,
            "เพลงซ้ำ",
            f"เพลงที่จะไม่ถูกเพิ่ม:\n{show_dup_music}")
        # เอา path เพลงไปเก็บใน db
        Control_Data_Store().add_music_in_DB(music_list)
    
    def delete_name_music(self, name_de):
        # เก็บชื่อ item ที่ต้องการจะลบ
        music_want_de = self.list_widget.findItems(name_de, Qt.MatchFlag.MatchExactly)
        # หา item ที่ชื่อตรงกัน แล้วลบ
        for item in music_want_de:
            where_item = self.list_widget.row(item)
            self.list_widget.takeItem(where_item)

    def home_to_library(self):
        library.update_music_list()
        self.stacked_widget.setCurrentIndex(3)

    def home_to_setting(self):
       self.stacked_widget.setCurrentIndex(4)

    def home_to_loging(self):
        globals_var.user_now = None
        globals_var.pass_now = None
        print(f" user is {globals_var.user_now}")
        print(f" pass is {globals_var.pass_now}")
        self.stacked_widget.setCurrentIndex(0)

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
        self.out_profile.setParent(self.centralWidget())
        self.show_user.setParent(self.centralWidget())

        # หา object show_all_music
        self.list_widget = self.findChild(QListWidget, "show_all_music")
        # เล่นเพลงเมื่อกด show_all_music
        self.list_widget.itemClicked.connect(lambda item: control_music().play_selected_music(item))

        # หา QListWidget ที่ชื่อ show_all_music จาก UI
        self.list_widget = self.findChild(QListWidget, "show_all_music")

        self.go_to_home.clicked.connect(self.library_to_home)
        self.go_to_setting.clicked.connect(self.library_to_setting)

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

        # ออกจากโปรไฟล์ out_profile
        self.out_profile.clicked.connect(self.library_to_loging)

        self.bar_app.setFixedHeight(70)

    def update_music_list(self):
        # ลบ item ใน show_all_music เมื่อ music_list ว่าง
        if not globals_var.music_list:
            self.list_widget.clear()
        for song_path in globals_var.music_list:
            song_name = os.path.basename(song_path)
            # ตรวจสอบว่ามี song_name ใน list_widget หรือยัง (ป้องกันการเพิ่มเพลงซ้ำ)
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
        # แสดงภาพปกเพลงของ Media
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_Media(check_index_music, self.Media))

        # สร้างตัวแปรสำหรับปรับขนาดของ name_song artis_name_song
        size = QFont()
        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 350, 41)
        if globals_var.index_music is None:
        # ปรับขนาดตัวหนังสือ
           size.setPointSize(15)
           self.name_song.setFont(size)
           # กำหนดข้อความ name_song
           self.name_song.setText("Name song")
        # เปลี่ยนชื่อเพลงทุกครั้งที่ตัวแปร check_index_music เปลี่ยน
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_name_song(check_index_music, self.name_song))

        # จัดตำแหน่ง artis_name_song
        self.artis_name_song.setGeometry(int(show_music_x + 12), 490, 350, 41)
        if globals_var.index_music is None:
           # ปรับขนาดตัวหนังสือ
           size.setPointSize(14)
           self.artis_name_song.setFont(size)
           # กำหนดข้อความ artis_name_song
           self.artis_name_song.setText("artist")
        # เปลี่ยนชื่อศิลปินทุกครั้งที่ตัวแปร check_index_music เปลี่ยน
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_artis_name_song(check_index_music, self.artis_name_song))

        # จัดตำแหน่ง show_user
        show_user_top = 10
        show_user_w = 50
        show_user_right = 100
        show_user_y = show_user_top
        show_user_x = self.width() - show_user_w - show_user_right
        self.show_user.setGeometry(int(show_user_x - 30), int(show_user_y + 15), 71, 16)
        size.setPointSize(14)
        # กำหนดข้อความ show_user
        self.show_user.setText(globals_var.user_now)

        # จัดตำแหน่ง play_music_box
        play_music_box_w = int(self.width() - 521) // 2
        self.play_music_box.setGeometry(int(play_music_box_w), int(down_bar_y + 5), 521, 91)

        # จัดตำแหน่ง t_show_all_music
        t_show_all_music_x = int(self.width() * 0.1)
        self.t_show_all_music.setGeometry(t_show_all_music_x, 90, 71, 21)

        # จัดตำแหน่ง show_all_music
        show_all_music_w = int(self.width() * 1 - 650)
        show_all_music_h = int(self.height() * 1 - 300)
        self.show_all_music.setGeometry(t_show_all_music_x, 120, show_all_music_w, show_all_music_h)
        
        # จัดตำแหน่ง out_profile
        margin_top = 10
        button_w = 50
        margin_right = 100
        out_profile_y = margin_top
        out_profile_x = self.width() - button_w - margin_right
        self.out_profile.setGeometry( int(out_profile_x + 50), int(out_profile_y + 10), 100, 32)

        # จัดตำแหน่ง set_volum
        set_volum_w = int(self.width() * 0.08)
        self.set_volum.setGeometry(int(play_music_box_w + 521), int(down_bar_y + 20), set_volum_w, 25)

        # จัดตำแหน่ง text_set_volum
        self.text_set_volum.setGeometry(int(play_music_box_w + 521), int(down_bar_y + 40), set_volum_w, 25)

    def delete_name_music(self, name_de):
        # เก็บชื่อ item ที่ต้องการจะลบ
        music_want_de = self.list_widget.findItems(name_de, Qt.MatchFlag.MatchExactly)
        # หา item ที่ชื่อตรงกัน แล้วลบ
        for item in music_want_de:
            where_item = self.list_widget.row(item)
            self.list_widget.takeItem(where_item)

    def library_to_home(self):
        Home.de_item_when_music_list_space()
        self.stacked_widget.setCurrentIndex(2)

    def library_to_setting(self):
        self.stacked_widget.setCurrentIndex(4)

    def library_to_loging(self):
        globals_var.user_now = None
        globals_var.pass_now = None
        print(f" user is {globals_var.user_now}")
        print(f" pass is {globals_var.pass_now}")
        self.stacked_widget.setCurrentIndex(0)

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
        self.out_profile.setParent(self.centralWidget())
        self.show_user.setParent(self.centralWidget())

        self.go_to_home.clicked.connect(self.setting_to_home)
        self.go_to_library.clicked.connect(self.setting_to_library)
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

        # ออกจากโปรไฟล์ out_profile
        self.out_profile.clicked.connect(self.setting_to_loging)

        # เชื่อมปุ่ม del_music_all
        self.del_music_all.clicked.connect(Control_Data_Store().delete_all_music)

        # เชื่อมปุ่ม del_music
        self.del_music.clicked.connect(Control_Data_Store().delete_some_music)

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
        # แสดงภาพปกเพลงของ Media
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_Media(check_index_music, self.Media))

        # สร้างตัวแปรสำหรับปรับขนาดของ name_song artis_name_song
        size = QFont()
        # จัดตำแหน่ง name_song
        self.name_song.setGeometry(int(show_music_x + 12), 450, 350, 41)
        if globals_var.index_music is None:
           # ปรับขนาดตัวหนังสือ
           size.setPointSize(15)
           self.name_song.setFont(size)
           # กำหนดข้อความ name_song
           self.name_song.setText("Name song")
        # เปลี่ยนชื่อเพลงทุกครั้งที่ตัวแปร check_index_music เปลี่ยน
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_name_song(check_index_music, self.name_song))

        # จัดตำแหน่ง artis_name_song
        self.artis_name_song.setGeometry(int(show_music_x + 12), 490, 350, 41)
        if globals_var.index_music is None:
           # ปรับขนาดตัวหนังสือ
           size.setPointSize(14)
           self.artis_name_song.setFont(size)
           # กำหนดข้อความ artis_name_song
           self.artis_name_song.setText("artist")
        # เปลี่ยนชื่อศิลปินทุกครั้งที่ตัวแปร check_index_music เปลี่ยน
        globals_var.check_index_music.subscribe(lambda check_index_music: globals_var.update_artis_name_song(check_index_music, self.artis_name_song))

        # จัดตำแหน่ง show_user
        show_user_top = 10
        show_user_w = 50
        show_user_right = 100
        show_user_y = show_user_top
        show_user_x = self.width() - show_user_w - show_user_right
        self.show_user.setGeometry(int(show_user_x - 30), int(show_user_y + 15), 71, 16)
        size.setPointSize(14)
        # กำหนดข้อความ show_user
        self.show_user.setText(globals_var.user_now)

        # จัดตำแหน่ง play_music_box
        play_music_box_w = int(self.width() - 521) // 2
        self.play_music_box.setGeometry(int(play_music_box_w), int(down_bar_y + 5), 521, 91)

        #เก็บค่าความกว้างยาวของเมนู
        manu_box_w = self.manu_box.width()
        manu_box_h = self.manu_box.height()
        #กำหนดให้อยู่ตรงกลางแนวนอนและความห่างจากขอบบน
        x = (self.width() - manu_box_w) // 2
        y = 5
        #แสดงเมนู
        self.manu_box.setGeometry(x, y, manu_box_w, manu_box_h)
        
        # จัดตำแหน่ง out_profile
        margin_top = 10
        button_w = 50
        margin_right = 100
        out_profile_y = margin_top
        out_profile_x = self.width() - button_w - margin_right
        self.out_profile.setGeometry( int(out_profile_x + 50), int(out_profile_y + 10), 100, 32)

        # จัดตำแหน่ง set_volum
        set_volum_w = int(self.width() * 0.08)
        self.set_volum.setGeometry(int(play_music_box_w + 521), int(down_bar_y + 20), set_volum_w, 25)

        # จัดตำแหน่ง text_set_volum
        self.text_set_volum.setGeometry(int(play_music_box_w + 521), int(down_bar_y + 40), set_volum_w, 25)

        # จัดตำแหน่ง del_music_y
        del_music_x = int(self.width() * 0.1 )
        del_music_y = int(self.height() * 0.15 )
        self.del_music.setGeometry(del_music_x, del_music_y, 61, 32)
        
        # จัดตำแหน่ง del_music_all
        self.del_music_all.setGeometry(int(del_music_x + 150), del_music_y, 91, 32)

        # จัดตำแหน่ง del_profile
        self.del_profile.setGeometry(del_music_x, int(del_music_y + 150), 71, 32)

    def delete_profile(self):
        # ถามผู้ใช้ว่าจะลบจริงๆใช่มั้ย
        awer = QMessageBox.question(None, "ask for delete pro", "ต้องการลบโปรไฟล์นี้จริงๆใช่มั้ย", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if awer == QMessageBox.StandardButton.Yes:
           username = globals_var.user_now

           check_del = Control_Data_Store().delete_profile_in_DB(username)
           if check_del:
              self.stacked_widget.setCurrentIndex(0)
        elif awer == QMessageBox.StandardButton.No:
            return False
    
    def setting_to_home(self):
        Home.de_item_when_music_list_space()
        self.stacked_widget.setCurrentIndex(2)

    def setting_to_library(self):
        library.update_music_list()
        self.stacked_widget.setCurrentIndex(3)

    def setting_to_loging(self):
        globals_var.user_now = None
        globals_var.pass_now = None
        print(f" user is {globals_var.user_now}")
        print(f" pass is {globals_var.pass_now}")
        self.stacked_widget.setCurrentIndex(0)


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


