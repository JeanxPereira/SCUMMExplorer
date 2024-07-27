from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel, QMessageBox
from PyQt6.QtGui import QColor
import sys

class ColorOpacityCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculadora de Cor e Opacidade')

        layout = QVBoxLayout()

        self.black_color_btn = QPushButton('Selecione a cor sobre fundo preto')
        self.black_color_btn.clicked.connect(self.select_black_color)
        layout.addWidget(self.black_color_btn)

        self.black_color_label = QLabel('Cor sobre fundo preto: #000000')
        layout.addWidget(self.black_color_label)

        self.white_color_btn = QPushButton('Selecione a cor sobre fundo branco')
        self.white_color_btn.clicked.connect(self.select_white_color)
        layout.addWidget(self.white_color_btn)

        self.white_color_label = QLabel('Cor sobre fundo branco: #FFFFFF')
        layout.addWidget(self.white_color_label)

        self.calc_btn = QPushButton('Calcular')
        self.calc_btn.clicked.connect(self.calculate_color_and_opacity)
        layout.addWidget(self.calc_btn)

        self.result_label = QLabel('Resultado: ')
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.black_color = QColor(0, 0, 0)
        self.white_color = QColor(255, 255, 255)

    def select_black_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.black_color = color
            self.black_color_label.setText(f'Cor sobre fundo preto: {color.name()}')

    def select_white_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.white_color = color
            self.white_color_label.setText(f'Cor sobre fundo branco: {color.name()}')

    def calculate_color_and_opacity(self):
        Rk = self.black_color.red()
        Gk = self.black_color.green()
        Bk = self.black_color.blue()

        Rw = self.white_color.red()
        Gw = self.white_color.green()
        Bw = self.white_color.blue()

        try:
            # Cálculos para encontrar a opacidade (X)
            numerator = -3100
            denominator = (Rw - 255)
            X = numerator / denominator

            # Cálculos para encontrar os valores RGB da cor desejada
            Rt = (Rk * 100) / X
            Gt = (Gk * 100) / X
            Bt = (Bk * 100) / X

            # Converte a opacidade para um valor entre 0 e 255
            alpha = int(X * 2.55)

            # Converte os valores RGB para hexadecimal
            hex_color = "#{:02X}{:02X}{:02X}{:02X}".format(int(Rt), int(Gt), int(Bt), alpha)

            # Exibição dos resultados
            self.result_label.setText(f'Cor com opacidade: {hex_color}')
        except ZeroDivisionError:
            QMessageBox.critical(self, "Erro", "Erro nos cálculos. Verifique os valores inseridos.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorOpacityCalculator()
    ex.show()
    sys.exit(app.exec())
