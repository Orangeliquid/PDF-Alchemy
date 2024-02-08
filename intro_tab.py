from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class IntroTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label1 = QLabel("Welcome to PDF Alchemy!\n")
        label1.setStyleSheet("font-size: 22px; font-weight: bold;")

        label2 = QLabel("Tab One is for PDF to TXT\n\n"
                        "Tab Two converts the TXT file to an MP3 for listening!\n")
        label2.setStyleSheet("font-size: 15px; font-weight: bold;")

        label3 = QLabel("Follow these steps for both tabs:")
        label3.setStyleSheet("font-size: 12px; font-weight: bold;")
        label4 = QLabel("1. Click the 'Browse' button to select a file(Tab1:PDF | Tab2:TXT)")
        label5 = QLabel("2. Enter the desired output file name (without extension).")
        label6 = QLabel("3. Click 'Convert' to perform the conversion.")
        label7 = QLabel("4. View the conversion status in the output area.")
        label8 = QLabel("5. Minimize or close the application to see the resulting file.")

        # Add labels to the layout
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(label5)
        layout.addWidget(label6)
        layout.addWidget(label7)
        layout.addWidget(label8)

        self.setLayout(layout)
