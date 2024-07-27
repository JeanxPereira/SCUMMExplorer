from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction

from options_window import OptionsWindow 

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        file_menu = self.addMenu("File")
        settings_menu = self.addMenu("Settings")
        help_menu = self.addMenu("Help")

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.parent.browse_file)
        file_menu.addAction(open_action)

        options_action = QAction("Options", self)
        options_action.triggered.connect(self.show_options)
        settings_menu.addAction(options_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_options(self):
        options_window = OptionsWindow(self.parent)
        options_window.exec()

    def show_about(self):
        pass  # Implement About dialog if needed
