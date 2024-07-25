import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QWidget, QVBoxLayout,
                             QTabWidget, QMenuBar, QStatusBar, QSplitter, QFormLayout, QLineEdit, QDesktopWidget)
from PyQt5.QtCore import Qt
from menu import create_menus
from widgets import create_main_widget
from readLA import read_la_file

SETTINGS_FILE = "settings.json"

class ScummRevisitedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('SCUMM Revisited')
        self.resize(800, 640)
        self.center()

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        create_menus(self, self.menubar)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
        main_widget, self.file_view = create_main_widget(self)
        informer_widget = self.create_informer_widget()
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(main_widget)
        splitter.addWidget(informer_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(splitter)
        container.setLayout(container_layout)
        self.setCentralWidget(container)
        
        self.file_view.itemClicked.connect(self.on_item_clicked)
        self.file_view.currentItemChanged.connect(self.on_item_clicked)

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                (screen.height() - size.height()) // 2)

        
    def create_informer_widget(self):
        tab_widget = QTabWidget()

        self.general_tab = QWidget()
        self.general_layout = QFormLayout()
        self.type_label = QLineEdit()
        self.type_label.setReadOnly(True)
        self.offset_label = QLineEdit()
        self.offset_label.setReadOnly(True)
        self.size_label = QLineEdit()
        self.size_label.setReadOnly(True)
        self.description_label = QLineEdit()
        self.description_label.setReadOnly(True)
        self.general_layout.addRow("Type:", self.type_label)
        self.general_layout.addRow("Offset:", self.offset_label)
        self.general_layout.addRow("Size:", self.size_label)
        self.general_layout.addRow("Description:", self.description_label)
        self.general_tab.setLayout(self.general_layout)
        
        self.annotator_tab = QWidget()
        self.annotator_layout = QVBoxLayout()
        self.annotator_tab.setLayout(self.annotator_layout)
        
        self.block_info_tab = QWidget()
        self.block_info_layout = QVBoxLayout()
        self.block_info_tab.setLayout(self.block_info_layout)
        
        tab_widget.addTab(self.general_tab, "General")
        tab_widget.addTab(self.annotator_tab, "Annotator")
        tab_widget.addTab(self.block_info_tab, "Block Specific Info")

        return tab_widget

    def open_file(self):
        options = QFileDialog.Options()
        directory = self.settings.get("last_open_directory", "")
        file_name, _ = QFileDialog.getOpenFileName(self, "Open LA File", directory, "LA Files (*.LA0 *.LA1 *.LA2);;All Files (*)", options=options)
        if file_name:
            self.settings["last_open_directory"] = os.path.dirname(file_name)  # Update directory
            self.update_recent_files(file_name)
            self.save_settings()
            self.populate_tree(file_name)

    def populate_tree(self, file_name):
        blocks = read_la_file(file_name)
        self.file_view.clear()
        for block in blocks:
            block_item = QTreeWidgetItem([block['type'], str(block['size'])])
            self.file_view.addTopLevelItem(block_item)
            block_item.setData(0, Qt.UserRole, block)

            for sub_block in block.get('sub_blocks', []):
                sub_block_item = QTreeWidgetItem([sub_block['type'], str(sub_block['size'])])
                block_item.addChild(sub_block_item)
                sub_block_item.setData(0, Qt.UserRole, sub_block)

                for chunk in sub_block.get('chunks', []):
                    chunk_item = QTreeWidgetItem([chunk['type'], str(chunk['size'])])
                    sub_block_item.addChild(chunk_item)
                    chunk_item.setData(0, Qt.UserRole, chunk)

    def on_item_clicked(self, item):
        if item:
            data = item.data(0, Qt.UserRole)
            if data:
                self.update_general_tab(data)
    
    def update_general_tab(self, block):
        self.type_label.setText(block['type'])
        self.offset_label.setText(f"{block.get('offset', 0)} (0x{block.get('offset', 0):08X})")
        self.size_label.setText(f"{block['size']} (0x{block['size']:08X})")
        self.description_label.setText(block.get('description', 'No description available'))

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"last_open_directory": "", "recent_files": []}
        except json.JSONDecodeError:
            print("Error decoding JSON from settings file.")
            return {"last_open_directory": "", "recent_files": []}


    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as file:
                json.dump(self.settings, file)
        except IOError:
            print("Error saving settings.")

    def update_recent_files(self, file_name):
        recent_files = self.settings.get("recent_files", [])
        if file_name not in recent_files:
            recent_files.insert(0, file_name)
            if len(recent_files) > 8:
                recent_files.pop()
        self.settings["recent_files"] = recent_files

def main():
    app = QApplication(sys.argv)
    ex = ScummRevisitedApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
