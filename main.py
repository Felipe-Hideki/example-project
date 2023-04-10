from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import QPoint

from libs.TopMenu import TopMenu
from libs.FileDialog import FileManager
from libs.Image import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Example app")
        self._on_resize_events: dict[str, callable] = {}
        topmenu = TopMenu(self)
        self.setMenuBar(topmenu)
        topmenu.setContentsMargins(0, 0, 0, 0)

        self.filemanager = FileManager(self)
        self.img = Image(self)
        self.img.move(0, topmenu.sizeHint().height())
        self.resize(800, 600)

    def add_resize_event(self, name: str, callback: callable):
        self._on_resize_events[name] = callback

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        for callback in self._on_resize_events.values():
            callback(a0)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()