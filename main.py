# main.py
import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QHeaderView, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QFileDialog, QGridLayout, QGroupBox, QSplitter, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QIcon
from read_index import read_la_files, populate_tree_item
from palette_viewer import PaletteViewer
from menu import MenuBar

from splash_screen import create_and_show_splash
from options_window import OptionsWindow 

# Caminho do arquivo de configurações
CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'enable_splash_screen': True,  # Habilitado por padrão
            'enable_feature_y': False
        }

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.palette_viewer = None  # Add this line to keep a reference to the palette viewer window

    def initUI(self):
        self.setWindowTitle('SCUMM Redux')
        self.setGeometry(100, 100, 1000, 600)

        app_icon = QIcon("res/icon.ico")
        self.setWindowIcon(app_icon)

        # Add the menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left side layout for TreeView and file input
        left_layout = QVBoxLayout()

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
        self.explorer_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.explorer_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.explorer_tree.setColumnWidth(1, 100)  # Ajuste o valor conforme necessário
        self.explorer_tree.itemSelectionChanged.connect(self.update_informer)

        left_layout.addLayout(file_layout)
        left_layout.addWidget(self.explorer_tree)

        # Right side layout for Block Info and Specific Info
        right_layout = QVBoxLayout()

        # Group Box for General Block Info
        block_info_group = QGroupBox('General Block Info')
        block_info_layout = QGridLayout()

        self.type_label = QLabel('Type:')
        self.type_value = QLabel('N/A')
        
        self.offset_label = QLabel('Offset:')
        self.offset_value = QLabel('N/A')
        
        self.size_label = QLabel('Size:')
        self.size_value = QLabel('N/A')
        
        self.size_format_label = QLabel('Size Format:')
        self.size_format_value = QLabel('N/A')
        
        self.description_label = QLabel('Description:')
        self.description_value = QLabel('N/A')

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        icon_pixmap = QPixmap("res/types/Unknown.png")
        self.icon_label.setPixmap(icon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))

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
        block_info_group.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        # Group Box for Block Specific Info
        block_specific_group = QGroupBox('Block Specific Info')
        block_specific_layout = QVBoxLayout()
        self.block_specific_label = QLabel('Block Specific Info will be displayed here.')
        block_specific_layout.addWidget(self.block_specific_label)
        self.block_specific_button = QPushButton('View Palette')
        self.block_specific_button.clicked.connect(self.view_palette)
        self.block_specific_button.setVisible(False)
        block_specific_layout.addWidget(self.block_specific_button)
        block_specific_group.setLayout(block_specific_layout)
        block_specific_group.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        right_layout.addWidget(block_info_group)
        right_layout.addWidget(block_specific_group)
        right_layout.addStretch()  # Add stretch to push fixed size widgets to the top

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)

        main_layout.addWidget(main_splitter)
        self.setCentralWidget(main_widget)

        self.descriptions = self.load_descriptions()
        self.set_block_info('N/A', 0, 0, 'N/A', 'N/A')

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;LA0 Files (*.la0)")
        if file_name:
            self.input_file_edit.setText(file_name)
            self.analyze_file(file_name)

    def analyze_file(self, file_path):
        data = read_la_files(file_path)
        self.populate_tree_view(data)

    def populate_tree_view(self, data):
        self.explorer_tree.clear()
        for block_name, elements in data.items():
            for element, block_size in elements:
                item = QTreeWidgetItem(self.explorer_tree)
                item.setText(0, block_name)
                item.setText(1, str(block_size))
                item_data = (block_name, element.offset, block_size, 'Standard') if hasattr(element, 'offset') else (block_name, 0, block_size, 'Standard')
                item.setData(0, Qt.ItemDataRole.UserRole, item_data)
                if element.data:
                    item.setData(1, Qt.ItemDataRole.UserRole, element.data)
                icon_path = os.path.join('res', 'types', f"{block_name}.png")
                if os.path.exists(icon_path):
                    item.setIcon(0, QIcon(icon_path))
                for child in element.children():
                    child_size = len(child.data) if hasattr(child, 'data') else 0
                    populate_tree_item(item, child, child_size, self.set_icon_callback)

        self.explorer_tree.expandAll()

    def set_icon_callback(self, item, block_name):
        icon_path = os.path.join('res', 'types', f"{block_name}.png")
        if os.path.exists(icon_path):
            item.setIcon(0, QIcon(icon_path))

    def update_informer(self):
        selected_items = self.explorer_tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            item_data = item.data(0, Qt.ItemDataRole.UserRole)
            if item_data:
                block_type, offset, size, size_format = item_data
                description = self.descriptions.get(block_type, 'N/A')
                self.set_block_info(block_type, offset, size, size_format, description)
                if block_type in ['RGBS', 'AKPL']:
                    self.block_specific_button.setVisible(True)
                else:
                    self.block_specific_button.setVisible(False)
            else:
                self.set_block_info('N/A', 0, 0, 'N/A', 'N/A')
        else:
            self.set_block_info('N/A', 0, 0, 'N/A', 'N/A')

    def set_block_info(self, block_type, offset, size, size_format, description='N/A'):
        self.type_value.setText(block_type)
        self.offset_value.setText(f'{offset} (0x{offset:08X})')
        self.size_value.setText(f'{size} (0x{size:08X})')
        self.size_format_value.setText(size_format)
        self.description_value.setText(description)

        icon_path = f'res/types/{block_type}.png'
        if os.path.exists(icon_path):
            self.icon_label.setPixmap(QPixmap(icon_path).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.icon_label.setPixmap(QPixmap("res/types/Unknown.png").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))

    def load_descriptions(self):
        descriptions = {}
        descriptions_file = os.path.join('res', 'descriptions.json')
        if os.path.exists(descriptions_file):
            with open(descriptions_file, 'r', encoding='utf-8') as file:
                descriptions = json.load(file)
        return descriptions
    
    def extract_palette_data(self, item):
        block_type = item.text(0)
        if block_type == 'AKPL':
            data = item.data(1, Qt.ItemDataRole.UserRole)
            palette_data = [tuple(data[i:i + 3]) for i in range(0, len(data), 3)]
        elif block_type == 'RGBS':
            data = item.data(1, Qt.ItemDataRole.UserRole)
            palette_data = [tuple(data[i:i + 3]) for i in range(0, len(data), 3)]
        else:
            palette_data = [(i, i, i) for i in range(256)]  # Default example palette data
        return palette_data


    def view_palette(self):
        selected_items = self.explorer_tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            item_data = item.data(0, Qt.ItemDataRole.UserRole)
            if item_data:
                block_type, offset, size, size_format = item_data
                if block_type in ['RGBS', 'APAL']:
                    palette_data = self.extract_palette_data(item)
                    if self.palette_viewer is None:
                        self.palette_viewer = PaletteViewer(palette_data)
                    else:
                        self.palette_viewer.update_palette(palette_data)
                    self.palette_viewer.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    config = load_config()

    splash_duration = 1000  # Duração em milissegundos (por exemplo, 3 segundos)

    if config.get('enable_splash_screen', True):
        splash = create_and_show_splash()  # Criação da splash screen
        main_window = MainWindow()
        QTimer.singleShot(splash_duration, splash.close)
        QTimer.singleShot(splash_duration, main_window.show)
    else:
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec())
