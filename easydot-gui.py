#!/bin/env python3
import json
import sys
import os
from pathlib import Path

import easydot

from PyQt6.QtGui import QColor, QDesktopServices
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QTreeWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.expanded_list = False

        self.init_ui()
        self.init_events()
        self.config = self.load_or_create_config_file()
        self.fill_data()

    def init_ui(self):
        loadUi(os.path.realpath(os.path.join(os.path.dirname(__file__), "mainwindow.ui")), self)

        self.setWindowTitle("easydot GUI - 0.2.3")

    def init_events(self):
        self.pushButton_5.clicked.connect(self.when_create_button_clicked)
        self.pushButton.clicked.connect(self.when_remove_button_clicked)
        self.pushButton_2.clicked.connect(self.when_update_button_clicked)
        self.pushButton_3.clicked.connect(self.when_open_source_folder_button_clicked)
        self.pushButton_4.clicked.connect(self.when_open_destination_folder_button_clicked)
        self.pushButton_7.clicked.connect(self.when_expand_button_clicked)

    def load_or_create_config_file(self):
        homepath = Path.home()
        config_filepath = os.path.join(homepath, ".easydot.json")
        if os.path.isfile(config_filepath):
            with open(config_filepath) as config_file:
                config = json.load(config_file)

                if not os.path.isdir(config["path"]):
                    config["path"] = os.path.join(homepath, config["path"])

            return config
        else:
            DEFAULT_CONFIG = {"path": os.path.join(homepath, "Dotfiles")}
            return DEFAULT_CONFIG

    def fill_data(self):
        if not self.treeWidget:
            self.treeWidget = QTreeWidget()

        self.treeWidget.clear()

        path = self.config["path"]
        softwares = easydot.get_softwares(path)

        for software_index, software in enumerate(softwares):
            activated_links_count = 0

            software_path = os.path.join(path, software)
            links = list(easydot.browse_software_files(software_path))

            self.treeWidget.insertTopLevelItem(software_index, QTreeWidgetItem(None))
            software_node = self.treeWidget.topLevelItem(software_index)

            for link in links:
                msg = link["src"] + " -> " + link["dst"]

                color = QColor(0, 128, 0) if link["msg"] is easydot.Messages.OK else QColor(128, 0, 0)
                item = QTreeWidgetItem(None, [msg])
                item.setData(0, Qt.ItemDataRole.UserRole, link)
                item.setBackground(0, color)
                software_node.addChild(item)

                if link["msg"] is easydot.Messages.OK:
                    activated_links_count += 1

            software_name = "{} [{}/{} actif]".format(software, activated_links_count, len(links))
            software_node.setText(0, software_name)

        self.expanded_or_collapse()

    def get_current_row_data(self):
        selected_item = self.treeWidget.currentItem()
        if selected_item:
            return selected_item.data(0, Qt.ItemDataRole.UserRole)
        else:
            return None

    def when_create_button_clicked(self):
        data = self.get_current_row_data()
        if data:
            dst_folder = os.path.dirname(data["dst"])
            if not os.path.isdir(dst_folder):
                os.makedirs(dst_folder)

            elif os.path.isfile(data["dst"]):
                os.remove(data["dst"])

            os.symlink(data["src"], data["dst"])

            self.fill_data()

    def when_remove_button_clicked(self):
        data = self.get_current_row_data()
        if data:
            if os.path.isfile(data["dst"]):
                dst_filepath = data["dst"]
                os.remove(dst_filepath)

                self.fill_data()

    def when_update_button_clicked(self):
        self.fill_data()

    def when_expand_button_clicked(self):
        self.expanded_list = not self.expanded_list
        self.expanded_or_collapse()

    def expanded_or_collapse(self):
        if self.expanded_list:
            self.treeWidget.expandAll()
        else:
            self.treeWidget.collapseAll()

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
    application = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    application.exec()
