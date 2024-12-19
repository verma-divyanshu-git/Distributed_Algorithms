#!/usr/bin/env python3
import sys

current_word = None
current_count = 0
word = None

# Input comes from standard input (stdin)
for line in sys.stdin:
    # Remove leading and trailing whitespace
    line = line.strip()
    # Parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    
    # Convert count from string to int
    try:
        count = int(count)
    except ValueError:
        continue
    
    # If the word is the same as the previous word, increment its count
    if current_word == word:
        current_count += count
    else:
        # If it's a new word, output the previous word and its count
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# Output the last word if needed
if current_word == word:
    print(f"{current_word}\t{current_count}")

