# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time

from PyQt5.uic.properties import QtGui


class UserInterface(QWidget):

    def __init__(self):
        super().__init__()

        # calling initUI method
        self.initUI()

    # method for creating widgets
    def initUI(self):
        # preview
        self.preview_label = QLabel("Output Preview")
        preview_layout = QVBoxLayout()
        preview_display = QLabel()
        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(preview_display)

        layout = QVBoxLayout()

        site_text_layout = QHBoxLayout()
        site_text = QTextEdit()
        site_text.setPlaceholderText("example.com")
        enter_bt = QPushButton('Enter')
        site_text_layout.addWidget(site_text)
        site_text_layout.addWidget(enter_bt)

        path_layout = QHBoxLayout()
        self.path_display = QTextEdit()
        self.path_display.setPlaceholderText("Enter logo path")
        logo_bt = QPushButton('select logo')
        logo_bt.clicked.connect(self.openFileNameDialog)
        path_layout.addWidget(self.path_display)
        path_layout.addWidget(logo_bt)

        run_bt = QPushButton('Process')
        preview_bt = QPushButton('Preview')
        preview_bt.clicked.connect(self.preview)

        layout.addLayout(preview_layout)
        layout.addLayout(site_text_layout)
        layout.addLayout(path_layout)
        layout.addWidget(preview_bt)

        layout.addWidget(run_bt)

        self.setLayout(layout)
        # setting window geometry
        self.setGeometry(300, 300, 280, 170)

        # setting window action
        self.setWindowTitle("Blog Image Generator")

        # showing all the widgets
        self.show()

    # when button is pressed this method is being called
    def preview(self):
        pixmap = QPixmap('logo.png')
        self.preview_label.setPixmap(pixmap)
        self.preview_label.resize(pixmap.width(), pixmap.height())

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getOpenFileName(self, "Select Logo Image", "",
                                                   "Images (*.png *.jpg)", options=options)
        if file_name:
            self.path_display.setText(file_name)
            # print(file_name)


# main method
if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = UserInterface()

    # start the app
    sys.exit(App.exec())
