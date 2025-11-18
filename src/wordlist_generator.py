# src/wordlist_generator.py

from typing import List, Set

# Leetspeak substitution map (common simple substitutions)
LEET_MAP = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['5', '$'],
    't': ['7', '+'],
    'l': ['1', '|'],
    # Can be expanded for more complex substitutions
}

def generate_permutations(base_words: List[str]) -> Set[str]:
    """
    Generates variations (capitalization, reversal, basic leetspeak) 
    from a list of base words.
    """
    wordlist = set()
    
    for word in base_words:
        if not word:
            continue
        
        # 1. Base forms (original, lower, upper, title)
        wordlist.add(word)
        wordlist.add(word.lower())
        wordlist.add(word.upper())
        wordlist.add(word.title())
        
        # 2. Reversals
        wordlist.add(word[::-1])
        wordlist.add(word.lower()[::-1])

    # 3. Apply simple Leetspeak to all current words in the set
    current_words = list(wordlist)
    for word in current_words:
        # A simple, single-level substitution
        leet_word = word
        for char, subs in LEET_MAP.items():
            # Apply only the first substitution for simplicity here
            leet_word = leet_word.replace(char, subs[0])
            leet_word = leet_word.replace(char.upper(), subs[0])
        
        if leet_word != word:
            wordlist.add(leet_word)
            # Add capitalized/reversed versions of the leet word too
            wordlist.add(leet_word.title())
            wordlist.add(leet_word[::-1])

    return wordlist

def append_common_years(wordlist: Set[str]) -> Set[str]:
    """
    Appends common four-digit and two-digit year combinations to every 
    word in the set.
    """
    new_wordlist = set(wordlist)
    
    # Common decades and years (can be expanded)
    years = [str(y) for y in range(1980, 2026)]
    years += [str(y)[2:] for y in range(1980, 2026)] # e.g., '95', '04'

    for word in wordlist:
        if len(word) > 2: # Avoid appending to very short strings
            for year in years:
                new_wordlist.add(word + year)
                new_wordlist.add(year + word) # Prepended versions

    return new_wordlist


def export_wordlist(wordlist: Set[str], filename: str) -> int:
    """
    Exports the final set of generated passwords to a .txt file.

    Returns:
        The number of unique passwords written to the file.
    """
    try:
        count = 0
        with open(filename, 'w', encoding='utf-8') as f:
            for word in sorted(list(wordlist)):
                f.write(word + '\n')
                count += 1
        return count
    except IOError as e:
        print(f"Error writing file {filename}: {e}")
        return 0


def generate_and_export_wordlist(inputs: List[str], output_filename: str):
    """
    Orchestrates the wordlist generation and export process.
    """
    # Filter out empty or irrelevant inputs
    base_inputs = [i.strip() for i in inputs if i.strip()]
    
    # 1. Generate core permutations (casing, reversals, basic leetspeak)
    print("Generating core permutations...")
    initial_words = generate_permutations(base_inputs)
    
    # 2. Apply complex patterns (Year Appending)
    print("Applying common year patterns...")
    final_wordlist = append_common_years(initial_words)

    # 3. Export
    print(f"Exporting {len(final_wordlist)} unique words to {output_filename}...")
    count = export_wordlist(final_wordlist, output_filename)
    
    print(f"Wordlist successfully created with {count} entries.")


if __name__ == "__main__":
    # --- Example Usage ---
    
    user_details = [
        "Jsmith", 
        "Sparky", 
        "1995", 
        "Summer" # A season or favorite word
    ]
    output_file = "custom_attack_list.txt"
    
    generate_and_export_wordlist(user_details, output_file)
