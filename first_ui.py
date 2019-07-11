import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QFileDialog, QMainWindow, QToolButton, QMenu, QAction
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5.QtGui import QIcon
from main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pushButton_Click)
        self.pushButton_2.clicked.connect(self.pushButton_Click)
        self.pushButton_3.clicked.connect(self.pushButton_Click)
        # Set ToolButton
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolButton.setAutoRaise(True)
        menu = QMenu(self)
        self.sortAct = QAction('排序', self)
        self.gapAct = QAction('缺漏', self)
        self.deplicateAct = QAction('重複', self)
        menu.addAction(self.sortAct)
        menu.addAction(self.gapAct)
        menu.addAction(self.deplicateAct)
        self.toolButton.setMenu(menu)
        self.sortAct.triggered.connect(self.on_click)
        self.gapAct.triggered.connect(self.on_click)
        self.deplicateAct.triggered.connect(self.on_click)

        # SetTableView
        self.tableView.clicked.connect(self.getHeaderCell)
        self.tableView.horizontalHeader().sectionClicked.connect(self.getHeaderCell)

    def getHeaderCell(self, item):
        if isinstance(item, QModelIndex):
            self.selectedHeader = self.headerList[item.column()]
        else:
            self.selectedHeader = self.headerList[item]

        header = self.df[self.selectedHeader]
        self.label_9.setText('當前欄位 : ' + str(self.selectedHeader))
        if header.dtype == 'int64' or header.dtype == 'float64':
            self.label_2.setText('總筆數 : ' + str(header.count()))
            self.label_3.setText('最大 : ' + str(header.max()))
            self.label_4.setText('最小 : ' + str(header.min()))
            self.label_5.setText('平均 : ' + str(header.mean()))
            self.label_6.setText('標準差 : ' + str(header.std()))
            self.label_7.setText('加總 : ' + str(header.sum()))
            self.label_8.setText('欄位 : ' + str(self.selectedHeader))

    def setData(self):
        model = PandasModel(self.df)
        self.headerList = model.getHeaderData()
        self.tableView.setModel(model)

    def pushButton_Click(self):
        if self.sender() == self.pushButton:
            file, _ = QFileDialog.getOpenFileName(
                None, "Select File", "", "CSV File (*.csv)")
            if file:
                self.label.setText(file)
                self.df = pd.read_csv(file)
                self.setData()
        elif self.sender() == self.pushButton_2:
            self.df = pd.read_csv(self.label.text())
            self.setData()
        elif self.sender() == self.pushButton_3:
            text = self.lineEdit.text()
            if self.selectedHeader and text:
                self.df = self.df[self.df[self.selectedHeader].astype('str') == text]
                self.setData()

    def on_click(self):
        if self.sender() == self.sortAct:
            self.df = self.df.sort_values(self.selectedHeader)
            self.setData()
        elif self.sender() == self.gapAct:
            data = self.df
            self.df = data[data[self.selectedHeader].isnull()]
            self.setData()
        elif self.sender() == self.deplicateAct:
            data = self.df
            self.df = data[data.duplicated(self.selectedHeader, keep=False)]
            self.setData()


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index.tolist()[col]
        return None

    def getHeaderData(self):
        return list(self._data.columns)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
