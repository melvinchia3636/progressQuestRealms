from PyQt5.QtWidgets import QWidget, QVBoxLayout

class Statistics(QWidget):
    ID = {
        'Knoram': 'knor',
        'Expodrine': 'expo',
        'Oobag': 'ooba',
        'Spoltog': 'spog',
        'Pemptus': 'pemp',
        'Alpaquil': 'alpa'
    }

    def __init__(self):
        super(Statistics, self).__init__()
        self.setupUI()
        
    def setupUI(self):
        self.setObjectName("Statistics")
        self.statisticLayout = QVBoxLayout(self)
        self.statisticLayout.setObjectName("StatisticsLayout")