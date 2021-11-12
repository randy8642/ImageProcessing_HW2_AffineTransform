'''
https://stackoverflow.com/questions/22954239/given-three-points-compute-affine-transformation
'''
import sys
import os
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import ImageQt
import cv2
from collections import deque
import numpy as np
import itertools

class displayLabel(QLabel):
    def customInit(self):        
        self.haveImage = False
        self.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.setScaledContents(True)
        self.selectedPoint = deque([])
        self.parent().btn_startTransform.setEnabled(False)

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
            
            prePoint = [x, y]

        if len(self.selectedPoint) > 2:
            painter.drawLine(self.selectedPoint[-1][0], self.selectedPoint[-1][1], self.selectedPoint[0][0], self.selectedPoint[0][1])
        # painter.end()

    def mousePressEvent(self, event):
        if not self.haveImage:
            return

        pos = event.pos()

        self.selectedPoint.append([pos.x(), pos.y()])

        if len(self.selectedPoint) > 2:
            self.parent().btn_startTransform.setEnabled(True)
        else:
            self.parent().btn_startTransform.setEnabled(False)

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
        # self.dstTri = [[130, 180], [190, 180], [160, 240]]   
        self.dstTri = [[65, 90], [95, 90], [80, 120]]       
        self.processedImage = None          
        
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

        self.btn_startTransform = QPushButton(self)
        self.btn_startTransform.setText('Transform')
        self.btn_startTransform.setFont(QFont('Arial', 20))
        self.btn_startTransform.setGeometry(100, 650, 600, 50)
        self.btn_startTransform.setEnabled(False)
        self.btn_startTransform.clicked.connect(self.run_AffineTransform)

        self.btn_saveImage = QPushButton(self)
        self.btn_saveImage.setText('Save')
        self.btn_saveImage.setFont(QFont('Arial', 20))
        self.btn_saveImage.setGeometry(800, 650, 600, 50)
        self.btn_saveImage.setEnabled(False)
        self.btn_saveImage.clicked.connect(self.save_image)

        # Display
        self.displayLabel = displayLabel(self)    
        self.displayLabel.customInit()       
        self.displayLabel.setGeometry(100, 200, 600, 400)

        self.disployLabel_processed = QLabel(self)
        self.disployLabel_processed.setGeometry(800, 200, 320, 380)
    
    def open_image(self):
        self.fileName = QFileDialog.getOpenFileName(self, \
            'Open file', 'c:\\',"Image files (*.jpg *.bmp *.png)")[0]
        if self.fileName == '':
            return

        self.displayLabel.setImage(QPixmap(self.fileName))

        self.label.setText('請依序點選 [左內眼角] -> [右內眼角] -> [鼻尖]')

    def run_AffineTransform(self):
        self.srcTri = self.displayLabel.selectedPoint
        src_tri = np.array(self.srcTri, dtype=np.float32)
        dst_tri = np.array(self.dstTri, dtype=np.float32)
        
        srcImg = cv2.imread(self.fileName)
        
        src_tri[:, 0] = src_tri[:, 0] / 600 * srcImg.shape[1]
        src_tri[:, 1] = src_tri[:, 1] / 400 * srcImg.shape[0]


        wrap_mat = cv2.getAffineTransform(src_tri, dst_tri)

        dst = apply_AffineTransform(srcImg, wrap_mat, (190, 160))

        dst = cv2.resize(dst, (320, 380))
        self.processedImage = dst

        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)

        height, width, channel = dst.shape
        bytesPerLine = 3 * width
        qImg = QImage(dst.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.disployLabel_processed.setPixmap(QPixmap.fromImage(qImg))
        
        self.btn_saveImage.setEnabled(True)
    
    def save_image(self):
        saveFileName = os.path.splitext(self.fileName.split('/')[-1])[0]
        saveImg = cv2.resize(self.processedImage, (160, 190))
        cv2.imwrite(f'./results/{saveFileName}.jpg', saveImg)

def cal_AffineTransformMatrix(srcPoints: np.ndarray, dstPoints:np.ndarray):




    return 0

def apply_AffineTransform(src, matrix, dst_size):
    mat = np.concatenate((matrix, [[0, 0, 1]]), axis=0)

    targetPoint = [(mat @ np.array([[x], [y], [1]]))[:2, 0] for x, y in itertools.product(range(src.shape[1]), range(src.shape[0]))]
    sourcePoint = [[x, y] for x, y in itertools.product(range(src.shape[1]), range(src.shape[0]))]

    targetPoint = np.array(targetPoint, dtype=np.int32)
    sourcePoint = np.array(sourcePoint, dtype=np.int32)

    mask = (targetPoint[:, 0] < dst_size[1]) & (targetPoint[:, 1] < dst_size[0]) & \
        (targetPoint[:, 1] >= 0) & (targetPoint[:, 0] >= 0)
    targetPoint = targetPoint[mask]
    sourcePoint = sourcePoint[mask]

    dst = np.zeros([dst_size[0], dst_size[1], 3], dtype=np.uint8)
    dst[targetPoint[:, 1], targetPoint[:, 0]] = src[sourcePoint[:, 1], sourcePoint[:, 0]]

    return dst
    

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())