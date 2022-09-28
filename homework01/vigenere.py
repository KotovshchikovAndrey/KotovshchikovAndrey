from string import ascii_lowercase, ascii_uppercase


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    key_dict = {symbol: i for i, symbol in enumerate(ascii_uppercase)}

    for i, symbol in enumerate(plaintext):
        alphabet = ascii_uppercase if symbol.isupper() else ascii_lowercase

        symbol_index_in_ascii = alphabet.find(symbol)
        if symbol_index_in_ascii == -1:
            ciphertext += symbol
            continue

        key_for_symbol = keyword[i] if i < len(keyword) else keyword[i % len(keyword)]
        shift = key_dict[key_for_symbol.upper()]
        try:
            ciphertext += alphabet[symbol_index_in_ascii + shift]
        except IndexError:
            ciphertext += alphabet[(symbol_index_in_ascii + shift) % len(alphabet)]

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    key_dict = {symbol: i for i, symbol in enumerate(ascii_uppercase)}

    for i, symbol in enumerate(ciphertext):
        alphabet = ascii_uppercase if symbol.isupper() else ascii_lowercase

        symbol_index_in_ascii = alphabet.find(symbol)
        if symbol_index_in_ascii == -1:
            plaintext += symbol
            continue

        key_for_symbol = keyword[i] if i < len(keyword) else keyword[i % len(keyword)]
        shift = key_dict[key_for_symbol.upper()]
        plaintext += alphabet[symbol_index_in_ascii - shift]

    return plaintext
