import csv
import sys

from qtpy import QtWidgets

from ui.mainwindow import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Rezepte")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.readCsvFile("rezepte.csv")
        self.ui.newEntryButton.clicked.connect(self.onNewEntry)
        self.ui.saveButton.clicked.connect(self.onSave)

    def onSave(self):
        with open('rezepte.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"')

            rows = self.ui.rezepteTable.rowCount()
            for i in range(0, rows):
                rowContent = [
                    self.ui.rezepteTable.item(i, 0).text(),
                    self.ui.rezepteTable.item(i, 1).text(),
                    self.ui.rezepteTable.item(i, 2).text()
                ]
                writer.writerow(rowContent)

    def onNewEntry(self):
        row = self.ui.rezepteTable.rowCount()
        self.ui.rezepteTable.insertRow(row)

        self.ui.rezepteTable.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
        self.ui.rezepteTable.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
        self.ui.rezepteTable.setItem(row, 2, QtWidgets.QTableWidgetItem(""))

        cell = self.ui.rezepteTable.item(row, 0)
        self.ui.rezepteTable.editItem(cell)

    def readCsvFile(self, filename):
        self.ui.rezepteTable.setRowCount(0)
        with open(filename, "r", newline='', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            for line in reader:
                row = self.ui.rezepteTable.rowCount()
                self.ui.rezepteTable.insertRow(row)

                self.ui.rezepteTable.setItem(row, 0, QtWidgets.QTableWidgetItem(line[0]))
                self.ui.rezepteTable.setItem(row, 1, QtWidgets.QTableWidgetItem(line[1]))
                self.ui.rezepteTable.setItem(row, 2, QtWidgets.QTableWidgetItem(line[2]))


window = MainWindow()

window.show()

sys.exit(app.exec_())
