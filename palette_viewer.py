import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen, QIcon
from PyQt6.QtCore import Qt, pyqtSignal

class PaletteLabel(QLabel):
    clicked = pyqtSignal(int)

    def __init__(self, color_index, r, g, b, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_index = color_index
        self.r = r
        self.g = g
        self.b = b  # Corrigido aqui
        self.selected = False
        self.setFixedSize(32, 32)
        self.update_pixmap()

    def update_pixmap(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(self.r, self.g, self.b))
        
        painter = QPainter(pixmap)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(0, 0, 31, 31)

        if self.selected:
            pen.setColor(QColor(255, 0, 0))
            painter.setPen(pen)
            painter.drawRect(1, 1, 29, 29)

        painter.end()
        self.setPixmap(pixmap)

    def set_selected(self, selected):
        self.selected = selected
        self.update_pixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.color_index)

class PaletteViewer(QMainWindow):
    def __init__(self, palette_data):
        super().__init__()
        self.palette_data = palette_data
        self.labels = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Palette Viewer')
        self.setGeometry(100, 100, 580, 450)

        # Set the window icon
        icon_path = os.path.join('res', 'types', 'RGBS.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        palette_widget = QWidget()
        palette_layout = QGridLayout(palette_widget)
        palette_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        palette_layout.setSpacing(4)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.on_list_item_changed)

        for i, (r, g, b) in enumerate(self.palette_data):
            label = PaletteLabel(i, r, g, b)
            label.clicked.connect(self.on_label_clicked)
            self.labels.append(label)
            palette_layout.addWidget(label, i // 12, i % 12)
            self.list_widget.addItem(f"{i:02X}: ({r:02X},{g:02X},{b:02X})")

        main_layout.addWidget(palette_widget)
        main_layout.addWidget(self.list_widget)

        self.setCentralWidget(main_widget)

    def on_list_item_changed(self, current_row):
        for label in self.labels:
            label.set_selected(label.color_index == current_row)

    def on_label_clicked(self, color_index):
        self.list_widget.setCurrentRow(color_index)

    def update_palette(self, palette_data):
        self.palette_data = palette_data
        self.initUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PaletteViewer([(i, i, i) for i in range(256)])  # Example data
    viewer.show()
    sys.exit(app.exec())
