import typing as tp
from string import ascii_lowercase, ascii_uppercase


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for symbol in plaintext:
        alphabet = ascii_uppercase if symbol.isupper() else ascii_lowercase 
        symbol_index_in_ascii = alphabet.find(symbol) 
        if symbol_index_in_ascii == -1:
            ciphertext += symbol
            continue
        
        try:
            ciphertext += alphabet[symbol_index_in_ascii + shift]
        except IndexError:
            ciphertext += alphabet[( symbol_index_in_ascii + shift ) % len(alphabet)]

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for symbol in ciphertext:
        alphabet = ascii_uppercase if symbol.isupper() else ascii_lowercase 
        symbol_index_in_ascii = alphabet.find(symbol) 
        if symbol_index_in_ascii == -1:
            plaintext += symbol
            continue
        
        plaintext += alphabet[symbol_index_in_ascii - shift]

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    while True:
        plaintext = decrypt_caesar(ciphertext=ciphertext, shift=best_shift)
        if plaintext not in dictionary:
            best_shift += 1
            continue

        return best_shift
