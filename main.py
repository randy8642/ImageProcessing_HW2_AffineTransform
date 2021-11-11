import sys
import os
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import ImageQt
import cv2



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

        # Display               
        self.displayLabel = QLabel(self)
        self.displayLabel.setGeometry(100, 200, 600, 400)
        self.displayLabel.setScaledContents(True)
        self.displayLabel.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.displayLabel.mousePressEvent = self.image_click
        
        # Text
        self.label = QLabel(self)        
        self.label.setText("請先選擇圖片")

        # Buttom
        self.button1 = QPushButton(self)
        self.button1.setText("選取圖片")  # 建立名字
        self.button1.setGeometry(100, 100, 600, 50)  # 移動位置
        # 當 button1 這個物件發出訊號時( 被按了) 到 button1_clicked 這個槽執行
        self.button1.clicked.connect(self.open_image)

    def button1_clicked(self):
        print('click')

        pass

    def open_image(self):
        self.fileName = QFileDialog.getOpenFileName(self, \
            'Open file', 'c:\\',"Image files (*.jpg *.bmp *.png)")[0]
        if self.fileName == '':
            return
        self.displayLabel.setPixmap(QPixmap(self.fileName))
        self.image = QPixmap(self.fileName)
        self.selectImage = True

        self.label.setText('請點選左內眼角')
        # self.draw_point()
       
    def image_click(self, event):
        if not self.selectImage:
            return

        pos = event.pos()

        print(pos)
        # print('real pos', pos.x()/600*self.image.shape[1], pos.y()/400*self.image.shape[0])

        self.selectedPoint.append([pos.x(), pos.y()])
        self.draw_point()

    def draw_point(self):
        painter = QPainter(self.displayLabel.pixmap())        
        painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))

        painter.drawLine(10, 10, 300, 200)
        painter.end()


        return
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))

        prePoint = []
        for x, y in self.selectedPoint: 
            if len(prePoint) > 0:
                painter.drawLine(prePoint[0], prePoint[1], x, y)
            painter.drawPoint(x, y) 
            print('draw', x, y)
            prePoint = [x, y]    
        
        painter.end()
        self.update()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())