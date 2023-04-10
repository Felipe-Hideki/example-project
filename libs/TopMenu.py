from PyQt5.QtWidgets import QMenuBar, QMenu
from PyQt5.QtCore import pyqtSlot

from libs.FileDialog import FileManager
from libs.Image import Image

class TopMenu(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_menu = QMenu("File", parent)
        self.file_menu.addAction("Open", self.open_file, "Ctrl+O")
        self.file_menu.addAction("Save", self.save_file, "Ctrl+S")

        self.edit_menu = QMenu("Edit", parent)
        self.edit_menu.addAction("Delete", self.delete, "Del")

        self.addMenu(self.file_menu)
        self.addMenu(self.edit_menu)

    @pyqtSlot()
    def open_file(self):
        if (instance := FileManager.instance()) is None:
            return
        instance.open("Open image")
    
    @pyqtSlot()
    def save_file(self):
        if (instance := FileManager.instance()) is None:
            return
        instance.save("Save image")

    @pyqtSlot()
    def delete(self):
        if (instance := Image.instance()) is None:
            return
        instance.delete_all_boxes()