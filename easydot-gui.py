#!/bin/env python3
import sys
import os
from pathlib import Path

from easydot import get_symbolics_links, Messages

from PyQt5.QtGui import QColor, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl


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
        loadUi(os.path.realpath(os.path.join(os.path.dirname(__file__), "mainwindow.ui")), self)

        self.setWindowTitle("easydot GUI - 0.1.2")

    def init_events(self):
        self.pushButton_5.clicked.connect(self.when_create_button_clicked)
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
            # Col 1
            item = QTableWidgetItem(link["msg"])
            item.setToolTip(link["msg"])
            item.setData(Qt.UserRole, link)

            if link["msg"] is Messages.OK:
                item.setBackground(QColor(0, 128, 0))
            else:
                item.setBackground(QColor(128, 0, 0))

            self.tableWidget.setItem(row_index, 0, item)

            #  Col 2
            msg = "<b>Source</b>: {}<br><b>Destination</b>: {}".format(link["src"], link["dst"])
            item = QLabel(msg)
            item.setToolTip(link["src"])
            self.tableWidget.setCellWidget(row_index, 1, item)

            # # Col 3
            # item = QTableWidgetItem(link["dst"])
            # item.setToolTip(link["dst"])
            # #item.setData(Qt.UserRole, link)
            # self.tableWidget.setItem(row_index, 2, item)


        #self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 QHeaderView.ResizeToContents)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.verticalHeader().resizeSections(QHeaderView.ResizeToContents)

    def get_current_row_data(self):
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            return selected_item.data(Qt.UserRole)
        else:
            return None

    def when_create_button_clicked(self):
        data = self.get_current_row_data()
        if data:
            os.symlink(data["src"], data["dst"])

            self.fill_data()

    def when_remove_button_clicked(self):
        data = self.get_current_row_data()
        if data:
            dst_filepath = data["dst"]
            os.remove(dst_filepath)

            self.fill_data()

    def when_update_button_clicked(self):
        self.fill_data()

    def open_folder(self, attribute):
        data = self.get_current_row_data()
        if data:
            filepath = data[attribute]
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(filepath)))

    def when_open_source_folder_button_clicked(self):
        self.open_folder("src")

    def when_open_destination_folder_button_clicked(self):
        self.open_folder("dst")

if __name__ == "__main__":
    import cgitb
    cgitb.enable(format='text')

    application = Application(sys.argv)
    mainwindow = MainWindow()
    mainwindow.move(application.desktop().screen().rect().center() - mainwindow.rect().center())
    mainwindow.show()
    application.exec_()
