from PyQt5.QtGui import QIcon, QFont, QKeySequence, QPalette, QColor
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer,
                                QMediaPlaylist, QAudio)

from PyQt5 import QtMultimedia
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QCheckBox,
                             QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QMenu, QMenuBar, QAction,
                             QSlider, QStyle, QVBoxLayout,
                             QWidget, QStatusBar, QMainWindow)

import sys
import os

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.p = self.palette()
        self.p.setColor(QPalette.Window, Qt.black)
        self.setPalette(self.p)

        self.mediaPlayer = QMediaPlayer(None,
                                        QMediaPlayer.VideoSurface)

        # ----------
        # Creating File Menu
        # ----------

        FileMenu = self.menuBar().addMenu('&File')

        # ----------
        # Open
        # ----------

        OpenFileAction = QAction(QIcon('Images/Open.png'), 'Open...', self)
        OpenFileAction.setStatusTip('Open')
        OpenFileAction.setShortcut(QKeySequence.Open)
        OpenFileAction.triggered.connect(self.Open_File)
        FileMenu.addAction(OpenFileAction)

        # ----------
        # Separator
        # ----------

        FileMenu.addSeparator()

        # ----------
        # Quit
        # ----------

        QuitFileAction = QAction(QIcon('Images/Close.png'), 'Quit...', self)
        QuitFileAction.setStatusTip('Quit')
        QuitFileAction.setShortcut(QKeySequence.Close)
        QuitFileAction.triggered.connect(self.Quit_Function)
        FileMenu.addAction(QuitFileAction)

        # ----------
        # Creating Preference Menu
        # ----------

        PreferenceMenu = self.menuBar().addMenu('&Preference')

        # ----------
        # Start
        # ----------

        StartPreferenceAction = QAction(QIcon('Images/Play.png'), 'Play', self)
        StartPreferenceAction.setStatusTip('Play')
        StartPreferenceAction.triggered.connect(self.Play_Video)
        PreferenceMenu.addAction(StartPreferenceAction)

        # ----------
        # Pause
        # ----------

        PausePreferenceAction = QAction(QIcon('Images/Pause.png'), 'Pause', self)
        PausePreferenceAction.setStatusTip('Pause')
        PausePreferenceAction.triggered.connect(lambda: self.mediaPlayer.pause())
        PreferenceMenu.addAction(PausePreferenceAction)

        # ----------
        # Stop
        # ----------

        StopPreferenceAction = QAction(QIcon('Images/Stop.png'), 'Stop', self)
        StopPreferenceAction.setStatusTip('Stop')
        StopPreferenceAction.triggered.connect(lambda: self.mediaPlayer.stop())
        PreferenceMenu.addAction(StopPreferenceAction)

        # ----------
        # Separator
        # ----------

        # PreferenceMenu.addSeparator()

        # ----------
        # Maximize
        # ----------

        # MaximizePreferenceAction = QAction('Maximize', self)
        # MaximizePreferenceAction.setStatusTip('Maximize')
        # MaximizePreferenceAction.triggered.connect(self.Show_Maximize)
        # PreferenceMenu.addAction(MaximizePreferenceAction)

        # ----------
        # Minimize
        # ----------

        # MinimizePreferenceAction = QAction('Minimize', self)
        # MinimizePreferenceAction.setStatusTip('Minimize')
        # MinimizePreferenceAction.triggered.connect(self.Show_Minimize)
        # PreferenceMenu.addAction(MinimizePreferenceAction)

        # ----------
        # Creating Video Object
        # ----------

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        # ----------
        # Creating Play Button
        # ----------

        self.Play_Button = QPushButton()
        self.Play_Button.setEnabled(False)
        self.Play_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.Play_Button.clicked.connect(self.Play_Video)

        # ----------
        # Creating Stop Button
        # ----------

        self.Stop_Button = QPushButton()
        self.Stop_Button.setEnabled(False)
        self.Stop_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.Stop_Button.clicked.connect(self.Stop_Function)

        # ----------
        # Creating Video Slider
        # ----------

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_Position)

        # ----------
        # Creating Volume Slider
        # ----------

        self.Volume_slider = QSlider(Qt.Horizontal)
        self.Volume_slider.setMinimum(1)
        self.Volume_slider.setMaximum(100)
        self.Volume_slider.setValue(70)
        self.Volume_slider.setEnabled(False)

        self.Volume_slider.sliderMoved.connect(self.mediaPlayer.setVolume)
        self.Volume_slider.valueChanged.connect(self.Volume_Changed)

        # ----------
        # Creating Label
        # ----------

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred,
                                 QSizePolicy.Maximum)

        # ----------
        # Creating Volume Display Label
        # ----------

        self.Volume_label = QLabel()
        self.Volume_label.setText('70')

        # ----------
        # Creating Mute Check Box
        # ----------

        self.Muted_CheckBox = QCheckBox()
        self.Muted_CheckBox.setEnabled(False)
        self.Muted_CheckBox.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        self.Muted_CheckBox.toggled.connect(self.Muted_Checking)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        # ----------
        # Create layouts to place inside widget
        # ----------

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.Play_Button)
        controlLayout.addWidget(self.Stop_Button)
        controlLayout.addWidget(self.slider)
        controlLayout.addWidget(self.Volume_label)
        controlLayout.addWidget(self.Volume_slider)
        controlLayout.addWidget(self.Muted_CheckBox)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)

        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.Logo_Changed)
        self.mediaPlayer.positionChanged.connect(self.position_Changed)
        self.mediaPlayer.durationChanged.connect(self.duration_Changed)

    def Open_File(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open", '.',
                                                       "Files (*.mp4 *.flv *.ts *.mts *.avi *.wav *.mp3 *.mkv)",
                                                       QDir.homePath())

        if self.fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.Play_Button.setEnabled(True)
            self.Stop_Button.setEnabled(True)
            self.Muted_CheckBox.setEnabled(True)
            self.Volume_slider.setEnabled(True)

            self.Play_Video()

    def Play_Video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def Logo_Changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.Play_Button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.Play_Button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    # def Show_Maximize(self):
    #     player = VideoPlayer()
    #     player.showMaximized()
    #
    # def Show_Minimize(self):
    #     player = VideoPlayer()
    #     player.setGeometry(10000, 10000, 480, 360)
    #     player.show()

    def Volume_Changed(self):
        self.value = self.Volume_slider.value()
        self.Volume_label.setText(str(self.value))

    def Muted_Checking(self):
        if self.Muted_CheckBox.isChecked():
            self.mediaPlayer.setMuted(True)

        else:
            self.mediaPlayer.setMuted(False)

    def Stop_Function(self):
        self.mediaPlayer.stop()

    def Quit_Function(self):
        sys.exit(App.exec_())

    def position_Changed(self, position):
        self.slider.setValue(position)

    def duration_Changed(self, duration):
        self.slider.setRange(0, duration)

    def set_Position(self, position):
        self.mediaPlayer.setPosition(position)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setApplicationName('Media Player --S.U.P.E.R.B.O.T')
    App.setWindowIcon(QIcon('Images/Icon.png'))
    App.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(192, 192, 192))
    palette.setColor(QPalette.WindowText, Qt.yellow)
    palette.setColor(QPalette.Base, QColor(255, 255, 0))
    palette.setColor(QPalette.AlternateBase, QColor(64, 128, 128))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.darkMagenta)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(255, 128, 128))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    App.setPalette(palette)
    App.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    Player = VideoPlayer()
    Player.resize(480, 360)
    Player.show()
    sys.exit(App.exec_())