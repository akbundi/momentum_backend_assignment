import os
from docx import Document  # For reading .doc files
import PyPDF2  # For reading .pdf files

class FileHandler:
    def read_file(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension == ".txt":
            return self._read_txt(file_path)
        elif extension == ".pdf":
            return self._read_pdf(file_path)
        elif extension == ".docx":
            return self._read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    def _read_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
            return content

    def _read_docx(self, file_path):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
