from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt

class CustomProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # Set the maximum value using QProgressBar's setMaximum method
        self.progress_bar.setMaximum(100)

    def set_value(self, value):
        # Access the QProgressBar widget and set its value
        self.progress_bar.setValue(value)
