from PyQt5.QtCore import *    # core Qt functionality
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *       # extends QtCore with GUI functionality
from PyQt5 import uic

from TrafficLight import *

import cv2
from detect import detector

import sys
import os

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs,)

        # Load the UI
        fileh = QFile(r'ui\main_window.ui')
        fileh.open(QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.numPeople.connect(self.updateLights)
        th.start()
        self.show()

        # Update views -----------------------------
        timer  = QTimer(self)
        timer.setInterval(20) # period in miliseconds
        timer.timeout.connect(self.TrafficLightEW.update)
        timer.timeout.connect(self.TrafficLightNS.update)
        timer.timeout.connect(self.PedestrianSignalEW.update)
        timer.timeout.connect(self.PedestrianSignalNS.update)
        timer.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.VideoLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(int)
    def updateLights(self, num):

        if num:
            self.PedestrianSignalEW.turnGreen()
            self.TrafficLightEW.turnRed()

        else:
            self.PedestrianSignalEW.turnRed()
            self.TrafficLightEW.turnGreen()

        self.TrafficLightEW.update()
        self.PedestrianSignalEW.update()

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    numPeople = pyqtSignal(int)

    def run(self):
        cap = cv2.VideoCapture('./testing/video.mp4')

        frameTime = 10

        while (cap.isOpened()):
            ret, frame = cap.read()

            frame, n = detector(frame)

            self.numPeople.emit(n)

            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

            if cv2.waitKey(frameTime) & 0xFF == ord('q'):
                break


def main():
    app = QApplication(sys.argv)

    main = MainWindow()
    #main = MainWindow()

    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()