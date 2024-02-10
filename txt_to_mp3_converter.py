from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, QTimer, QThread, pyqtSignal, Qt
import os
from gtts import gTTS
from custom_widgets import CustomProgressBar


class Mp3ConversionWorker(QThread):
    progress_update = pyqtSignal(int)

    def __init__(self, text_to_convert, chunk_size):
        super().__init__()
        self.last_progress_value = None
        self.error_message = None
        self.output_path = None
        self.text_to_convert = text_to_convert
        self.chunk_size = chunk_size

    # When stopping application before conversion is complete the output chunks are left in working directory
    # This needs to be addressed seeing as it is not a function we want and is annoying for user
    # Additionally I need to allow the user to enter a name for the new mp3 file instead of output.mp3
    def run(self):
        try:
            tts = gTTS(text=self.text_to_convert, lang='en', slow=False)  # May be able to remove - unused
            total_chars = len(self.text_to_convert)
            num_chunks = total_chars // self.chunk_size  # May be able to remove - unused
            self.progress_update.emit(0)

            chunk_files = []
            success = True  # Flag to track if the conversion is successful

            # Save the MP3 file in chunks to update the progress bar
            for i in range(0, total_chars, self.chunk_size):
                if not success:
                    break

                tts_chunk = gTTS(text=self.text_to_convert[i:i + self.chunk_size], lang='en', slow=False)
                chunk_file_path = 'output_chunk{}.mp3'.format(i // self.chunk_size)
                tts_chunk.save(chunk_file_path)
                chunk_files.append(chunk_file_path)

                # Emit progress only when the value changes
                progress_value = min((i + self.chunk_size) * 100 // total_chars, 100)
                if progress_value != self.last_progress_value:
                    self.progress_update.emit(progress_value)
                    self.last_progress_value = progress_value

                    QCoreApplication.processEvents()

            if success:
                # Combine the chunks
                combined_output_path = 'output.mp3'
                with open(combined_output_path, 'wb') as output_file:
                    for chunk_file in chunk_files:
                        with open(chunk_file, 'rb') as chunk:
                            output_file.write(chunk.read())

                self.output_path = combined_output_path

                # Remove the chunk files
                for chunk_file in chunk_files:
                    os.remove(chunk_file)

        except Exception as e:
            success = False
            self.error_message = f"Error during text-to-speech conversion: {e}"

        finally:
            if not success:
                # If the conversion was not successful, delete the intermediate chunk files
                for chunk_file in chunk_files:
                    os.remove(chunk_file)


class TxtToMp3ConversionTab(QWidget):
    def __init__(self):
        super().__init__()

        self.lbl_file = QLabel('Selected TXT file:', self)
        self.lbl_file.setGeometry(20, 20, 300, 20)
        self.lbl_file.setStyleSheet("font-size: 15px; color: Black; font-weight: Bold;")

        self.file_path_display = QLineEdit(self)
        self.file_path_display.setGeometry(20, 50, 500, 30)
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setStyleSheet("font-size: 12px; font-weight:Bold; color: Black;")

        self.btn_browse = QPushButton('Browse', self)
        self.btn_browse.setGeometry(20, 100, 100, 30)
        self.btn_browse.clicked.connect(self.browse_txt)
        self.btn_browse.setStyleSheet("font-size: 15px; background-color: Black; color: Cyan; font-weight: Bold;")

        self.browse_hint = QLabel('<--- Select TXT file to convert to MP3', self)
        self.browse_hint.setGeometry(130, 95, 350, 40)
        self.browse_hint.setStyleSheet("font-size: 15px; color: Black; font-weight: Bold;")

        self.lbl_output = QLabel('After pressing "Convert"\n'
                                 'Enter the output file name (without extension):', self)
        self.lbl_output.setGeometry(20, 170, 350, 40)
        self.lbl_output.setStyleSheet("font-size: 15px; color: Black; font-weight: Bold;")

        self.btn_convert = QPushButton('Convert', self)
        self.btn_convert.setGeometry(20, 230, 100, 30)
        self.btn_convert.clicked.connect(self.convert_to_mp3)
        self.btn_convert.setStyleSheet("font-size: 15px; background-color: Black; color: Cyan; font-weight: Bold;")

        # Create a custom progress bar
        self.progressBar = CustomProgressBar(self)
        self.progressBar.setGeometry(120, 197, 400, 100)
        self.progressBar.setStyleSheet(
            "QProgressBar { border: 3px solid grey; border-radius: 3px; background: white; text-align: center; } "
            "QProgressBar::chunk { background-color: Cyan; }"
        )

        self.lbl_warning = QLabel('Please wait for conversion to finish.\n'
                                  'This can take some time depending on TXT file size!', self)
        self.lbl_warning.setGeometry(150, 260, 400, 70)
        self.lbl_warning.setStyleSheet("color: Black; font-size:13px; font-weight: Bold;")

        self.txt_output = QLabel(self)
        self.txt_output.setGeometry(20, 350, 500, 100)
        self.txt_output.setStyleSheet("color: Cyan; font-weight: Italic;")

        self.txt_file_path = None
        self.mp3_file_path = None
        self.setup_ui()

        self.chunk_size = 500
        self.worker = None

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
        if self.txt_file_path:
            text_to_convert = self.read_txt_file()

            if text_to_convert:
                self.worker = Mp3ConversionWorker(text_to_convert, self.chunk_size)
                self.worker.progress_update.connect(self.progressBar.set_value)
                self.worker.finished.connect(self.show_success_message)
                self.worker.start()

    def show_success_message(self):
        if hasattr(self.worker, 'output_path') and self.worker.output_path:
            self.mp3_file_path = self.worker.output_path
            self.txt_output.setText(os.path.basename(self.mp3_file_path))

            self.lbl_warning.setText('Conversion successful! Saved as: {}\n'
                                     'Refresh the file explorer or navigate to the directory to see the file!'
                                     .format(os.path.basename(self.worker.output_path)))
        elif hasattr(self.worker, 'error_message') and self.worker.error_message:
            self.txt_output.setText('Error during text-to-speech conversion. Check the console for details.')
            print(self.worker.error_message)
        else:
            self.txt_output.setText('Conversion aborted.')
        self.progressBar.setValue(0)

    def read_txt_file(self):
        try:
            with open(self.txt_file_path, 'r', encoding='utf-8') as txt_file:
                return txt_file.read()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return None
