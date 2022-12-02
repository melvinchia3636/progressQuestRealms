from PyQt5 import QtCore, QtGui, QtWidgets
from tab.tab import TabWidget


class Ui_Layout(object):
    def setupUi(self, Layout):
        Layout.setObjectName("Layout")
        Layout.resize(772, 393)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Layout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListWidget(Layout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMaximumSize(QtCore.QSize(150, 16777215))
        self.listView.setObjectName("listView")
        
        realmList = ['Knoram', 'Expodrine', 'Oobag', 'Spoltdog', 'Pemptus', 'Alpaquil']
        
        items = [QtWidgets.QListWidgetItem(realmList[i]) for i in range(len(realmList))]
        for i in items:
            self.listView.addItem(i)

        self.listView.setCurrentItem(items[0])
        self.horizontalLayout.addWidget(self.listView)

        self.tabWidget1 = TabWidget('Knoram')
        self.tabWidget2 = TabWidget('Expodrine',)
        self.tabWidget3 = TabWidget('Oobag')
        self.tabWidget4 = TabWidget('Spoltog')
        self.tabWidget5 = TabWidget('Pemptus')
        self.tabWidget6 = TabWidget('Alpaquil')

        self.stack = QtWidgets.QStackedWidget(Layout)
        self.stack.addWidget(self.tabWidget1)
        self.stack.addWidget(self.tabWidget2)
        self.stack.addWidget(self.tabWidget3)
        self.stack.addWidget(self.tabWidget4)
        self.stack.addWidget(self.tabWidget5)
        self.stack.addWidget(self.tabWidget6)

        self.listView.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.horizontalLayout.addWidget(self.stack)

        self.retranslateUi(Layout)

        QtCore.QMetaObject.connectSlotsByName(Layout)

    def retranslateUi(self, Layout):
        _translate = QtCore.QCoreApplication.translate
        Layout.setWindowTitle(_translate("Layout", "Form"))
