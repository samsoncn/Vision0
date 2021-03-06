from PyQt5.QtCore import *    # core Qt functionality
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *       # extends QtCore with GUI functionality
from PyQt5 import uic

import sys
import os

class Light(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.green = False
        self.yellow = False
        self.red = False

        self.greenLight_img = ''
        self.redLight_img = ''

    def reset(self):
        self.green = False
        self.yellow = False
        self.red = False

    def turnGreen(self):
        self.reset()
        self.green = True
    
    def turnRed(self):
        self.reset()
        self.red = True

    def turnYellow(self):
        self.reset()
        self.yellow = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)

        self.drawBlackBox(painter)
        self.drawSignal(painter)

        painter.end()

    def drawBlackBox(self, painter):
        p = painter.pen()
        painter.setPen(p)

        painter.fillRect(self.rect(), QColor('black'))

    def drawSignal(self, painter):
        if self.green:
            pixmap = QPixmap(self.greenLight_img)
            r = self.rect()
            greenlight_rect = QRect(r.x() + r.width()/4, r.y() + r.height()/2, r.width()/2, r.width()/2)
            painter.drawPixmap(greenlight_rect, pixmap)

        elif self.red:
            pixmap = QPixmap(self.redLight_img)
            r = self.rect()
            redlight_rect = QRect(r.x() + r.width()/4, r.y(), r.width()/2, r.width()/2)
            painter.drawPixmap(redlight_rect, pixmap)

class PedestrianLight(Light):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.greenLight_img = 'image/p_greenlight.png'
        self.redLight_img = 'image/p_redlight.png'

class TrafficLight(Light):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.greenLight_img = 'image/t_greenlight.png'
        self.redLight_img = 'image/t_redlight.png'

