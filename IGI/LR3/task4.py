def find_ind(word):
    """
    Check if word has equal number of vowels and consonants.
    
    Args:
        word: input word
    
    Returns:
        bool: True if vowels count equals consonants count
    """
    vowels = "aeiouy"
    consonants = "bcdfghjklmnpqrstvwxz"
    v = 0
    c = 0
    for char in word.lower():
        if char in vowels:
            v += 1
        elif char in consonants:
            c += 1
    return v == c


def task4():
    """
    Main function for Task 4.
    Analyzes a fixed text:
    a) Counts words with 4 letters
    b) Finds words with equal vowels and consonants
    c) Sorts words by length descending
    """
    text = ("So she was considering in her own mind, "
            "as well as she could, for the hot day made "
            "her feel very sleepy and stupid, whether "
            "the pleasure of making a daisy-chain would "
            "be worth the trouble of getting up and "
            "picking the daisies, when suddenly a White "
            "Rabbit with pink eyes ran close by her.")

    for p in ",.!?;:-":
        text = text.replace(p, ' ')
    words = text.split()
    
    # a) Words with length 4
    words_4 = [word for word in words if len(word) == 4]
    print(f"a) Words with 4 letters: {len(words_4)}")
    print(words_4)
    
    # b) Words with equal vowels and consonants
    equal_words = [(i + 1, word) for i, word in enumerate(words) if find_ind(word)]
    print(f"\nb) Words with equal vowels and consonants:")
    for idx, word in equal_words:
        print(f"   {idx}: {word}")
    
    # c) Words sorted by length descending
    sorted_words = sorted(words, key=len, reverse=True)
    print(f"\nc) Words sorted by length descending:")
    print(sorted_words)

