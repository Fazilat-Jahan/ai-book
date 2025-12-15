import re
from typing import List, Tuple
from pypdf import PdfReader
from markdown_it import MarkdownIt

def _parse_pdf(file_path: str) -> List[Tuple[str, int]]:
    """Parses a PDF file and returns its text content page by page."""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        pages_content = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text: # Only add if text is not empty
                pages_content.append((text, i + 1)) # page numbers are 1-indexed
        return pages_content

def _parse_markdown(file_path: str) -> str:
    """Parses a Markdown file and returns its text content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        md = MarkdownIt()
        html_content = md.render(content)
        # Strip HTML tags to get plain text
        text = re.sub(r'<[^>]+>', '', html_content)
    return text

def parse_document(file_path: str) -> List[Tuple[str, int]]:
    """
    Parses a document (PDF or Markdown) and returns its text content along with page numbers.
    For Markdown, it will return a single entry with page_number = 1.
    """
    if file_path.lower().endswith('.pdf'):
        return _parse_pdf(file_path)
    elif file_path.lower().endswith('.md') or file_path.lower().endswith('.mdx'):
        # For markdown, treat the whole document as a single "page" for simplicity
        return [(_parse_markdown(file_path), 1)]
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
