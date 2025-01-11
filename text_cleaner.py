import os
import re
from pathlib import Path
from typing import Dict

def setup_directories() -> tuple[Path, Path]:
    """Create input and output directories if they don't exist."""
    input_dir = Path("raw_texts")
    output_dir = Path("cleaned_texts")
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    return input_dir, output_dir

def split_into_pages(text: str) -> list[tuple[str, str]]:
    """Split text into pages and return list of (page_number, content) tuples."""
    pages = []
    page_matches = list(re.finditer(r'---\s*Page\s*(\d+)\s*---', text))
    
    for i, match in enumerate(page_matches):
        page_num = match.group(1)
        start = match.end()
        end = page_matches[i + 1].start() if i + 1 < len(page_matches) else len(text)
        page_content = text[start:end].strip()
        pages.append((page_num, page_content))
    
    return pages

def remove_headers_footers(text: str) -> str:
    """Remove common header and footer patterns from the text."""
    header_patterns = [
        r'පාර්ලිමේන්තු විවාද\s*\n.*\n',
        r'.*ශ්‍රී ලංකා ප්‍රජාතාන්ත්‍රික සමාජවාදී ජනරජයේ පාර්ලිමේන්තුව.*\n'
    ]
    for pattern in header_patterns:
        text = re.sub(pattern, '', text)
    return text

def remove_ocr_artifacts(text: str) -> str:
    """Remove common OCR errors while preserving valid characters."""
    # Keep Sinhala, Tamil, English, and common punctuation
    text = re.sub(r'[^\u0D80-\u0DFF\u0B80-\u0BFFA-Za-z\s.,!?()"\'-]', '', text)
    return text

def normalize_spacing(text: str) -> str:
    """Normalize whitespace and paragraph breaks."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()

def clean_text(text: str) -> str:
    """Apply all cleaning operations to the text."""
    # Remove headers and footers
    text = remove_headers_footers(text)
    
    # Remove page numbers
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Remove OCR artifacts
    text = remove_ocr_artifacts(text)
    
    # Normalize whitespace
    text = normalize_spacing(text)
    
    return text

def verify_cleaning(text: str) -> Dict[str, int]:
    """Check for potential remaining issues in the cleaned text."""
    return {
        'isolated_numbers': len(re.findall(r'\b\d+\b', text)),
        'excessive_whitespace': len(re.findall(r'\s{3,}', text)),
        'empty_lines': len(re.findall(r'\n\s*\n\s*\n', text))
    }

def process_files(input_dir: Path, output_dir: Path) -> None:
    """Process all text files in the input directory."""
    for file_path in input_dir.glob("*.txt"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Create document-specific output directory
            doc_output_dir = output_dir / file_path.stem / "pages"
            doc_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Split and process each page
            pages = split_into_pages(text)
            for page_num, page_content in pages:
                cleaned_page = clean_text(page_content)
                issues = verify_cleaning(cleaned_page)
                
                # Save individual page
                page_path = doc_output_dir / f"page{page_num}.txt"
                with open(page_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_page)
                
                if any(v > 0 for v in issues.values()):
                    print(f"Issues in {file_path.name} page {page_num}: {issues}")
                    
            print(f"Successfully processed: {file_path.name}")
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
