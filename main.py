from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QPushButton, QLabel, QApplication, QLineEdit, QWidget
import os
import fitz
from pdf_to_text_converter import PdfToTxtConverter


def main():
    app = QApplication([])
    converter = PdfToTxtConverter()
    # Use a QTimer to schedule the conversion after the event loop starts
    # QTimer.singleShot(0, converter.convert_pdf)
    app.exec_()


if __name__ == '__main__':
    main()
