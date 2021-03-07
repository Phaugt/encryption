from cryptography.fernet import Fernet
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, qApp, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QMainWindow,
                            QMessageBox, QStatusBar, QWidget, QMenuBar, QStatusBar, QAction, QRadioButton)
from PyQt5.QtCore import QFile, QObject , Qt
from PyQt5.QtGui import QIcon
import sys, os
from easysettings import EasySettings
from pathlib import Path
from os.path import expanduser


def resource_path(relative_path):
    """used by pyinstaller to see the relative path"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

guifile = resource_path("./gui/main.ui")
logo = resource_path("./gui/logo.png")
userfold = expanduser("~")
config = EasySettings(userfold+"/secret.key")

class GUI(QMainWindow):
    """main window used by the application"""
    def __init__(self):
        super(GUI, self).__init__()
        UIFile = QFile(guifile)
        UIFile.open(QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()
        
        self.w = Worker()
        self.w.write_key()

        self.setAcceptDrops(True)

        self.file.setAlignment(Qt.AlignCenter)
        self.file.setText('\n\n Drop file here! \n\n')
        self.file.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
            }
            ''')
        self.btnEncrypt.clicked.connect(self.encrypt)
        self.btnDecrypt.clicked.connect(self.decrypt)

    def informationMessage(self,message):
        """send message to messagebox"""
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.exec()
        

    def dragEnterEvent(self, event):
        """accept the drag to window if it contains an file"""
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
 
    def dragMoveEvent(self, event):
        """accept the drag to window if it contains an file"""
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        """accept file when dropped into window"""
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.fileLocation.setText(file_path)
 
            event.accept()
        else:
            event.ignore()


    def encrypt(self):
        self.w.encrypt()
    
    def decrypt(self):
        self.w.decrypt()

class Worker(QObject):

    def write_key(self):
        try:
            check = Path('secret2.key')
            if check.is_file():
                pass
            else:
                key = Fernet.generate_key()
                with open("secret2.key", "wb") as key_file:
                    key_file.write(key)
        except FileNotFoundError:
            pass

    def load_key(self):
        return open("secret2.key", "rb").read()

    def encrypt(self):
        key = self.load_key()
        f = Fernet(key)
        with open('/Users/patrikhauguth/GIT/encryption/csv1.png', "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open('/Users/patrikhauguth/GIT/encryption/csv1.png', "wb") as file:
            file.write(encrypted_data)

    def decrypt(self):
        key = self.load_key()
        f = Fernet(key)
        with open('/Users/patrikhauguth/GIT/encryption/csv1.png', "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open('/Users/patrikhauguth/GIT/encryption/csv1.png', "wb") as file:
            file.write(decrypted_data)


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(logo))
window = GUI()
window.show()
app.exec_()