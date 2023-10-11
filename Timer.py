from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QPalette, QColor


s=m=h=0
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowTitle('Timer --S.U.P.E.R.B.O.T.')
        Form.setWindowIcon(QIcon('Images/Timer.png'))
        Form.resize(360, 240)
        Form.setMinimumSize(QtCore.QSize(360, 240))
        Form.setMaximumSize(QtCore.QSize(360, 240))
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(10, 190, 341, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(10, 10, 341, 141))
        self.lcdNumber.setObjectName("lcdNumber")

        time = "{:02}:{:02}:{:02}".format(0,0,0)

        self.lcdNumber.setDigitCount(len(time))
        self.lcdNumber.display(time)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 160, 341, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonStart = QtWidgets.QPushButton(self.widget)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.horizontalLayout.addWidget(self.pushButtonStart)
        self.pushButtonPause = QtWidgets.QPushButton(self.widget)
        self.pushButtonPause.setObjectName("pushButtonPause")
        self.horizontalLayout.addWidget(self.pushButtonPause)
        self.pushButtonLap = QtWidgets.QPushButton(self.widget)
        self.pushButtonLap.setObjectName("pushButtonLap")
        self.horizontalLayout.addWidget(self.pushButtonLap)
        self.pushButtonReset = QtWidgets.QPushButton(self.widget)
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.horizontalLayout.addWidget(self.pushButtonReset)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.Timer = QTimer()

        self.Timer.timeout.connect(self.LCD)
        self.pushButtonStart.clicked.connect(self.Start)
        self.pushButtonPause.clicked.connect(self.Pause)
        self.pushButtonLap.clicked.connect(self.Lap)
        self.pushButtonReset.clicked.connect(self.Reset)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Timer --S.U.P.E.R.B.O.T."))
        self.pushButtonStart.setText(_translate("Form", "Start"))
        self.pushButtonPause.setText(_translate("Form", "Pause"))
        self.pushButtonLap.setText(_translate("Form", "Lap"))
        self.pushButtonReset.setText(_translate("Form", "Reset"))

    def Start(self):
        global s, m, h
        self.Timer.start(1000)

    def Pause(self):
        self.Timer.stop()

    def Reset(self):

        global s, m, h

        self.Timer.stop()
        s = m= h= 0

        time = "{:02}:{:02}:{:02}".format(h, m, s)

        self.lcdNumber.setDigitCount(len(time))
        self.lcdNumber.display(time)

        self.textBrowser.setText('')

    def Lap(self):
        global s, m, h
        if self.Timer.isActive():
            self.textBrowser.append('The Lap is : {}'.format(str(self.time)))

        else:
            self.textBrowser.setText('')



    def LCD(self):
        global s, m, h

        if s < 59:
            s += 1
        else:
            if m < 59:
                s = 0
                m += 1
            elif m == 59 and h < 24:
                h += 1
                m = 0
                s = 0
            else:
                self.Timer.stop()

        self.time = "{:02}:{:02}:{:02}".format(h, m, s)

        self.lcdNumber.setDigitCount(len(self.time))
        self.lcdNumber.display(self.time)




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(83, 83, 83))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.gray)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")



    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())