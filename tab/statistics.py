from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QRect, Qt, QCoreApplication, QSize
from PyQt5.QtGui import QFont

import requests
from bs4 import BeautifulSoup as bs

class Statistics(QWidget):
    ID = {
        'Knoram': 'knor',
        'Expodrine': 'expo',
        'Oobag': 'ooba',
        'Spoltog': 'spog',
        'Pemptus': 'pemp',
        'Alpaquil': 'alpa'
    }

    def __init__(self, realm):
        super(Statistics, self).__init__()
        self.realm = realm

        self.scrapeData()
        self.setupUI()

    def scrapeData(self):
        soup = bs(requests.get(f"http://progressquest.com/stats.php?realm={self.ID[self.realm]}").text, 'lxml')
        data = [i.select("tr")[1:] for i in soup.select("table table")]
        self.data = [[[i.text for i in i.select("td")] for i in i] for i in data]
        print(self.data)

    def getQTableWidgetHeight(self, table):
        h = table.horizontalHeader().height() + 4
        for i in range(table.rowCount() - 1):
            h += table.rowHeight(i)
        return h + 10

    def setupTable(self, table):
        table.setColumnCount(2)
        table.setRowCount(6)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setMinimumHeight(self.getQTableWidgetHeight(table))
        table.setSpan(0, 0, 1, 2)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)

    def addTableTitle(self, table, title):
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        item = QTableWidgetItem()
        item.setData(Qt.DisplayRole, title)
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        table.setItem(0, 0, item)

    def insertData(self, table, data):
        for i, v in enumerate(data):
            for j, w in enumerate(v):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, int(w) if w.isnumeric() else w)
                if w.isnumeric(): item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                table.setItem(i+1, j, item)
        
    def setupUI(self):
        self.setObjectName("Statistics")
        self.statisticLayout = QVBoxLayout(self)
        self.statisticLayout.setObjectName("verticalLayout")
        
        self.tableWrapper = QScrollArea(self)
        self.tableWrapper.setWidgetResizable(True)
        self.tableWrapper.setObjectName("tableWrapper")

        self.tableContainer = QWidget()
        self.tableContainer.setGeometry(QRect(0, 0, 534, 500))
        self.tableContainer.setObjectName("tableContainer")

        self.verticalLayout_2 = QVBoxLayout(self.tableContainer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.statisticLabel = QLabel(self.tableContainer)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.statisticLabel.setFont(font)
        self.statisticLabel.setAlignment(Qt.AlignCenter)
        self.statisticLabel.setObjectName("statisticLabel")
        self.verticalLayout_2.addWidget(self.statisticLabel)

        self.populationLabel = QLabel(self.tableContainer)
        self.populationLabel.setAlignment(Qt.AlignCenter)
        self.populationLabel.setObjectName("populationLabel")
        self.verticalLayout_2.addWidget(self.populationLabel)

        self.lv2OrHigherLabel = QLabel(self.tableContainer)
        self.lv2OrHigherLabel.setAlignment(Qt.AlignCenter)
        self.lv2OrHigherLabel.setObjectName("lv2OrHigherLabel")
        self.verticalLayout_2.addWidget(self.lv2OrHigherLabel)

        self.averageLevelLabel = QLabel(self.tableContainer)
        self.averageLevelLabel.setAlignment(Qt.AlignCenter)
        self.averageLevelLabel.setObjectName("averageLevelLabel")
        self.verticalLayout_2.addWidget(self.averageLevelLabel)
        
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.top5RacesByPopulatiry = QTableWidget(self.tableContainer)
        self.top5RacesByPopulatiry.setObjectName("top5RacesByPopulatiry")
        self.setupTable(self.top5RacesByPopulatiry)
        self.addTableTitle(self.top5RacesByPopulatiry, "Top 5 Races by Popularity")
        self.insertData(self.top5RacesByPopulatiry, self.data[0])

        self.top5RacesByCombinedLevel = QTableWidget(self.tableContainer)
        self.top5RacesByCombinedLevel.setObjectName("top5RacesByCombinedLevel")
        self.setupTable(self.top5RacesByCombinedLevel)
        self.addTableTitle(self.top5RacesByCombinedLevel, "Top 5 Races by Combined Level")
        self.insertData(self.top5RacesByCombinedLevel, self.data[1])

        self.top5ClassesByPopulatiry = QTableWidget(self.tableContainer)
        self.top5ClassesByPopulatiry.setObjectName("top5ClassesByPopulatiry")
        self.setupTable(self.top5ClassesByPopulatiry)
        self.addTableTitle(self.top5ClassesByPopulatiry, "Top 5 Classes by Popularity")
        self.insertData(self.top5ClassesByPopulatiry, self.data[2])
        
        self.top5ClassesByCombinedLevel = QTableWidget(self.tableContainer)
        self.top5ClassesByCombinedLevel.setObjectName("top5ClassesByCombinedLevel")
        self.setupTable(self.top5ClassesByCombinedLevel)
        self.addTableTitle(self.top5ClassesByCombinedLevel, "Top 5 Classes by Combined Level")
        self.insertData(self.top5ClassesByCombinedLevel, self.data[3])

        self.top5AvatarByPopularity = QTableWidget(self.tableContainer)
        self.top5AvatarByPopularity.setObjectName("top5AvatarByPopularity")
        self.setupTable(self.top5AvatarByPopularity)
        self.addTableTitle(self.top5AvatarByPopularity, "Top 5 Avatar by Popularity")
        self.insertData(self.top5AvatarByPopularity, self.data[4])

        self.top5AvatarByCombinedLevel = QTableWidget(self.tableContainer)
        self.top5AvatarByCombinedLevel.setObjectName("top5AvatarByCombinedLevel")
        self.setupTable(self.top5AvatarByCombinedLevel)
        self.addTableTitle(self.top5AvatarByCombinedLevel, "Top 5 Avatar by Combined Level")
        self.insertData(self.top5AvatarByCombinedLevel, self.data[5])

        self.gridLayout.addWidget(self.top5RacesByPopulatiry, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.top5ClassesByPopulatiry, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.top5AvatarByPopularity, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.top5RacesByCombinedLevel, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.top5ClassesByCombinedLevel, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.top5AvatarByCombinedLevel, 2, 1, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)
        self.tableWrapper.setWidget(self.tableContainer)
        self.statisticLayout.addWidget(self.tableWrapper)

        _translate = QCoreApplication.translate

        self.statisticLabel.setText(_translate("Layout", "Statistics"))
        self.populationLabel.setText(_translate("Layout", "Population 121,101"))
        self.lv2OrHigherLabel.setText(_translate("Layout", "(81,868 level 2 or higher)"))
        self.averageLevelLabel.setText(_translate("Layout", "Average Level: 28"))