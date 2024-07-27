from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout
import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'enable_splash_screen': True,
            'enable_feature_y': False
        }

class OptionsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setGeometry(100, 100, 300, 200)

        self.config = load_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.option1 = QCheckBox("Enable Splash Screen")
        self.option1.setChecked(self.config.get('enable_splash_screen', True))
        self.option2 = QCheckBox("Enable feature Y")
        self.option2.setChecked(self.config.get('enable_feature_y', False))

        layout.addWidget(self.option1)
        layout.addWidget(self.option2)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.save_options)
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def save_options(self):
        self.config['enable_splash_screen'] = self.option1.isChecked()
        self.config['enable_feature_y'] = self.option2.isChecked()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)
        self.accept()

    def get_options(self):
        return {
            'enable_splash_screen': self.option1.isChecked(),
            'enable_feature_y': self.option2.isChecked()
        }
