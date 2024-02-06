import PyPDF2
import pyttsx3
import tkinter as tk
from tkinter import filedialog, messagebox
import threading


class PDFReader:
    def __init__(self, root):
        self.engine = pyttsx3.init()
        self.text = ""
        self.paused = False
        self.thread = None
        self.root = root
        self.file_label = tk.Label(root, text="Selected File: None")
        self.file_label.grid(row=0, column=1, pady=10, padx=10)

    def extract_text_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    self.text += page.extract_text()
            return self.text
        except PyPDF2.utils.PdfReadError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None
        finally:
            file.close()

    def text_to_speech(self):
        self.engine.say(self.text)
        self.engine.runAndWait()

    def pause_resume(self):
        if self.paused:
            self.engine.stop()
        else:
            self.thread = threading.Thread(target=self.text_to_speech)
            self.thread.start()
            self.root.after(100, self.check_thread)

        self.paused = not self.paused

    def check_thread(self):
        if self.thread and self.thread.is_alive():
            self.root.after(100, self.check_thread)
        else:
            self.paused = True


def file_selection(pdf_reader):
    filetypes = [('PDF files', '*.pdf'), ('All files', '*.*')]
    filename = filedialog.askopenfilename(title='Open a PDF file', initialdir='/', filetypes=filetypes)

    if not filename:
        return

    pdf_reader.text = ""
    text_content = pdf_reader.extract_text_from_pdf(filename)
    if text_content:
        pdf_reader.file_label.config(text=f"Selected File: {filename}")
        messagebox.showinfo('Conversion Complete', 'Text extraction successful.')
    else:
        pdf_reader.file_label.config(text="Selected File: None")
        messagebox.showwarning('Conversion Failed', 'Text extraction failed.')


def main():
    root = tk.Tk()
    root.title("PDF -> Text-to-Speech")
    root.configure(bg='orange')
    root.geometry("420x140")

    pdf_reader = PDFReader(root)

    file_selection_button = tk.Button(root, text="File Selection", command=lambda: file_selection(pdf_reader))
    file_selection_button.grid(row=0, column=0, pady=10, padx=10)

    pause_resume_button = tk.Button(root, text="Pause/Resume", command=pdf_reader.pause_resume)
    pause_resume_button.grid(row=1, column=0, pady=10, padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()
