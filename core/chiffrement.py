"""Algorithmes de chiffrement (ASCII + César)."""

def chiffrement_ascii(message: str):
    return [ord(c) for c in message]

def dechiffrement_ascii(codes) -> str:
    return "".join(chr(c) for c in codes)

def chiffrement_cesar(message: str, decalage: int) -> str:
    resultat = ""
    for c in message:
        if c.isalpha():
            if c.islower():
                resultat += chr((ord(c) - ord('a') + decalage) % 26 + ord('a'))
            else:
                resultat += chr((ord(c) - ord('A') + decalage) % 26 + ord('A'))
        else:
            resultat += c
    return resultat

def dechiffrement_cesar(message: str, decalage: int) -> str:
    return chiffrement_cesar(message, -decalage)