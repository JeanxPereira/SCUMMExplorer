# 2021 - Douglas Diniz - www.manualdocodigo.com.br

import sys

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QFontDatabase

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.filename = ""
        self.setWindowTitle('Hex Editor')

        QFontDatabase.addApplicationFont('fonts/unifont.ttf')

        # Load the UI Page
        uic.loadUi("mainwindow.ui", self)

        self.setStyleSheet("background-color: #0f0f0f;")

        self.actionopen.triggered.connect(self.open)
        self.actionsave.triggered.connect(self.save)
        self.actionsave_as.triggered.connect(self.saveAs)
        self.lineEditAddress.textChanged.connect(self.serCursorPosition)

    def open(self):
        fName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
        if fName:
            f = QFile(fName)
            if f.open(QFile.OpenModeFlag.ReadOnly):
                data = f.readAll()
                self.hexwidget.setData(data)
                self.filename = fName

    def save(self):
        if self.filename:
            data = self.hexwidget.getData()
            with open(self.filename, "wb") as f:
                f.write(data)
            print("Saved successfully...")
        else:
            print("No file to save")

    def saveAs(self):
        fName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        if fName:
            self.filename = fName
            self.save()
        else:
            print("Invalid File")

    def serCursorPosition(self):
        try:
            address = int(self.lineEditAddress.text(), 16)
            self.hexwidget.setCursorPosition(address)
        except ValueError:
            print("Invalid hexadecimal number")


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Theme test from:
    # https://github.com/Alexhuszagh/BreezeStyleSheets
    # if False:
    file = QFile("./ui.qss")
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
