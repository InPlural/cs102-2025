alpha_size = 26


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_len = len(keyword)
    for key_idx, char in enumerate(plaintext):
        if "A" <= char <= "Z":
            a_idx = ord("A")
        elif "a" <= char <= "z":
            a_idx = ord("a")
        else:
            ciphertext += char
            continue

        position = ord(char) - a_idx
        key_char = keyword[key_idx % key_len]
        shift = ord(key_char) - a_idx
        new_position = position + shift
        new_char = chr(a_idx + new_position % alpha_size)
        ciphertext += new_char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_len = len(keyword)
    for key_idx, char in enumerate(plaintext):
        if "A" <= char <= "Z":
            a_idx = ord("A")
        elif "a" <= char <= "z":
            a_idx = ord("a")
        else:
            ciphertext += char
            continue

        position = ord(char) - a_idx
        key_let = keyword[key_idx % key_len]
        shift = ord(key_let) - a_idx
        new_position = position - shift
        new_char = chr(a_idx + new_position % alpha_size)
        plaintext += new_char
    return plaintext
