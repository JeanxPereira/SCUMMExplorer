# splash_screen.py
from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap, duration=3000):
        super().__init__(pixmap)
        self.duration = duration
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Initialize opacity
        self._opacity = 1.0
        self.setWindowOpacity(0)

        # Disable mouse events
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def show_splash(self):
        self.show()

        # Fade-in animation
        self.fade_in_animation = QPropertyAnimation(self, b"opacity")
        self.fade_in_animation.setDuration(1000)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.start()

        # Fade-out animation
        self.fade_out_animation = QPropertyAnimation(self, b"opacity")
        self.fade_out_animation.setDuration(1000)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)

        # Set a timer to trigger the fade-out animation
        QTimer.singleShot(self.duration, self.start_fade_out)

    def start_fade_out(self):
        self.fade_out_animation.start()
        # Close the splash screen after the fade-out animation is finished
        self.fade_out_animation.finished.connect(self.close)

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    def mousePressEvent(self, event):
        # Disable default "click-to-dismiss" behavior
        pass

def create_and_show_splash():
    splash_pixmap = QPixmap('res/splash.png')
    splash = SplashScreen(splash_pixmap)  # Use the custom SplashScreen class
    splash.show_splash()
    return splash
