import typing

from PyQt5.QtGui import QPixmap, QResizeEvent, QPaintEvent, QPainter, QMouseEvent, QCursor, QKeyEvent
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize, QPoint

from libs.Util import Util as util
from libs.Box import Box

normal, drawing, moving = range(3)

class Image(QWidget):
    __instance = None

    @classmethod
    def instance(cls) -> typing.Union[None, "Image"]:
        return cls.__instance
    
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.draw_square = (False, None)
        self.img = QPixmap()
        self.painter = QPainter()
        self.pixmap_orig_size = QSize(0, 0)

        self.boxes: list[Box] = []
        self.state = normal

        mainWindow.add_resize_event("Image", self.on_resize)

        self.setContentsMargins(0, 0, 0, 0)

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        Image.__instance = self

    def paintEvent(self, a0: QPaintEvent):
        self.painter.begin(self)
        self.painter.setPen(Qt.black)
        self.painter.drawPixmap(0, 0, self.img)
        for box in self.boxes:
            box.draw(self.painter)
        if self.draw_square[0]:
            mousepos = self.mapFromGlobal(QCursor.pos())
            self.painter.setPen(Qt.red)
            self.painter.drawRect(util.get_rect(self.draw_square[1].x(), self.draw_square[1].y(), mousepos.x(), mousepos.y()))
            self.painter.setPen(Qt.black)
        self.painter.end()

    def on_resize(self, event: QResizeEvent):
        self.pixmap_size = event.size()
        self.img = self.img.scaled(self.pixmap_size)
        self.setFixedSize(self.pixmap_size)

    def load(self, path: str):
        print("Loading image from", path)
        self.img.load(path)
        self.pixmap_orig_size = self.img.size()
        self.img = self.img.scaled(self.pixmap_size)
        self.update()
    
    def save(self, path: str):
        print("Saving image to", path)
        for i, box in enumerate(self.boxes):
            result = self.img.copy(box.rect()).save(f"{path}/Box_{i}.png", "PNG", 100)
            print(f"Saved {i}.png: {result}")

    def delete_all_boxes(self):
        self.boxes = []
        self.update()

    def closest_vertex(self, point: QPoint) -> typing.Union[None, tuple[Box, int, float]]:
        closest = None, -1, float("inf")
        for box in self.boxes:
            closer = box.closer_vertex(point)
            if closer and closer[1] < closest[2]:
                closest = box, closer[0], closer[1]

        return closest if closest[2] != float("inf") else None
        

    def is_drawing(self) -> bool:
        return self.state == drawing
    
    def is_moving(self) -> bool:
        return self.state == moving

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self.is_moving():
            self.moving_box[0].move_vertex(a0.pos(), self.moving_box[1])
        else:
            closest = self.closest_vertex(a0.pos())
            if closest:
                self.setCursor(Qt.PointingHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        self.update()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.is_drawing():
            self.draw_square = (True, a0.pos())
        else:
            closest = self.closest_vertex(a0.pos())
            if closest:
                self.state = moving
                self.moving_box = closest[0], closest[1]
        self.update()

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if self.draw_square[0]:
            self.boxes.append(Box(self.draw_square[1], a0.pos()))
            self.draw_square = (False, None)
            self.state = normal
        elif self.is_moving():
            self.moving_box = None
            self.state = normal
        self.update()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_W:
            print("w")
            self.state = drawing
        
        if a0.key() == Qt.Key_Escape:
            self.state = normal
            self.draw_square = (False, None)