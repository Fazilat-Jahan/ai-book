from typing import List
from pypdf import PdfReader
from markdown_it import MarkdownIt

def _parse_pdf(file_path: str) -> str:
    """Parses a PDF file and returns its text content."""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def _parse_markdown(file_path: str) -> str:
    """Parses a Markdown file and returns its text content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        md = MarkdownIt()
        text = md.render(content)
    return text

def parse_document(file_path: str) -> str:
    """
    Parses a document (PDF or Markdown) and returns its text content.
    """
    if file_path.lower().endswith('.pdf'):
        return _parse_pdf(file_path)
    elif file_path.lower().endswith('.md') or file_path.lower().endswith('.mdx'):
        return _parse_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
