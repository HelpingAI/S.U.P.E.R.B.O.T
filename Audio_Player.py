from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *

from qtwidgets import EqualizerBar

import random
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.UI_Components()

    def UI_Components(self):

        self.equalizer = EqualizerBar(5, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])

        # ----------
        # mp3 player
        # ----------

        self.player = QMediaPlayer()

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
        PausePreferenceAction.triggered.connect(self.Pause_Video)
        PreferenceMenu.addAction(PausePreferenceAction)

        # ----------
        # Stop
        # ----------

        StopPreferenceAction = QAction(QIcon('Images/Stop.png'), 'Stop', self)
        StopPreferenceAction.setStatusTip('Stop')
        StopPreferenceAction.triggered.connect(lambda: self.player.stop())
        PreferenceMenu.addAction(StopPreferenceAction)

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
        # Creating Audio Slider
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

        self.Volume_slider.sliderMoved.connect(self.player.setVolume)
        self.Volume_slider.valueChanged.connect(self.Volume_Changed)

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

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.Play_Button)
        controlLayout.addWidget(self.Stop_Button)
        controlLayout.addWidget(self.slider)
        controlLayout.addWidget(self.Volume_label)
        controlLayout.addWidget(self.Volume_slider)
        controlLayout.addWidget(self.Muted_CheckBox)

        layout = QVBoxLayout()
        layout.addWidget(self.equalizer)
        layout.addLayout(controlLayout)

        wid.setLayout(layout)

        self.player.stateChanged.connect(self.Logo_Changed)
        self.player.positionChanged.connect(self.position_Changed)
        self.player.durationChanged.connect(self.duration_Changed)

    def Open_File(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open", '.',
                                                       "Files (*.wav *.mp3)",
                                                       QDir.homePath())

        if self.fileName != '':
            self.player.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.Play_Button.setEnabled(True)
            self.Stop_Button.setEnabled(True)
            self.Muted_CheckBox.setEnabled(True)
            self.Volume_slider.setEnabled(True)

            self.timer = QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.update_values)

    def Play_Video(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.timer.stop()

        else:
            self.player.play()
            self.timer.start()

    def Logo_Changed(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.Play_Button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))


        else:
            self.Play_Button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def Pause_Video(self):
        self.player.pause()
        self.timer.stop()

    def Volume_Changed(self):
        self.value = self.Volume_slider.value()
        self.Volume_label.setText(str(self.value))

    def Muted_Checking(self):
        if self.Muted_CheckBox.isChecked():
            self.player.setMuted(True)

        else:
            self.player.setMuted(False)

    def Stop_Function(self):
        self.player.stop()
        self.timer.stop()

    def Quit_Function(self):
        sys.exit(App.exec_())

    def position_Changed(self, position):
        self.slider.setValue(position)

    def duration_Changed(self, duration):
        self.slider.setRange(0, duration)

    def set_Position(self, position):
        self.player.setPosition(position)

    def update_values(self):
        self.equalizer.setValues([
            min(100, v + random.randint(0, 50)
            if random.randint(0, 5) > 2 else v)
            for v in self.equalizer.values()])


if __name__ == '__main__':
    App = QApplication(sys.argv)
    App.setWindowIcon(QIcon('Images\\Icon'))
    App.setApplicationName('Audio Player --S.U.P.E.R.B.O.T')
    App.setStyle('Fusion')
    Equalizer = Window()
    Equalizer.resize(460, 340)
    Equalizer.show()

    sys.exit(App.exec_())