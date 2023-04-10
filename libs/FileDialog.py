import os
import typing

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject, pyqtSlot

from libs.Image import Image

class FileManager(QObject):
    __instance = None

    @classmethod
    def instance(cls) -> typing.Union[None, "FileManager"]:
        return cls.__instance

    def __init__(self, parent):
        super().__init__(parent)
        FileManager.__instance = self
    
    def open(self, title):
        path = QFileDialog.getOpenFileName(self.parent(), title, os.path.expanduser("~"), "Images (*.png *.jpg)")[0]
        Image.instance().load(path)
    
    def save(self, title):
        path = QFileDialog.getExistingDirectory(self.parent(), title, os.path.expanduser("~"))
        Image.instance().save(path)