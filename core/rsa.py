"""RSA simplifié (pédagogique)."""

def generer_cles(p: int, q: int, e: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = None
    for k in range(1, phi):
        if (k * e) % phi == 1:
            d = k
            break
    return {"n": n, "phi": phi, "e": e, "d": d}

def chiffrer_rsa(message: int, e: int, n: int) -> int:
    return pow(message, e, n)

def dechiffrer_rsa(chiffre: int, d: int, n: int) -> int:
    return pow(chiffre, d, n)