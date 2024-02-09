from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from intro_tab import IntroTab
from pdf_to_text_converter import PdfToTxtConversionTab
from txt_to_mp3_converter import TxtToMp3ConversionTab


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 200, 425, 400)
        self.setWindowTitle('PDF Alchemy')

        icon_path = 'Orange_Alchemy.PNG'
        self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet("background-color: Orange;")

        # Create an instance of IntroTab
        intro_tab = IntroTab()

        # Create an instance of PdfToTxtConversionTab
        pdf_to_txt_tab = PdfToTxtConversionTab()

        # Create an instance of
        txt_to_mp3_tab = TxtToMp3ConversionTab()

        # Create a tab widget
        tab_widget = QTabWidget(self)
        tab_widget.addTab(intro_tab, 'Introduction')
        tab_widget.addTab(pdf_to_txt_tab, 'PDF -> TXT')
        tab_widget.addTab(txt_to_mp3_tab, 'TXT -> MP3')

        # Apply styles to the QTabBar (tabs)
        tab_widget.setStyleSheet(
            "QTabBar::tab { min-width: 100px; min-height: 50px; }"  # Adjust the values as needed
            "QTabBar::tab:selected { background-color: cyan; color: Black; font-weight: bold; }"
            "QTabBar::tab:!selected { background-color: LightGray; color: Black; font-weight: normal; }"
        )

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication([])
    main_app = MainApplication()
    main_app.show()
    app.exec_()
