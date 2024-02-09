from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QProgressBar, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QTimer, Qt
import os
from gtts import gTTS
from custom_widgets import CustomProgressBar


class TxtToMp3ConversionTab(QWidget):
    def __init__(self):
        super().__init__()

        self.lbl_file = QLabel('Selected TXT file:', self)
        self.lbl_file.setGeometry(20, 40, 300, 20)
        self.lbl_file.setStyleSheet("color: Black; font-weight: Bold;")

        self.file_path_display = QLineEdit(self)
        self.file_path_display.setGeometry(20, 70, 300, 20)
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setStyleSheet("color: Black; font-weight: Bold;")

        self.btn_browse = QPushButton('Browse', self)
        self.btn_browse.setGeometry(20, 100, 80, 30)
        self.btn_browse.clicked.connect(self.browse_txt)
        self.btn_browse.setStyleSheet("background-color: Black; color: Orange; font-weight: Bold;")

        self.lbl_output = QLabel('After pressing "Convert"\n'
                                 'Enter the output file name (without extension):', self)
        self.lbl_output.setGeometry(20, 150, 300, 40)
        self.lbl_output.setStyleSheet("color: Black; font-weight: Bold;")

        self.txt_output = QLabel(self)
        self.txt_output.setGeometry(20, 200, 400, 35)
        self.txt_output.setStyleSheet("color: Black; font-weight: Bold;")

        self.btn_convert = QPushButton('Convert', self)
        self.btn_convert.setGeometry(20, 265, 80, 30)
        self.btn_convert.clicked.connect(self.convert_to_mp3)
        self.btn_convert.setStyleSheet("background-color: Black; color: Orange; font-weight: Bold;")

        # Create a custom progress bar
        self.progressBar = CustomProgressBar(self)
        self.progressBar.setGeometry(100, 240, 300, 80)
        self.progressBar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; background: white; text-align: center; } "
            "QProgressBar::chunk { background-color: cyan; }"
                                      )

        self.lbl_warning = QLabel('Please wait for conversion to finish.\n'
                                  'This can take some time.', self)
        self.lbl_warning.setGeometry(20, 295, 300, 30)
        self.lbl_warning.setStyleSheet("color: Black; font-weight: Bold;")
        self.txt_file_path = None
        self.mp3_file_path = None
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: Orange;")
        self.show()

    def browse_txt(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open TXT File', '', 'Text Files (*.txt);;All Files (*)',
                                                   options=options)

        if file_path:
            self.txt_file_path = file_path
            self.file_path_display.setText(file_path)
            self.lbl_file.setToolTip(file_path)  # Display full path in tooltip
            self.txt_output.setText('')

    def convert_to_mp3(self):
        print("convert_to_mp3 method called")
        print(f"self.txt_file_path: {self.txt_file_path}")

        if self.txt_file_path:
            text_to_convert = self.read_txt_file()

            if text_to_convert:
                output_name, ok = QFileDialog.getSaveFileName(self, 'Save as MP3 File',
                                                              os.path.join(os.getcwd(), 'output.mp3'),
                                                              'MP3 Files (*.mp3);;All Files (*)')
                if ok and output_name:
                    output_name = output_name.split('.')[0]  # Remove the extension if the user adds it

                    try:
                        tts = gTTS(text=text_to_convert, lang='en', slow=False)
                        total_chars = len(text_to_convert)
                        chunk_size = 500  # Choose an appropriate chunk size
                        num_chunks = total_chars // chunk_size
                        self.progressBar.progress_bar.setMaximum(num_chunks)

                        chunk_files = []

                        # Save the MP3 file in chunks to update the progress bar
                        for i in range(0, total_chars, chunk_size):
                            tts_chunk = gTTS(text=text_to_convert[i:i + chunk_size], lang='en', slow=False)
                            chunk_file_path = output_name + '_chunk{}.mp3'.format(i // chunk_size)
                            tts_chunk.save(chunk_file_path)
                            chunk_files.append(chunk_file_path)
                            self.progressBar.set_value(i // chunk_size + 1)
                            QCoreApplication.processEvents()

                        # Combine the chunks
                        combined_output_path = os.path.join(os.getcwd(), output_name + '.mp3')
                        with open(combined_output_path, 'wb') as output_file:
                            for chunk_file in chunk_files:
                                with open(chunk_file, 'rb') as chunk:
                                    output_file.write(chunk.read())

                        # Remove the chunk files
                        for chunk_file in chunk_files:
                            os.remove(chunk_file)

                        self.mp3_file_path = combined_output_path  # Update the mp3_file_path attribute
                        self.txt_output.setText(os.path.basename(self.mp3_file_path))

                        # Use QTimer to delay the display of the success message
                        QTimer.singleShot(0, lambda: self.show_success_message(output_name))

                    except Exception as e:
                        print(f"Error during text-to-speech conversion: {e}")
                        self.txt_output.setText(
                            'Error during text-to-speech conversion. Check the console for details.')
                    finally:
                        self.progressBar.setValue(0)

    def read_txt_file(self):
        try:
            with open(self.txt_file_path, 'r', encoding='utf-8') as txt_file:
                return txt_file.read()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return None

    def show_success_message(self, output_name):
        self.txt_output.setText(f'Conversion successful! Saved as: {os.path.basename(output_name)}.mp3\n'
                                f'Refresh the file explorer or navigate to the directory to see the file!')
        self.progressBar.setValue(0)
