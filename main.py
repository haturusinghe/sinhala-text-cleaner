from text_cleaner import setup_directories, process_files

def main():
    """Main entry point for the text cleaning program."""
    print("Starting Hansard text cleaning process...")
    input_dir, output_dir = setup_directories()
    process_files(input_dir, output_dir)
    print("Processing complete.")

if __name__ == "__main__":
    main()
