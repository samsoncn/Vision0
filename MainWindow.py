from PyQt5.QtCore import *    # core Qt functionality
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *       # extends QtCore with GUI functionality
from PyQt5 import uic

from TrafficLight import * 

import cv2
#from detect import detector
from test_detect import detector

from collections import Counter

import sys
import os

DETECTION_TOLERANCE = 5

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs,)

        # Load the UI
        fileh = QFile(r'ui\main_window.ui')
        fileh.open(QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()

        # traffic light control
        self.counter = 0
        self.green = True

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.numPeople.connect(self.updateTrafficState)
        th.start()

        # Update views -----------------------------
        timer  = QTimer(self)
        timer.timeout.connect(self.updateLights)
        timer.start()

    def updateLights(self):
        if self.counter > DETECTION_TOLERANCE:
            self.green = not(self.green)

        if self.green:
            self.PedestrianSignalEW.turnGreen()
            self.TrafficLightEW.turnRed()
            self.PedestrianSignalNS.turnRed()
            self.TrafficLightNS.turnGreen()

        else:
            self.PedestrianSignalEW.turnRed()
            self.TrafficLightEW.turnGreen()
            self.PedestrianSignalNS.turnGreen()
            self.TrafficLightNS.turnRed()

        self.TrafficLightEW.update()
        self.PedestrianSignalEW.update()
        self.PedestrianSignalNS.update()
        self.TrafficLightNS.update()        

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.VideoLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(dict)
    def updateTrafficState(self, data):

        # REYNOLD ------------------------------------------
        if 0 not in data.key():
            numPed = 0
        else:
            numPed = data['0']
        
        if 2 not in data.key():
            numCars = 0
        else:
            numCars = data['2']


        if (numPed > 0 and self.green) or (numPed == 0 and not(self.green)):
            self.counter = 0
        else:
            self.counter += 1

        self.NumberofPedestrians.setText('# of Pedestrians Currently Moving E/W:  ' + str(numPed))
        self.NumberCars.setText('# of Cars Currently Moving or in View:  ' + str(numCars))

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    numPeople = pyqtSignal(dict)

    def run(self):
        cap = cv2.VideoCapture('./testing/t3(1).mp4')

        while (cap.isOpened()):
            ret, frame = cap.read()

            frame, classIDs = detector(frame)

            # REYNOLD ------------------------------------------
            self.numPeople.emit(Counter(classIDs))

            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(960, 720, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

            if cv2.waitKey(1) == 13:
                break
            if frame is None:
                break

def main():
    app = QApplication(sys.argv)

    main = MainWindow()
    #main = MainWindow()

    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()