import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QFileDialog, QTabWidget, QTreeWidget, QTreeWidgetItem, QSplitter, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from nutcracker.sputm.tree import open_game_resource
from nutcracker.sputm.schema import SCHEMA


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SCUMM Revisited')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # File Input Layout
        file_layout = QHBoxLayout()
        self.input_file_edit = QLineEdit()
        browse_button = QPushButton('Browse...')
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(QLabel('Input File:'))
        file_layout.addWidget(self.input_file_edit)
        file_layout.addWidget(browse_button)

        # TreeView for Explorer
        self.explorer_tree = QTreeWidget()
        self.explorer_tree.setColumnCount(2)
        self.explorer_tree.setHeaderLabels(['Block Name', 'Size'])

        # General Block Info
        block_info_group = QGroupBox('General Block Info')
        block_info_layout = QGridLayout()

        self.type_label = QLabel('Type:')
        self.type_value = QLabel('DCOS')

        self.offset_label = QLabel('Offset:')
        self.offset_value = QLabel('8358 (0x000020A6)')

        self.size_label = QLabel('Size:')
        self.size_value = QLabel('2242 (0x000008C2)')

        self.size_format_label = QLabel('Size Format:')
        self.size_format_value = QLabel('Standard')

        self.description_label = QLabel('Description:')
        self.description_value = QLabel('Directory of Costumes')

        # Placeholder for icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        icon_pixmap = QPixmap("icons/types/DCOS.png")
        self.icon_label.setPixmap(icon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))

        # Add labels and values to the layout
        block_info_layout.addWidget(self.type_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.type_value, 0, 1, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.offset_label, 1, 0, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.offset_value, 1, 1, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.size_label, 2, 0, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.size_value, 2, 1, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.size_format_label, 3, 0, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.size_format_value, 3, 1, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.description_label, 4, 0, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.description_value, 4, 1, Qt.AlignmentFlag.AlignLeft)
        block_info_layout.addWidget(self.icon_label, 0, 2, 5, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        block_info_group.setLayout(block_info_layout)

        # Main Layout Adjustments
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.explorer_tree)
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(block_info_group)
        right_widget.setLayout(right_layout)

        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)

        main_layout.addLayout(file_layout)
        main_layout.addWidget(main_splitter)

        self.setCentralWidget(main_widget)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;LA0 Files (*.la0)")
        if file_name:
            self.input_file_edit.setText(file_name)
            print(f"File selected: {file_name}")
            self.analyze_file(file_name)

    def analyze_file(self, file_path):
        print(f"Analyzing file: {file_path}")
        data = self.read_la0(file_path)
        print(f"Data read: {data}")  # Debug print
        self.populate_tree_view(data)

    def read_la0(self, file_path):
        try:
            print(f"Opening game resource from: {file_path}")
            gameres = open_game_resource(Path(file_path))
            resources = gameres.read_resources()
            data_dict = {}
            for resource in resources:
                block_name = resource.__class__.__name__
                block_size = resource._block.size
                print(f"Block Name: {block_name}, Block Size: {block_size}")  # Debug print
                if block_name not in data_dict:
                    data_dict[block_name] = 0
                data_dict[block_name] += block_size
            return data_dict
        except Exception as e:
            print(f"Error reading LA0 file: {e}")
            return {}

    def populate_tree_view(self, data):
        self.explorer_tree.clear()  # Clear existing items
        root = QTreeWidgetItem(self.explorer_tree)
        root.setText(0, "Root")
        for key, value in data.items():
            print(f"Adding item to tree: {key} - {value}")  # Debug print
            item = QTreeWidgetItem(root)
            item.setText(0, key)
            item.setText(1, str(value))
        root.setExpanded(True)  # Expand the root item to show its children
        self.explorer_tree.expandAll()  # Ensure all items are expanded


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
