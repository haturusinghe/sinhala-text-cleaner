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
            
            cleaned_text = clean_text(text)
            issues = verify_cleaning(cleaned_text)
            
            output_path = output_dir / file_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            print(f"Successfully processed: {file_path.name}")
            if any(v > 0 for v in issues.values()):
                print(f"Potential issues found: {issues}")
                
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")