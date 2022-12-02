from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from layout import Ui_Layout
import sys

class Window(QWidget, Ui_Layout):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Progress Quest Realms")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./pq.png'))
    window = Window()
    window.show()
    sys.exit(app.exec_())