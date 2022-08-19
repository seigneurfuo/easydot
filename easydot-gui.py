#!/bin/env python3
import sys
import os
from pathlib import Path

from easydot import get_symbolics_links, Messages

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_events()
        self.fill_data()

    def init_ui(self):
        loadUi(os.path.join(os.path.dirname(__file__), "mainwindow.ui"), self)

        self.setWindowTitle("easydot GUI - 0.1.2")

    def init_events(self):
        self.pushButton.clicked.connect(self.when_remove_button_clicked)
        self.pushButton_2.clicked.connect(self.when_update_button_clicked)
        self.pushButton_3.clicked.connect(self.when_open_source_folder_button_clicked)
        self.pushButton_4.clicked.connect(self.when_open_destination_folder_button_clicked)

    def fill_data(self):
        homepath = Path.home()
        path = os.path.join(homepath, "Dotfiles")
        links = get_symbolics_links(path)

        self.tableWidget.setRowCount(len(links))

        for row_index, link in enumerate(links):
            #  Col 1
            item = QTableWidgetItem(link["src_short"])
            item.setToolTip(link["src_short"])
            item.setData(Qt.UserRole, link)
            self.tableWidget.setItem(row_index, 0, item)

            # Col 2
            item = QTableWidgetItem(link["src_short"])
            item.setToolTip(link["dst_short"])
            item.setData(Qt.UserRole, link)
            self.tableWidget.setItem(row_index, 1, item)

            # Col 2
            item = QTableWidgetItem(link["src_short"])
            item.setToolTip(link["src_short"])
            item.setData(Qt.UserRole, link)
            self.tableWidget.setItem(row_index, 2, item)

            # Col 4
            item = QTableWidgetItem(link["msg"])
            item.setToolTip(link["msg"])

            if link["msg"] is Messages.OK:
                item.setBackground(QColor(0, 128, 0))
            else:
                item.setBackground(QColor(128, 0, 0))

            self.tableWidget.setItem(row_index, 2, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)

    def when_remove_button_clicked(self):
        pass

    def when_update_button_clicked(self):
        self.fill_data()

    def when_open_source_folder_button_clicked(self):
        pass

    def when_open_destination_folder_button_clicked(self):
        pass

if __name__ == "__main__":
    application = Application(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    application.exec_()
