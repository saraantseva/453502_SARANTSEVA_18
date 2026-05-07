'''
Description: Main module for text analysis with interactive menu
'''
import zipfile
import os
from task2.models import TextAnalyzer

DATA_DIR = os.path.join(os.getcwd(), r"task2\data")
INPUT_FILE = os.path.join(DATA_DIR, "input.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.txt")
ZIP_FILE = os.path.join(DATA_DIR, "result.zip")


def get_yes_no(prompt: str) -> bool:
    """Get yes/no answer from user"""
    while True:
        answer = input(prompt + " (y/n): ").lower()
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("Please enter y or n")


def task2():
    """Main function for task 2 - Variant 18"""
    analyzer = TextAnalyzer()

    os.makedirs(DATA_DIR, exist_ok=True)

    # Get filename from user
    while True:
        filename = input("Enter filename (Enter for default): ").strip()
        if not filename:
            filename = INPUT_FILE
        try:
            analyzer.read_file(filename)
            break
        except FileNotFoundError as e:
            print(e)

    # Collect results
    results = {
        "=" * 50: "",
        "GENERAL ANALYSIS": "",
        "Total sentences": analyzer.count_sentences(),
        "Declarative sentences": analyzer.count_declarative(),
        "Interrogative sentences": analyzer.count_interrogative(),
        "Exclamatory sentences": analyzer.count_exclamatory(),
        "Average sentence length (chars)": f"{analyzer.avg_sentence_length():.2f}",
        "Average word length (chars)": f"{analyzer.avg_word_length():.2f}",
        "Number of smileys": analyzer.count_smileys(),
        "=" * 50: "",
        "VARIANT 18 RESULTS": "",
        "Arithmetic expressions": analyzer.find_arithmetic(),
        "Words with digits AND vowels": analyzer.find_words_with_digits_and_vowels(),
        "Words with odd length": analyzer.odd_length_words(),
        "Shortest word starting with 'i'": analyzer.shortest_i_word(),
        "Duplicate words": analyzer.duplicate_words(),
    }

    # Print to console
    print("\n")
    for key, value in results.items():
        if key == "":
            print()
        elif isinstance(value, list):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")

    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for key, value in results.items():
            if key == "":
                f.write("\n")
            elif isinstance(value, list):
                f.write(f"{key}: {value}\n")
            else:
                f.write(f"{key}: {value}\n")
    print(f"\nResults saved to {OUTPUT_FILE}")

    # Create zip archive
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(OUTPUT_FILE, arcname="output.txt")

    # Show archive info
    with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
        info = zf.getinfo("output.txt")
        print(f"\nArchive created: {ZIP_FILE}")
        print(f"File in archive: {info.filename}")
        print(f"Original size: {info.file_size} bytes")
        print(f"Compressed size: {info.compress_size} bytes")
   

def main():
    """Main function with interactive menu"""
    work = True
    while work:
        task2()
        work = get_yes_no("\nDo you want to analyze another text?")
    print("Goodbye!")


if __name__ == "__main__":
    main()
