import sys
import os
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import ImageQt
import cv2
from collections import deque

class displayLabel(QLabel):
    def customInit(self):        
        self.haveImage = False
        self.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.setScaledContents(True)
        self.selectedPoint = deque([])

    def setImage(self, filePath):
        self.customInit()
        self.image = QPixmap(filePath)
        self.haveImage = True

    def paintEvent(self, event): 
        if not self.haveImage:
            return       

        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

        #
        painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))        
        prePoint = []
        for x, y in self.selectedPoint: 
            if len(prePoint) > 0:
                painter.drawLine(prePoint[0], prePoint[1], x, y)
            painter.drawPoint(x, y) 
            print('draw', x, y)
            prePoint = [x, y]

        if len(self.selectedPoint) > 2:
            painter.drawLine(self.selectedPoint[-1][0], self.selectedPoint[-1][1], self.selectedPoint[0][0], self.selectedPoint[0][1])
        # painter.end()

    def mousePressEvent(self, event):
        if not self.haveImage:
            return

        pos = event.pos()

        self.selectedPoint.append([pos.x(), pos.y()])

        if len(self.selectedPoint) > 3:
            self.selectedPoint.popleft()

        self.update()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1500, 800)
        self.setWindowTitle('face transform')

        # param
        self.srcTri = [] # [左內眼角], [右內眼角], [鼻尖]
        self.dstTri = [[65, 90], [95, 90], [80, 120]]
        self.selectedPoint = []
        self.selectImage = False
        self.image = QPixmap(600, 400)

        # Display
        self.displayLabel = displayLabel(self)    
        self.displayLabel.customInit()       
        self.displayLabel.setGeometry(100, 200, 600, 400)        
        
        # Text
        self.label = QLabel(self)        
        self.label.setText("Select image first")
        self.label.setGeometry(100, 150, 600, 50)
        self.label.setAlignment(Qt.AlignCenter) 
        self.label.setFont(QFont('Arial', 20)) 

        # Buttom
        self.btn_selectImage = QPushButton(self)
        self.btn_selectImage.setText("Select Image")
        self.btn_selectImage.setFont(QFont('Arial', 20)) 
        self.btn_selectImage.setGeometry(100, 100, 600, 50)        
        self.btn_selectImage.clicked.connect(self.open_image)


    
    def open_image(self):
        self.fileName = QFileDialog.getOpenFileName(self, \
            'Open file', 'c:\\',"Image files (*.jpg *.bmp *.png)")[0]
        if self.fileName == '':
            return

        self.displayLabel.setImage(QPixmap(self.fileName))
        self.image = QPixmap(self.fileName)
        self.selectImage = True

        self.label.setText('請依序點選 [左內眼角] -> [右內眼角] -> [鼻尖]')

       

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())