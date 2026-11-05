import os

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber with fallback to pypdf."""
    text = ""
    # Try pdfplumber first
    if pdfplumber is not None:
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text.strip()
        except Exception:
            pass

    # Fallback to pypdf
    if PdfReader is not None:
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                return text.strip()
        except Exception:
            pass

    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a Word .docx file including paragraphs and tables."""
    if docx is None:
        return "Word (.docx) extraction requires python-docx package."

    try:
        doc = docx.Document(file_path)
        full_text = []

        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())

        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    full_text.append(" | ".join(row_text))

        return "\n".join(full_text)
    except Exception as e:
        return f"Error extracting text from DOCX: {str(e)}"


def extract_text_from_file(file_path: str) -> str:
    """Universal text extractor supporting PDF, DOCX, and TXT files."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    else:
        # Attempt fallback to PDF then DOCX
        pdf_res = extract_text_from_pdf(file_path)
        if pdf_res:
            return pdf_res
        return extract_text_from_docx(file_path)
