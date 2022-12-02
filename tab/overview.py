from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

import requests
from bs4 import BeautifulSoup as bs
import re

class Overview(QWidget):

    def __init__(self, realm):
        super(Overview, self).__init__()
        self.realm = realm 
        self.scrapeData()
        self.setupUI()

    def scrapeData(self):
        raw = bs(requests.get("http://progressquest.com/realms.php").text, 'lxml')
        table = [i for i in raw.select_one("table").select("td")[:-1] if i.select_one("b").text == self.realm][0]

        self.pop = '{:,}'.format(int(re.findall(r'(\d+)', table.select_one("i").text)[0]))
        self.desc = table.select_one("p").text

    def setupUI(self):
        self.setObjectName("Overview")
        self.overviewLayout = QVBoxLayout(self)
        self.overviewLayout.setObjectName("overviewLayout")

        self.realmName = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.realmName.sizePolicy().hasHeightForWidth())
        self.realmName.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.realmName.setFont(font)
        self.realmName.setObjectName("realmName")
        self.overviewLayout.addWidget(self.realmName)

        self.realmPop = QLabel(self)
        font = QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.realmPop.setFont(font)
        self.realmPop.setObjectName("realmPop")
        self.overviewLayout.addWidget(self.realmPop)

        self.realmDesc = QLabel(self)
        self.realmDesc.setWordWrap(True)
        self.realmDesc.setObjectName("realmDesc")
        self.overviewLayout.addWidget(self.realmDesc)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.overviewLayout.addItem(spacerItem)

        _translate = QCoreApplication.translate
        self.realmName.setText(_translate("Layout", self.realm))
        self.realmDesc.setText(_translate("Layout", self.desc))
        self.realmPop.setText(_translate("Layout", f"Populations: {self.pop}"))