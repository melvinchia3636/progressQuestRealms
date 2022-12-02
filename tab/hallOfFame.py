from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QLineEdit, QTableWidget, QComboBox, QPushButton, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QCoreApplication

import requests
from bs4 import BeautifulSoup as bs
import re

class HallOfFame(QWidget):
    def __init__(self, realm):
        super(HallOfFame, self).__init__()
        self.realm = "Expo" if realm == "Expodrine" else realm
        self.page = 1

        self.scrapeData()
        self.setupUI()

    def scrapeData(self, query=None):
        raw = requests.get("http://progressquest.com/{}.php?{}".format(self.realm.lower(), f"name={query}" if query else f"min={(self.page-1)*10+1}&max=10")).text
        soup = bs(raw, 'lxml')
        table = soup.select('table tr')[1:]
        table = [[i.text for i in i.select('td')] for i in table]
        
        self.data = table

        try:
            population = re.findall(r"Pop\. (\d+)</i>", raw)[0]
            self.population = population
        except:
            self.population = "-"

    def setupUI(self):
        self.setObjectName("HallOfFame")

        self.hallOfFameLayout = QVBoxLayout(self)
        self.hallOfFameLayout.setObjectName("outerWrapper")

        self.topWrapper = QHBoxLayout()
        self.topWrapper.setObjectName("topWrapper")

        self.findLabel = QLabel(self)
        self.findLabel.setObjectName("findLabel")

        self.queryInput = QLineEdit(self)
        self.queryInput.setObjectName("queryInput")

        self.proceedSearchButton = QPushButton(self)
        self.proceedSearchButton.setObjectName("proceedSearchButton")
        
        self.hallOfFameTable = QTableWidget(self)

        self.hallOfFameTable.setObjectName("hallOfFameTable")
        self.hallOfFameTable.setColumnCount(len(self.data[0]))
        self.hallOfFameTable.setRowCount(len(self.data))
        self.hallOfFameTable.setHorizontalHeaderLabels([
            "Rank",
            "Name",
            "Race",
            "Class",
            "Level",
            "Prime Stat",
            "Plot Stage",
            "Prized Item",
            "Specialty",
            "Motto (Ctrl-M) ",
            "Guild (Ctrl-G)",
        ])
        self.hallOfFameTable.verticalHeader().setVisible(False)
        self.hallOfFameTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.hallOfFameTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.hallOfFameTable.setSelectionMode(QTableWidget.SingleSelection)
        self.hallOfFameTable.setSortingEnabled(True)

        header = self.hallOfFameTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        for i, v in enumerate(self.data):
            for j, w in enumerate(v):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, int(w) if w.isdecimal() else w)
                self.hallOfFameTable.setItem(i, j, item)

        self.bottomWrapper = QHBoxLayout()
        self.bottomWrapper.setObjectName("bottomWrapper")

        bottomSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.top10Button = QPushButton(self)
        self.top10Button.setObjectName("top10Button")

        self.refreshButton = QPushButton(self)
        self.refreshButton.setObjectName("refreshButton")

        self.lastPageButton = QPushButton(self)
        self.lastPageButton.setObjectName("lastPageButton")

        self.currentPageLabel = QLabel(self)
        self.currentPageLabel.setAlignment(Qt.AlignCenter)
        self.currentPageLabel.setObjectName("currentPageLabel")

        self.nextPageButton = QPushButton(self)
        self.nextPageButton.setObjectName("nextPageButton")

        self.topWrapper.addWidget(self.findLabel)
        self.topWrapper.addWidget(self.queryInput)
        self.topWrapper.addWidget(self.proceedSearchButton)

        self.bottomWrapper.addWidget(self.top10Button)
        self.bottomWrapper.addWidget(self.refreshButton)
        self.bottomWrapper.addItem(bottomSpacer)
        self.bottomWrapper.addWidget(self.lastPageButton)
        self.bottomWrapper.addWidget(self.currentPageLabel)
        self.bottomWrapper.addWidget(self.nextPageButton)

        self.hallOfFameLayout.addLayout(self.topWrapper)
        self.hallOfFameLayout.addWidget(self.hallOfFameTable)
        self.hallOfFameLayout.addLayout(self.bottomWrapper)

        _translate = QCoreApplication.translate
        
        self.findLabel.setText(_translate("Layout", "Find:"))
        self.lastPageButton.setText(_translate("Layout", "<"))
        self.currentPageLabel.setText(_translate("Layout", f"{(self.page-1)*10+1} - {self.page * 10} / {self.population}"))
        self.nextPageButton.setText(_translate("Layout", ">"))
        self.proceedSearchButton.setText(_translate("Layout", "Go"))
        self.refreshButton.setText(_translate("Layout", "Refresh"))
        self.top10Button.setText(_translate("Layout", "Top 10"))
        
        self.lastPageButton.clicked.connect(self.lastPage)
        self.nextPageButton.clicked.connect(self.nextPage)
        self.queryInput.returnPressed.connect(self.submitSearch)
        self.proceedSearchButton.clicked.connect(self.submitSearch)
        self.refreshButton.clicked.connect(self.refresh)
        self.top10Button.clicked.connect(self.top10)

    def updateTable(self):
        self.hallOfFameTable.setRowCount(len(self.data))
        self.hallOfFameTable.setSpan(0, 0, 1, 1)
        self.currentPageLabel.setText(f"{(self.page-1)*10+1} - {self.page * 10} / {self.population}")
        for i, v in enumerate(self.data):
            for j, w in enumerate(v):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, int(w) if w.isdecimal() else w)
                self.hallOfFameTable.setItem(i, j, item)

        self.hallOfFameTable.clearSelection()
        self.highlightQuery()

    def highlightQuery(self):
        try:
            for i, v in enumerate(self.data):
                if v[1].lower() == self.queryInput.text().lower():
                    self.hallOfFameTable.selectRow(i)
                    self.page = (int(v[0]) // 10) + 1
                    self.currentPageLabel.setText(f"{(self.page-1)*10+1} - {self.page * 10} / {self.population}")
                    break
        except:
            pass

    def lastPage(self):
        if self.page > 1: self.page -= 1
        self.scrapeData()
        self.updateTable()

    def nextPage(self):
        self.page += 1
        self.scrapeData()
        self.updateTable()

    def submitSearch(self):
        self.hallOfFameTable.setSpan(0, 0, 1, 1)
        self.scrapeData(query=self.queryInput.text())

        if all([len(i) < 5 for i in self.data]):
            self.hallOfFameTable.setRowCount(1)
            self.hallOfFameTable.setItem(0, 0, QTableWidgetItem("No results found."))
            self.hallOfFameTable.setSpan(0, 0, 1, 11)
            return

        self.updateTable()
        
    def refresh(self):
        if self.queryInput.text(): self.scrapeData(query=self.queryInput.text())
        else: self.scrapeData()
        if all([len(i) < 5 for i in self.data]):
            self.hallOfFameTable.setRowCount(1)
            self.hallOfFameTable.setItem(0, 0, QTableWidgetItem("No results found."))
            self.hallOfFameTable.setSpan(0, 0, 1, 11)
            return

        self.updateTable()
        

    def top10(self):
        self.page = 1
        self.scrapeData()
        self.updateTable()


