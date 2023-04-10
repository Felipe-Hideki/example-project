from typing import Union

from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter

from libs.Util import Util as util

class Box:
    Min_Dist = 2.

    def __init__(self, min: QPoint, max: QPoint) -> None:
        self.points: list[QPoint] = [None] * 4
        self.points[0] = min
        self.points[1] = QPoint(min.x(), max.y())
        self.points[2] = QPoint(max.x(), min.y())
        self.points[3] = max

        self.__rect = QRect(min, max)

    def is_within(self, point: QPoint) -> bool:
        return self.rect().contains(point)
    
    def closer_vertex(self, point: QPoint) -> Union[tuple[int, float], None]:
        min_dist = 0, util.distance(point, self.points[0])
        for i, p in enumerate(self.points):
            if (dist := util.distance(point, p)) < min_dist[1] and dist < Box.Min_Dist:
                min_dist = i, dist
        return min_dist if min_dist[1] < Box.Min_Dist else None

    def move_vertex(self, point: QPoint, index: int):
        if index == 0:
            self.points[0] = QPoint(point)
            self.points[1].setX(point.x())
            self.points[2].setY(point.y())
        elif index == 1:
            self.points[1] = QPoint(point)
            self.points[0].setX(point.x())
            self.points[3].setY(point.y())
        elif index == 2:
            self.points[2] = QPoint(point)
            self.points[0].setY(point.y())
            self.points[3].setX(point.x())
        elif index == 3:
            self.points[3] = QPoint(point)
            self.points[1].setY(point.y())
            self.points[2].setX(point.x())
        
        self.__rect = QRect(self.min(), self.max())
        return

    def pos(self) -> QPoint:
        return self.min()
    
    def min(self) -> QPoint:
        return self.__get_min()
    
    def max(self) -> QPoint:
        return self.__get_max()

    def rect(self) -> QRect:
        return self.__rect
    
    def __get_min(self) -> QPoint:
        minimum = QPoint(self.points[0])
        for p in self.points:
            minimum.setX(min(minimum.x(), p.x()))
            minimum.setY(min(minimum.y(), p.y()))
        return minimum
    
    def __get_max(self) -> QPoint:
        maximum = QPoint(self.points[0])
        for p in self.points:
            maximum.setX(max(maximum.x(), p.x()))
            maximum.setY(max(maximum.y(), p.y()))
        return maximum

    def draw(self, painter: QPainter):
        painter.setPen(Qt.red)
        painter.drawRect(self.rect())

        painter.setPen(Qt.green)
        for point in self.points:
            painter.drawEllipse(point, 5, 5)