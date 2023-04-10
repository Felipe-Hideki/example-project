from math import sqrt

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QPoint, QRect

class Util:
    @staticmethod
    def get_main_widget() -> QMainWindow:
        return [widget for widget in QGuiApplication.instance().allWidgets() if isinstance(widget, QMainWindow)][0]
    
    @staticmethod
    def get_rect(x1: int, y1: int, x2: int, y2: int) -> QRect:
        return QRect(QPoint(x1, y1), QPoint(x2, y2))
    
    @staticmethod
    def distance(p1: QPoint, p2: QPoint) -> float:
        return sqrt((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2)