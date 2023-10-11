from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Paint')
        self.setWindowIcon(QIcon('Images\\Paint.png'))
        self.setMaximumSize(860, 720)
        self.setMinimumSize(860, 720)

        self.UI()

    def UI(self):
        self.Image = QImage(self.size(), QImage.Format_RGB32)
        self.Image.fill(Qt.white)

        self.Drawing = False
        self.BrushSize = 2
        self.BrushColor = Qt.black
        self.LastPoint = QPoint()

        self.MainMenu = self.menuBar()
        self.FileMenu = self.MainMenu.addMenu('File')
        self.BrushSizeMenu = self.MainMenu.addMenu('Brush Size')
        self.BrushColorMenu = self.MainMenu.addMenu('Brush Color')

        self.OpenAction = QAction(QIcon('Images\\Open.png'), 'Open', self)
        self.OpenAction.setShortcut(QKeySequence.Open)
        self.OpenAction.triggered.connect(self.Open)
        self.FileMenu.addAction(self.OpenAction)

        self.SaveAction = QAction(QIcon('Images\\Save.png'), 'Save', self)
        self.SaveAction.setShortcut(QKeySequence.Save)
        self.SaveAction.triggered.connect(self.Save)
        self.FileMenu.addAction(self.SaveAction)

        self.ClearAction = QAction(QIcon('Images\\Clear.png'), 'Clear', self)
        self.ClearAction.triggered.connect(self.Clear)
        self.FileMenu.addAction(self.ClearAction)

        self.QuitAction = QAction(QIcon('Images\\Quit.png'), 'Quit', self)

        self.QuitAction.setShortcut(QKeySequence.Close)
        self.QuitAction.triggered.connect(self.closeEvent)
        self.FileMenu.addAction(self.QuitAction)

        self.OnepxAction = QAction(QIcon('Images\\1.png'), 'One', self)
        self.OnepxAction.triggered.connect(self.One)
        self.BrushSizeMenu.addAction(self.OnepxAction)

        self.TwopxAction = QAction(QIcon('Images\\2.png'), 'Two', self)
        self.TwopxAction.triggered.connect(self.Two)
        self.BrushSizeMenu.addAction(self.TwopxAction)

        self.ThreepxAction = QAction(QIcon('Images\\3.png'), 'Three', self)
        self.ThreepxAction.triggered.connect(self.Three)
        self.BrushSizeMenu.addAction(self.ThreepxAction)

        self.FourpxAction = QAction(QIcon('Images\\4.png'), 'Four', self)
        self.FourpxAction.triggered.connect(self.Four)
        self.BrushSizeMenu.addAction(self.FourpxAction)

        self.FivepxAction = QAction(QIcon('Images\\5.png'), 'Five', self)
        self.FivepxAction.triggered.connect(self.Five)
        self.BrushSizeMenu.addAction(self.FivepxAction)

        self.SixpxAction = QAction(QIcon('Images\\6.png'), 'Six', self)
        self.SixpxAction.triggered.connect(self.Six)
        self.BrushSizeMenu.addAction(self.SixpxAction)

        self.SevenpxAction = QAction(QIcon('Images\\7.png'), 'Seven', self)
        self.SevenpxAction.triggered.connect(self.Seven)
        self.BrushSizeMenu.addAction(self.SevenpxAction)

        self.EightpxAction = QAction(QIcon('Images\\7.png'), 'Eight', self)
        self.EightpxAction.triggered.connect(self.Eight)
        self.BrushSizeMenu.addAction(self.EightpxAction)

        self.NinepxAction = QAction(QIcon('Images\\9.png'), 'Nine', self)
        self.NinepxAction.triggered.connect(self.Nine)
        self.BrushSizeMenu.addAction(self.NinepxAction)

        self.MessageAction = QAction(QIcon('Images\\Colors'), 'Standard Colors', self)
        self.MessageAction.setText('Standard Colors')
        self.BrushColorMenu.addAction(self.MessageAction)

        self.BrushColorMenu.addSeparator()

        # self.WhiteAction = QAction(QIcon('Images/White.png'), 'White',self)
        # self.WhiteAction.triggered.connect(self.White)
        # self.BrushColorMenu.addAction(self.WhiteAction)

        self.BlackAction = QAction(QIcon('Images\\Black.png'), 'Black', self)
        self.BlackAction.triggered.connect(self.Black)
        self.BrushColorMenu.addAction(self.BlackAction)

        self.DarkGrayAction = QAction(QIcon('Images\\Dark Gray.png'), 'Dark Gray', self)
        self.DarkGrayAction.triggered.connect(self.DarkGray)
        self.BrushColorMenu.addAction(self.DarkGrayAction)

        self.GrayAction = QAction(QIcon('Images\\Gray.png'), 'Gray', self)
        self.GrayAction.triggered.connect(self.Gray)
        self.BrushColorMenu.addAction(self.GrayAction)

        self.LightGrayAction = QAction(QIcon('Images\\Light Gray.png'), 'Light Gray', self)
        self.LightGrayAction.triggered.connect(self.LightGray)
        self.BrushColorMenu.addAction(self.LightGrayAction)

        self.DarkRedAction = QAction(QIcon('Images\\Dark Red.png'), 'Dark Red', self)
        self.DarkRedAction.triggered.connect(self.DarkRed)
        self.BrushColorMenu.addAction(self.DarkRedAction)

        self.BrownAction = QAction(QIcon('Images\\Brown.png'), 'Brown', self)
        self.BrownAction.triggered.connect(self.Brown)
        self.BrushColorMenu.addAction(self.BrownAction)

        self.RedAction = QAction(QIcon('Images\\Red.png'), 'Red', self)
        self.RedAction.triggered.connect(self.Red)
        self.BrushColorMenu.addAction(self.RedAction)

        self.PinkAction = QAction(QIcon('Images\\Pink.png'), 'Pink', self)
        self.PinkAction.triggered.connect(self.Pink)
        self.BrushColorMenu.addAction(self.PinkAction)

        self.DarkYellowAction = QAction(QIcon('Images\\Dark Yellow.png'), 'Dark Yellow', self)
        self.DarkYellowAction.triggered.connect(self.DarkYellow)
        self.BrushColorMenu.addAction(self.DarkYellowAction)

        self.YellowAction = QAction(QIcon('Images\\Yellow.png'), 'Yellow', self)
        self.YellowAction.triggered.connect(self.Yellow)
        self.BrushColorMenu.addAction(self.YellowAction)

        self.LightYellowAction = QAction(QIcon('Images\\Light Yellow.png'), 'Light Yellow', self)
        self.LightYellowAction.triggered.connect(self.LightYellow)
        self.BrushColorMenu.addAction(self.LightYellowAction)

        self.OrangeAction = QAction(QIcon('Images\\Orange.png'), 'Orange', self)
        self.OrangeAction.triggered.connect(self.Orange)
        self.BrushColorMenu.addAction(self.OrangeAction)

        self.DarkGreenAction = QAction(QIcon('Images\\Dark Green.png'), 'Dark Green', self)
        self.DarkGreenAction.triggered.connect(self.DarkGreen)
        self.BrushColorMenu.addAction(self.DarkGreenAction)

        self.GreenAction = QAction(QIcon('Images\\Green.png'), 'Green', self)
        self.GreenAction.triggered.connect(self.Green)
        self.BrushColorMenu.addAction(self.GreenAction)

        self.LightGreenAction = QAction(QIcon('Images\\Light Green.png'), 'Light Green', self)
        self.LightGreenAction.triggered.connect(self.LightGreen)
        self.BrushColorMenu.addAction(self.LightGreenAction)

        self.LightBlueAction = QAction(QIcon('Images\\Light Blue.png'), 'Light Blue', self)
        self.LightBlueAction.triggered.connect(self.LightBlue)
        self.BrushColorMenu.addAction(self.LightBlueAction)

        self.BlueAction = QAction(QIcon('Images\\Blue.png'), 'Blue', self)
        self.BlueAction.triggered.connect(self.Blue)
        self.BrushColorMenu.addAction(self.BlueAction)

        self.DarkBlueAction = QAction(QIcon('Images\\Dark Blue.png'), 'Dark Blue', self)
        self.DarkBlueAction.triggered.connect(self.DarkBlue)
        self.BrushColorMenu.addAction(self.DarkBlueAction)

        self.MarineBlueAction = QAction(QIcon('Images\\Marine Blue.png'), 'Marine Blue', self)
        self.MarineBlueAction.triggered.connect(self.MarineBlue)
        self.BrushColorMenu.addAction(self.MarineBlueAction)

        self.VioletAction = QAction(QIcon('Images\\Purple.png'), 'Purple', self)
        self.VioletAction.triggered.connect(self.Purple)
        self.BrushColorMenu.addAction(self.VioletAction)

        self.BrushColorMenu.addSeparator()

        self.SelectColorAction = QAction(QIcon('Images\\Color Picker.png'), 'Select Color', self)
        self.SelectColorAction.triggered.connect(self.ColorDialog)
        self.BrushColorMenu.addAction(self.SelectColorAction)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.Drawing = True
            self.LastPoint = event.pos()

            # print(self.LastPoint)

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton) and self.Drawing:
            Painter = QPainter(self.Image)
            Painter.setPen(QPen(self.BrushColor, self.BrushSize,
                                Qt.SolidLine, Qt.RoundCap,
                                Qt.RoundJoin))

            Painter.drawLine(self.LastPoint, event.pos())
            self.LastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.Drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.Image,
                                self.Image.rect())

    def Save(self):
        filePath, _ = QFileDialog.getSaveFileName(self,
                                                  'Save Image',
                                                  '',
                                                  '*.PNG')
        if filePath == '':
            return
        self.Image.save(filePath)

    def Clear(self):
        self.Image.fill(Qt.white)
        self.update()

    def closeEvent(self, event):
        text = '''Are you sure you want to Quit?\nAny unsaved work will be lost.'''
        reply = QMessageBox.question(
            self, 'Warning!', text,
            QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Close
        )

        if reply == QMessageBox.Close:
            QApplication.quit()

        elif reply == QMessageBox.Save:
            self.Save()

        elif reply == QMessageBox.Cancel:
            pass

        else:
            pass

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            QApplication.quit()

    def ColorDialog(self):

        self.Dailog = QColorDialog()

        self.Dailog.exec_()
        self.Value = self.Dailog.selectedColor()
        print(self.Value)

        self.BrushColor = self.Value

    def Open(self, event):

        filename = QFileDialog.getOpenFileName()
        imagepath = filename[0]
        print(imagepath)

        image = QImage(imagepath)

        painter = QPainter(self.Image)
        painter.setPen(QPen(Qt.NoPen))

        height = image.height()
        width = image.width()

        painter.drawImage(QRect(0, 0, height * 2, width * 2), image)

    def One(self):
        self.BrushSize = 1

    def Two(self):
        self.BrushSize = 2

    def Three(self):
        self.BrushSize = 3

    def Four(self):
        self.BrushSize = 4

    def Five(self):
        self.BrushSize = 5

    def Six(self):
        self.BrushSize = 6

    def Seven(self):
        self.BrushSize = 7

    def Eight(self):
        self.BrushSize = 8

    def Nine(self):
        self.BrushSize = 9

    def Black(self):
        self.BrushColor = Qt.black

    def Red(self):
        self.BrushColor = Qt.red

    def Yellow(self):
        self.BrushColor = Qt.yellow

    def LightBlue(self):
        self.BrushColor = QColor(173, 216, 230)

    def DarkBlue(self):
        self.BrushColor = Qt.darkBlue

    def Orange(self):
        self.BrushColor = QColor(255, 165, 0)

    def LightGreen(self):
        self.BrushColor = QColor(144, 238, 144)

    def DarkGreen(self):
        self.BrushColor = Qt.darkGreen

    def Purple(self):
        self.BrushColor = QColor(128, 0, 128)

    def Brown(self):
        self.BrushColor = QColor(165, 42, 42)

    def White(self):
        self.BrushColor = Qt.white

    def MarineBlue(self):
        self.BrushColor = QColor(0, 119, 190)

    def LightGray(self):
        self.BrushColor = Qt.lightGray

    def DarkGray(self):
        self.BrushColor = Qt.darkGray

    def Gray(self):
        self.BrushColor = Qt.gray

    def DarkRed(self):
        self.BrushColor = Qt.darkRed

    def Pink(self):
        self.BrushColor = QColor(247, 120, 193)

    def DarkYellow(self):
        self.BrushColor = Qt.darkYellow

    def LightYellow(self):
        self.BrushColor = QColor(244, 247, 155)

    def Green(self):
        self.BrushColor = Qt.green

    def Blue(self):
        self.BrushColor = Qt.blue


App = QApplication(sys.argv)
Main = MainWindow()
Main.resize(640, 480)
Main.show()

sys.exit(App.exec_())