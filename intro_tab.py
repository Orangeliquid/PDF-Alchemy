from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class IntroTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label1 = QLabel("Welcome to PDF Alchemy!\n")
        label1.setStyleSheet("font-size: 35px; font-weight: bold;")

        label2 = QLabel("Tab One is for PDF to TXT\n\n"
                        "Tab Two converts the TXT file to an MP3 for listening!\n")
        label2.setStyleSheet("font-size: 20px; font-weight: bold;")

        label3 = QLabel("Follow these steps for both tabs:")
        label3.setStyleSheet("font-size: 17px; font-weight: bold;")

        label4 = QLabel("1. Click the 'Browse' button to select a file -> Tab1: .PDF | Tab2: .TXT")
        label4.setStyleSheet("font-size: 15px; font-weight: italic;")

        label5 = QLabel("2. Enter the desired output file name (without extension).")
        label5.setStyleSheet("font-size: 15px; font-weight: italic;")

        label6 = QLabel("3. Click 'Convert' to perform the conversion.")
        label6.setStyleSheet("font-size: 15px; font-weight: italic;")

        label7 = QLabel("4. View the conversion status in the output area.")
        label7.setStyleSheet("font-size: 15px; font-weight: italic;")

        label8 = QLabel("(If using TXT to MP3 the loading bar will indicate status of conversion.\n"
                        "This can take some time depending on the size of the TXT file)")
        label8.setStyleSheet("font-weight: Bold;")

        label9 = QLabel("5. Minimize or close the application to see the resulting file.")
        label9.setStyleSheet("font-size: 15px; font-weight: italic;")

        # Add labels to the layout
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(label5)
        layout.addWidget(label6)
        layout.addWidget(label7)
        layout.addWidget(label8)
        layout.addWidget(label9)

        self.setLayout(layout)
