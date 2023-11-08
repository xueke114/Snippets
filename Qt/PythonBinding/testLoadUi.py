import sys

from PyQt5 import uic, QtWidgets


class TestDialog(QtWidgets.QDialog):
    def __init__(self):
        super(TestDialog, self).__init__()
        uic.loadUi("exampleDialog.ui", self)
        self.pushButton = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.lcd = self.findChild(QtWidgets.QLCDNumber, "lcdNumber")

        self.pushButton.clicked.connect(self.on_push_button)

    def on_push_button(self):
        print(self.lcd.intValue())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = TestDialog()
    dialog.show()
    app.exec_()
