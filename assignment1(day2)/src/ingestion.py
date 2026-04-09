import pdfplumber
import re
from typing import List, Dict
from collections import Counter

class DocumentProcessor:
    def __init__(self, footer_threshold: float = 0.8):
        self.footer_threshold = footer_threshold

    def extract_text(self, pdf_path: str) -> List[Dict]:
        """Extracts text and metadata from each page of a PDF."""
        pages_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                # Optional: Handle tables explicitly if needed
                # tables = page.extract_tables()
                pages_content.append({
                    "page_num": i + 1,
                    "text": text,
                    "raw_lines": text.split("\n")
                })
        return pages_content

    def clean_boilerplate(self, pages_content: List[Dict]) -> List[Dict]:
        """Identifies and removes headers/footers based on frequency across pages."""
        if not pages_content:
            return pages_content

        # Count occurrences of specific lines at the beginning and end of pages
        header_candidates = Counter()
        footer_candidates = Counter()

        for page in pages_content:
            lines = [l.strip() for l in page["raw_lines"] if l.strip()]
            if lines:
                header_candidates[lines[0]] += 1
                footer_candidates[lines[-1]] += 1

        num_pages = len(pages_content)
        headers_to_remove = {line for line, count in header_candidates.items() 
                             if count / num_pages > self.footer_threshold}
        footers_to_remove = {line for line, count in footer_candidates.items() 
                             if count / num_pages > self.footer_threshold}

        for page in pages_content:
            lines = page["raw_lines"]
            cleaned_lines = [l for l in lines if l.strip() not in headers_to_remove 
                             and l.strip() not in footers_to_remove]
            page["cleaned_text"] = "\n".join(cleaned_lines).strip()
            
        return pages_content

    def process_document(self, pdf_path: str) -> str:
        """Full pipeline: Load, clean, and merge into a single clean string."""
        raw_pages = self.extract_text(pdf_path)
        cleaned_pages = self.clean_boilerplate(raw_pages)
        full_text = "\n\n--- PAGE BREAK ---\n\n".join([p["cleaned_text"] for p in cleaned_pages])
        return full_text

if __name__ == "__main__":
    # Smoke test logic
    import sys
    if len(sys.argv) > 1:
        processor = DocumentProcessor()
        text = processor.process_document(sys.argv[1])
        print(f"Extracted {len(text)} characters.")
