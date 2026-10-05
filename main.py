"""
Math & Crypto Suite
Application mobile éducative — KivyMD
"""

import os
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from core import chiffrement as crypto
from core import arithmetique as arith
from core import rsa as rsa_core
from core import ensembles as ens_core
from core import graphes as graph_core


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")


class ModuleCard(MDCard):
    title_text = StringProperty("")
    subtitle_text = StringProperty("")
    icon_name = StringProperty("apps")
    target_screen = StringProperty("")


class HomeScreen(MDScreen):
    pass


class ChiffrementScreen(MDScreen):
    def _get_message(self):
        msg = self.ids.message_field.text.strip()
        if not msg:
            self._err("Veuillez entrer un message.")
            return None
        return msg

    def _get_decalage(self):
        txt = self.ids.decalage_field.text.strip()
        try:
            return int(txt)
        except ValueError:
            self._err("Le décalage doit être un nombre entier.")
            return None

    def _err(self, msg):
        MDApp.get_running_app().show_dialog("Erreur", msg)

    def chiffrer(self):
        msg = self._get_message()
        if msg is None:
            return
        dec = self._get_decalage()
        if dec is None:
            return
        self.ids.cesar_label.text = crypto.chiffrement_cesar(msg, dec)

    def dechiffrer(self):
        msg = self._get_message()
        if msg is None:
            return
        dec = self._get_decalage()
        if dec is None:
            return
        self.ids.cesar_label.text = crypto.dechiffrement_cesar(msg, dec)

    def afficher_ascii(self):
        msg = self._get_message()
        if msg is None:
            return
        codes = crypto.chiffrement_ascii(msg)
        self.ids.ascii_label.text = ", ".join(str(c) for c in codes)
        self.ids.ascii_back_label.text = crypto.dechiffrement_ascii(codes)


class RSAScreen(MDScreen):
    cles = ObjectProperty(None, allownone=True)

    def _err(self, msg):
        MDApp.get_running_app().show_dialog("Erreur", msg)

    def generer(self):
        try:
            p = int(self.ids.p_field.text)
            q = int(self.ids.q_field.text)
            e = int(self.ids.e_field.text)
        except ValueError:
            self._err("p, q et e doivent être des entiers.")
            return
        if not (arith.est_premier(p) and arith.est_premier(q)):
            self._err("p et q doivent être des nombres premiers.")
            return

        self.cles = rsa_core.generer_cles(p, q, e)
        if self.cles["d"] is None:
            self._err("Impossible de trouver d. Choisissez un autre e.")
            self.cles = None
            return

        self.ids.public_label.text = f"Clé publique : (e = {self.cles['e']}, n = {self.cles['n']})"
        self.ids.private_label.text = f"Clé privée : (d = {self.cles['d']}, n = {self.cles['n']})"
        self.ids.phi_label.text = f"φ(n) = {self.cles['phi']}"

    def chiffrer(self):
        if not self.cles:
            self._err("Générez d'abord les clés.")
            return
        try:
            m = int(self.ids.msg_field.text)
        except ValueError:
            self._err("Le message doit être un entier (0 ≤ m < n).")
            return
        if not (0 <= m < self.cles["n"]):
            self._err(f"Le message doit être entre 0 et {self.cles['n'] - 1}.")
            return
        c = rsa_core.chiffrer_rsa(m, self.cles["e"], self.cles["n"])
        self.ids.chiffre_label.text = f"Message chiffré C = {c}"

    def dechiffrer(self):
        if not self.cles:
            self._err("Générez d'abord les clés.")
            return
        try:
            c = int(self.ids.chiffre_field.text)
        except ValueError:
            self._err("Entrez un entier chiffré valide.")
            return
        m = rsa_core.dechiffrer_rsa(c, self.cles["d"], self.cles["n"])
        self.ids.dechiffre_label.text = f"Message déchiffré M = {m}"


class ArithmetiqueScreen(MDScreen):
    def _err(self, msg):
        MDApp.get_running_app().show_dialog("Erreur", msg)

    def _parse(self):
        txt = self.ids.nombres_field.text
        nombres = []
        for token in txt.replace(";", ",").split(","):
            token = token.strip()
            if token:
                try:
                    nombres.append(int(token))
                except ValueError:
                    self._err(f"'{token}' n'est pas un entier.")
                    return None
        if not nombres:
            self._err("Entrez au moins un nombre.")
            return None
        return nombres

    def calculer(self):
        nombres = self._parse()
        if nombres is None:
            return

        premiers = arith.trier_premiers(nombres)
        self.ids.premiers_label.text = (
            ", ".join(map(str, premiers)) if premiers else "Aucun nombre premier."
        )

        if len(nombres) >= 2:
            g = arith.pgcd_plusieurs(nombres)
            p = arith.ppcm_plusieurs(nombres)
            self.ids.pgcd_label.text = f"PGCD = {g}"
            self.ids.ppcm_label.text = f"PPCM = {p}"
        else:
            self.ids.pgcd_label.text = "PGCD = (au moins 2 nombres)"
            self.ids.ppcm_label.text = "PPCM = (au moins 2 nombres)"


class EnsemblesScreen(MDScreen):
    def _err(self, msg):
        MDApp.get_running_app().show_dialog("Erreur", msg)

    def calculer(self):
        try:
            a = ens_core.parse_ensemble(self.ids.ens_a.text)
            b = ens_core.parse_ensemble(self.ids.ens_b.text)
        except ValueError:
            self._err("N'entrez que des entiers séparés par des virgules.")
            return

        self.ids.union_label.text = "{" + ", ".join(map(str, sorted(a | b))) + "}"
        self.ids.inter_label.text = "{" + ", ".join(map(str, sorted(a & b))) + "}"
        self.ids.diff_label.text = "{" + ", ".join(map(str, sorted(a - b))) + "}"
        self.ids.card_label.text = f"Card(A∪B) = {len(a | b)}   |   Card(A∩B) = {len(a & b)}"

        img = ens_core.image_ensemble(a)
        self.ids.image_label.text = "{" + ", ".join(map(str, sorted(img))) + "}   (f(x) = x² − 3)"


class GraphesScreen(MDScreen):
    def _err(self, msg):
        MDApp.get_running_app().show_dialog("Erreur", msg)

    def calculer(self):
        texte = self.ids.graphe_field.text
        if not texte.strip():
            self._err("Entrez au moins une ligne (ex: A: B,C).")
            return
        try:
            g = graph_core.parse_graphe(texte)
        except Exception:
            self._err("Format invalide. Utilisez : A: B,C")
            return
        if not g:
            self._err("Aucun sommet détecté.")
            return

        lignes = [f"• {s} : degré {d}" for s, d in graph_core.degres(g).items()]
        self.ids.degres_label.text = "\n".join(lignes)
        self.ids.somme_label.text = f"Somme des degrés = {graph_core.somme_degres(g)}"


class MathCryptoApp(MDApp):
    dialog = None

    def build(self):
        self.title = "Math & Crypto Suite"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"

        for fname in ("home.kv", "chiffrement.kv", "rsa.kv",
                      "arithmetique.kv", "ensembles.kv", "graphes.kv"):
            Builder.load_file(os.path.join(KV_DIR, fname))

        Window.bind(on_keyboard=self._on_keyboard)

        sm = MDScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ChiffrementScreen(name="chiffrement"))
        sm.add_widget(RSAScreen(name="rsa"))
        sm.add_widget(ArithmetiqueScreen(name="arithmetique"))
        sm.add_widget(EnsemblesScreen(name="ensembles"))
        sm.add_widget(GraphesScreen(name="graphes"))
        return sm

    def go_to(self, screen_name):
        if screen_name:
            self.root.current = screen_name

    def go_back(self):
        self.root.current = "home"

    def _on_keyboard(self, window, key, *args):
        if key == 27:
            if self.root.current != "home":
                self.root.current = "home"
                return True
        return False

    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss(),
                )
            ],
        )
        self.dialog.open()


if __name__ == "__main__":
    MathCryptoApp().run()