from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import QCoreApplication

from tab.overview import Overview
from tab.hallOfFame import HallOfFame
from tab.hallOfInfamy import HallOfInfamy
from tab.statistics import Statistics

class TabWidget(QTabWidget):
    def __init__(self, realm=None, parent=None):
        super(TabWidget, self).__init__(parent)
        self.realm = realm

        self.setTabShape(QTabWidget.Rounded)
        self.setObjectName("tabWidget")

        self.setupUI()
        self.retranslateUi()

    def setupUI(self):
        self.overview = Overview(self.realm)
        self.hallOfFame = HallOfFame(self.realm)
        self.hallOfInfamy = HallOfInfamy(self.realm)
        self.statistics = Statistics()

        self.addTab(self.overview, "")
        self.addTab(self.hallOfFame, "")
        self.addTab(self.hallOfInfamy, "")
        self.addTab(self.statistics, "")
        
        self.setCurrentIndex(0)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setTabText(self.indexOf(self.overview), _translate("Layout", "Overview"))
        self.setTabText(self.indexOf(self.hallOfFame), _translate("Layout", "Hall of Fame"))
        self.setTabText(self.indexOf(self.hallOfInfamy), _translate("Layout", "Hall of Infamy"))
        self.setTabText(self.indexOf(self.statistics), _translate("Layout", "Statistics"))