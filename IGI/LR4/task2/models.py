'''
Description: TextAnalyzer class for text analysis using regular expressions

'''
import re
"""
Module: models.py
Lab: Laboratory Work No. 4, Task 2 (Variant 18)
Developer: Sarantseva Darya
Date: 2026-05-07
Description: TextAnalyzer class for text analysis using regular expressions
"""

import re


class TextAnalyzer:
    """Text analyzer using regular expressions - Variant 18"""
    
    VOWELS = 'aeiouyAEIOUYаеёиоуыэюяАЕЁИОУЫЭЮЯ'

    def __init__(self):
        self.__text = ""

    def read_file(self, filename: str):
        """Read text from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.__text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")

    def get_text(self) -> str:
        """Return current text"""
        return self.__text

    # general
    
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
        r"""Smileys pattern: [:;][-]*[()\[\]]+"""
        return len(re.findall(r'[:;]-*[()\[\]]+', self.__text))

    #  18
    
    def find_arithmetic(self) -> list:
        """Arithmetic expressions: number operator number"""
        pattern = r'-?\d+(?:\.\d+)?\s*[+\-*/]\s*-?\d+(?:\.\d+)?'
        return re.findall(pattern, self.__text)

    def find_words_with_digits_and_vowels(self) -> list:
        """Words containing both digits and vowels"""
        words = re.findall(r'[A-Za-zА-Яа-я0-9]+', self.__text)
        result = []
        for w in words:
            has_digit = any(c.isdigit() for c in w)
            has_vowel = any(c in self.VOWELS for c in w)
            if has_digit and has_vowel:
                result.append(w)
        return result

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