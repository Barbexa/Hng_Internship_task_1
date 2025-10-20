import hashlib
import re
from collections import Counter

def analyze_string(s: str) -> dict:
    sha256_hash = hashlib.sha256(s.encode('utf-8')).hexdigest()

    length= len(s)

    word_count = len(s.split())
    
    clean_s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()



    is_palindrome = (clean_s == clean_s[::-1])

    char_counts = Counter(clean_s)

    unique_chars = len(char_counts)

    return{
        'id': sha256_hash,
        'value': s,
        'length': length,
        'is_palindrome': is_palindrome,
        'unique_characters': unique_chars,
        'word_count': word_count,
        'sha256_hash': sha256_hash, 
        'character_frequency_map': dict(char_counts)

    }
