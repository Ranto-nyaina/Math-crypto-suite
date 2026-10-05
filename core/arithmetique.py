"""Nombres premiers, PGCD et PPCM."""

def est_premier(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def trier_premiers(liste):
    return sorted([n for n in liste if est_premier(n)])

def pgcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def ppcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // pgcd(a, b)

def pgcd_plusieurs(nombres):
    r = nombres[0]
    for n in nombres[1:]:
        r = pgcd(r, n)
    return r

def ppcm_plusieurs(nombres):
    r = nombres[0]
    for n in nombres[1:]:
        r = ppcm(r, n)
    return r