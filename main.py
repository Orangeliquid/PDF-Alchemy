from PyQt5.QtWidgets import QFileDialog, QPushButton, QLabel, QApplication, QLineEdit, QWidget
import os
import fitz


class PdfToTxtConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle('PDF Alchemy')

        self.lbl_file = QLabel('Selected PDF file:', self)
        self.lbl_file.setGeometry(20, 40, 300, 20)

        self.file_path_display = QLineEdit(self)
        self.file_path_display.setGeometry(20, 70, 300, 20)
        self.file_path_display.setReadOnly(True)

        self.btn_browse = QPushButton('Browse', self)
        self.btn_browse.setGeometry(20, 100, 80, 30)
        self.btn_browse.clicked.connect(self.browsePDF)

        self.lbl_output = QLabel('Enter the output file name (without extension):', self)
        self.lbl_output.setGeometry(20, 150, 300, 20)

        self.txt_output = QLabel(self)
        self.txt_output.setGeometry(20, 180, 300, 20)

        self.btn_convert = QPushButton('Convert', self)
        self.btn_convert.setGeometry(20, 210, 80, 30)
        self.btn_convert.clicked.connect(self.convertPDF)

        self.show()

    def browsePDF(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open PDF File', '', 'PDF Files (*.pdf);;All Files (*)',
                                                   options=options)

        if file_path:
            self.pdf_file_path = file_path
            self.file_path_display.setText(file_path)
            self.lbl_file.setToolTip(file_path)  # Display full path in tooltip
            self.txt_output.setText('')

    def convertPDF(self):
        if hasattr(self, 'pdf_file_path'):
            output_name, ok = QFileDialog.getSaveFileName(self, 'Save as TXT File',
                                                          os.path.join(os.getcwd(), 'output.txt'),
                                                          'Text Files (*.txt);;All Files (*)')
            if ok and output_name:
                output_name = output_name.split('.')[0]  # Remove the extension if the user adds it

                pdf_document = None

                try:
                    pdf_document = fitz.open(self.pdf_file_path)
                    with open(output_name + '.txt', 'w', encoding='utf-8') as txt_file:
                        for page_number in range(pdf_document.page_count):
                            page = pdf_document[page_number]
                            text = page.get_text()
                            txt_file.write(text)

                    self.txt_output.setText(f'Conversion successful! Saved as: {output_name}.txt')
                except Exception as e:
                    print(f"Error during PDF conversion: {e}")
                    self.txt_output.setText(f'Error during PDF conversion. Please check the console for details.')
                finally:
                    if pdf_document:
                        pdf_document.close()
            else:
                self.txt_output.setText('Please provide a valid output file name.')
        else:
            self.txt_output.setText('Please select a PDF file first.')


if __name__ == '__main__':
    app = QApplication([])
    converter = PdfToTxtConverter()
    app.exec_()
