# Sinhala Text Cleaner

A Python program for cleaning text files extracted from Sri Lankan Parliament Hansard PDFs.

## Features

- Removes headers, footers, and page numbers
- Cleans OCR artifacts while preserving multilingual content
- Normalizes spacing and formatting
- Supports Sinhala, Tamil, and English text

## Usage

1. Create a directory named `raw_texts` and place your input text files there
2. Run the program:
   ```bash
   python main.py
   ```
3. Find the cleaned files in the `cleaned_texts` directory

## Requirements

- Python 3.7+
- UTF-8 encoded text files

## Input File Requirements

- Text files should be UTF-8 encoded
- Files should have `.txt` extension
- Place files in the `raw_texts` directory

## Output

Cleaned files will be created in the `cleaned_texts` directory with the same names as the input files.