"""Opérations sur les ensembles finis."""

def parse_ensemble(texte: str):
    elements = set()
    for token in texte.replace(";", ",").split(","):
        token = token.strip()
        if token:
            elements.add(int(token))
    return elements

def union(a, b):
    return a | b

def intersection(a, b):
    return a & b

def difference(a, b):
    return a - b

def fonct(x):
    return x * x - 3

def image_ensemble(ensemble):
    return {fonct(x) for x in ensemble}