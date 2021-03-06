from PyQt5.QtCore import *    # core Qt functionality
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *       # extends QtCore with GUI functionality
from PyQt5 import uic

from TrafficLight import *

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

        self.PedestrianSignalEW.turnGreen()
        self.PedestrianSignalNS.turnRed()
        self.TrafficLightNS.turnGreen()
        self.TrafficLightEW.turnRed()

        # Update views -----------------------------
        timer  = QTimer(self)
        timer.setInterval(20) # period in miliseconds
        timer.timeout.connect(self.TrafficLightEW.update)
        timer.timeout.connect(self.TrafficLightNS.update)
        timer.timeout.connect(self.PedestrianSignalEW.update)
        timer.timeout.connect(self.PedestrianSignalNS.update)
        timer.start()


def main():
    app = QApplication(sys.argv)

    main = MainWindow()
    #main = MainWindow()

    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()