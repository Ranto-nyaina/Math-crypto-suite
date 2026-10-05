"""Graphes non orientés — degrés et somme."""

def parse_graphe(texte: str):
    graphe = {}
    for ligne in texte.strip().splitlines():
        if ":" not in ligne:
            continue
        sommet, voisins = ligne.split(":", 1)
        sommet = sommet.strip()
        voisins = [v.strip() for v in voisins.split(",") if v.strip()]
        graphe[sommet] = voisins
    return graphe

def degres(graphe):
    return {s: len(v) for s, v in graphe.items()}

def somme_degres(graphe):
    return sum(len(v) for v in graphe.values())