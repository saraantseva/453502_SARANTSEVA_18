import re
import zipfile
import os

DATA_DIR = os.path.join(os.getcwd(), "task2\data")
INPUT_FILE = os.path.join(DATA_DIR, "input.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.txt")
ZIP_FILE = os.path.join(DATA_DIR, "result.zip")


class TextAnalyzer:
    """Text analyzer using regular expressions"""

    def __init__(self):
        self.__text = ""

    def read_file(self, filename: str):
        """Read text from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.__text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")

    def count_sentences(self) -> int:
        """Total number of sentences"""
        sentences = re.split(r'[.!?]+', self.__text)
        return len([s for s in sentences if s.strip()])

    def count_declarative(self) -> int:
        """Declarative sentences (ending with dot)"""
        return len(re.findall(r'[^.!?]*\.', self.__text))

    def count_interrogative(self) -> int:
        """Interrogative sentences (ending with ?)"""
        return len(re.findall(r'[^.!?]*\?', self.__text))

    def count_exclamatory(self) -> int:
        """Exclamatory sentences (ending with !)"""
        return len(re.findall(r'[^.!?]*!', self.__text))

    def avg_sentence_length(self) -> float:
        """Average sentence length in characters (words only)"""
        sentences = re.split(r'[.!?]+', self.__text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        total = 0
        for s in sentences:
            clean = re.sub(r'[^A-Za-zА-Яа-я\s]', '', s)
            total += len(clean.replace(' ', ''))
        return total / len(sentences)

    def avg_word_length(self) -> float:
        """Average word length in characters"""
        words = re.findall(r'[A-Za-zА-Яа-я]+', self.__text)
        if not words:
            return 0.0
        return sum(len(w) for w in words) / len(words)

    def count_smileys(self) -> int:
        """Smileys pattern: [:;][-]*[()\[\]]+"""
        return len(re.findall(r'[:;]-*[()\[\]]+', self.__text))

    def find_arithmetic(self) -> list:
        """Arithmetic expressions: number operator number"""
        pattern = r'-?\d+(?:\.\d+)?\s*[+\-*/]\s*-?\d+(?:\.\d+)?'
        return re.findall(pattern, self.__text)

    def odd_length_words(self) -> list:
        """Words with odd number of letters"""
        words = re.findall(r'[A-Za-zА-Яа-я]+', self.__text)
        return [w for w in words if len(w) % 2 == 1]

    def shortest_i_word(self) -> str:
        """Shortest word starting with 'i' (case insensitive)"""
        words = re.findall(r'[A-Za-zА-Яа-я]+', self.__text)
        i_words = [w for w in words if w.lower().startswith('i')]
        return min(i_words, key=len) if i_words else ""

    def duplicate_words(self) -> list:
        """Duplicate words (case insensitive)"""
        words = re.findall(r'[A-Za-zА-Яа-я]+', self.__text)
        lower_words = [w.lower() for w in words]
        seen = set()
        duplicates = set()
        for w in lower_words:
            if w in seen:
                duplicates.add(w)
            else:
                seen.add(w)
        return sorted(duplicates)


def task_2():
    """Main function for task 2"""
    analyzer = TextAnalyzer()

    # Create data directory if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    # Get filename from user
    while True:
        filename = input("Enter filename (Enter for default data/input.txt): ").strip()
        if not filename:
            filename = INPUT_FILE
        try:
            analyzer.read_file(filename)
            break
        except FileNotFoundError as e:
            print(e)

    # Collect results
    results = {
        "Total sentences": analyzer.count_sentences(),
        "Declarative sentences": analyzer.count_declarative(),
        "Interrogative sentences": analyzer.count_interrogative(),
        "Exclamatory sentences": analyzer.count_exclamatory(),
        "Average sentence length (chars)": f"{analyzer.avg_sentence_length():.2f}",
        "Average word length (chars)": f"{analyzer.avg_word_length():.2f}",
        "Number of smileys": analyzer.count_smileys(),
        "Arithmetic expressions": analyzer.find_arithmetic(),
        "Words with odd length": analyzer.odd_length_words(),
        "Shortest word starting with 'i'": analyzer.shortest_i_word(),
        "Duplicate words": analyzer.duplicate_words()
    }

    # Print to console
    print("\n")
    print("TEXT ANALYSIS RESULTS")
    for key, value in results.items():
        print(f"{key}: {value}")

    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for key, value in results.items():
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
        print(f"Compression ratio: {info.compress_size / info.file_size * 100:.1f}%")


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
    """Interactive menu with retry functionality"""
    work = True
    while work:
        task_2()
        work = get_yes_no("\nDo you want to analyze another text?")
    print("Goodbye!")


if __name__ == "__main__":
    task2()