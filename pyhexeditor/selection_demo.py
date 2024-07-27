import sys
from PyQt5.QtCore import Qt, QRectF, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QTextCursor, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget

class RoundedSelectionTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(RoundedSelectionTextEdit, self).__init__(parent)
        self.setAcceptRichText(False)
        self.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse | Qt.TextEditable)

    def paintEvent(self, event):
        super(RoundedSelectionTextEdit, self).paintEvent(event)

        # Create a painter for custom rendering
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)

        # Get the text cursor
        cursor = self.textCursor()
        if cursor.hasSelection():
            # Get the selection range
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()

            cursor.setPosition(selection_start)
            selection_rects = []

            # Iterate over the selection to get the rectangles
            while cursor.position() < selection_end:
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor, 1)
                rect = self.cursorRect(cursor)
                selection_rects.append(rect)
                cursor.movePosition(QTextCursor.NextBlock)

            # Set the brush for rounded selection
            selection_color = QColor(0, 120, 215, 128)  # Semi-transparent blue
            painter.setBrush(QBrush(selection_color))
            painter.setPen(Qt.NoPen)

            # Draw rounded rectangles for the selection
            for rect in selection_rects:
                rounded_rect = QRectF(rect)
                rounded_rect.adjust(1, 1, -1, -1)  # Adjust to prevent border clipping
                painter.drawRoundedRect(rounded_rect, 3, 3)

        painter.end()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rounded Selection Example')

        text_edit = RoundedSelectionTextEdit()
        text_edit.setPlainText("This is an example text. Select some text to see the rounded selection effect.")

        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
