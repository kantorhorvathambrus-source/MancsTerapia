#!/usr/bin/env python3
"""Legenerálja a data/fajtak.json fájlt az ALAPADATOK listából és a SZOVEGEK
szótárban gyűjtött fajtaleírásokból.

Használat:
    python3 scripts/fajtak_epit.py
"""

import json
import os

# --- Alapadatok: (név, méret, csoport) -------------------------------------
# méret: "kicsi" | "kozepes" | "nagy"
ALAPADATOK = [
    ("Magyar vizsla", "kozepes", "Vadászkutya"),
    ("Drótszőrű magyar vizsla", "kozepes", "Vadászkutya"),
    ("Puli", "kicsi", "Pásztorkutya"),
    ("Pumi", "kicsi", "Pásztorkutya"),
    ("Mudi", "kicsi", "Pásztorkutya"),
    ("Komondor", "nagy", "Pásztorkutya"),
    ("Kuvasz", "nagy", "Pásztorkutya"),
    ("Erdélyi kopó", "kozepes", "Vadászkutya"),
    ("Labrador retriever", "nagy", "Retriever"),
    ("Golden retriever", "nagy", "Retriever"),
    ("Border collie", "kozepes", "Pásztorkutya"),
    ("Ausztrál juhászkutya", "kozepes", "Pásztorkutya"),
    ("Német juhászkutya", "nagy", "Pásztorkutya"),
    ("Belga juhászkutya (malinois)", "kozepes", "Pásztorkutya"),
    ("Fehér svájci pásztorkutya", "nagy", "Pásztorkutya"),
    ("Cane corso", "nagy", "Testőrkutya"),
    ("Rottweiler", "nagy", "Testőrkutya"),
    ("Dobermann", "nagy", "Testőrkutya"),
    ("Boxer", "nagy", "Munkakutya"),
    ("Bernáthegyi", "nagy", "Munkakutya"),
    ("Newfoundlandi kutya", "nagy", "Vízikutya"),
    ("Nagy svájci hegyikutya", "nagy", "Munkakutya"),
    ("Leonbergi", "nagy", "Munkakutya"),
    ("Óriás schnauzer", "nagy", "Munkakutya"),
    ("Középső schnauzer", "kozepes", "Munkakutya"),
    ("Törpeschnauzer", "kicsi", "Terrier"),
    ("Airedale terrier", "kozepes", "Terrier"),
    ("Ír szetter", "nagy", "Vadászkutya"),
    ("Angol szetter", "nagy", "Vadászkutya"),
    ("Gordon szetter", "nagy", "Vadászkutya"),
    ("Pointer", "nagy", "Vadászkutya"),
    ("Német drótszőrű vizsla", "kozepes", "Vadászkutya"),
    ("Weimari vizsla", "nagy", "Vadászkutya"),
    ("Breton spániel", "kozepes", "Vadászkutya"),
    ("Cocker spániel", "kicsi", "Spániel"),
    ("Springer spániel", "kozepes", "Spániel"),
    ("Cavalier king charles spániel", "kicsi", "Társasági kutya"),
    ("King charles spániel", "kicsi", "Társasági kutya"),
    ("Beagle", "kozepes", "Vadászkutya"),
    ("Basset hound", "kozepes", "Vadászkutya"),
    ("Foxhound", "nagy", "Vadászkutya"),
    ("Dalmata", "nagy", "Társasági kutya"),
    ("Jack russell terrier", "kicsi", "Terrier"),
    ("Parson russell terrier", "kicsi", "Terrier"),
    ("Drótszőrű foxterrier", "kicsi", "Terrier"),
    ("Simaszőrű foxterrier", "kicsi", "Terrier"),
    ("Yorkshire terrier", "kicsi", "Társasági kutya"),
    ("West highland white terrier", "kicsi", "Terrier"),
    ("Skót terrier", "kicsi", "Terrier"),
    ("Cairn terrier", "kicsi", "Terrier"),
    ("Boston terrier", "kicsi", "Társasági kutya"),
    ("Bullterrier", "kozepes", "Terrier"),
    ("Staffordshire bullterrier", "kozepes", "Terrier"),
    ("Amerikai staffordshire terrier", "kozepes", "Terrier"),
    ("Ír terrier", "kozepes", "Terrier"),
    ("Border terrier", "kicsi", "Terrier"),
    ("Bichon frisé", "kicsi", "Társasági kutya"),
    ("Máltai selyemkutya", "kicsi", "Társasági kutya"),
    ("Havanese", "kicsi", "Társasági kutya"),
    ("Törpepudli", "kicsi", "Társasági kutya"),
    ("Nagypudli", "nagy", "Társasági kutya"),
    ("Lagotto romagnolo", "kozepes", "Vízikutya"),
    ("Shih tzu", "kicsi", "Társasági kutya"),
    ("Lhasa apso", "kicsi", "Társasági kutya"),
    ("Tibeti spániel", "kicsi", "Társasági kutya"),
    ("Pekingi palotakutya", "kicsi", "Társasági kutya"),
    ("Mopsz", "kicsi", "Társasági kutya"),
    ("Francia bulldog", "kicsi", "Társasági kutya"),
    ("Angol bulldog", "kozepes", "Társasági kutya"),
    ("Basenji", "kicsi", "Vadászkutya"),
    ("Sharpei", "kozepes", "Testőrkutya"),
    ("Chow chow", "kozepes", "Társasági kutya"),
    ("Akita inu", "nagy", "Testőrkutya"),
    ("Shiba inu", "kicsi", "Vadászkutya"),
    ("Sziberiai husky", "kozepes", "Szánhúzó kutya"),
    ("Alaszkai malamut", "nagy", "Szánhúzó kutya"),
    ("Szamojéd", "kozepes", "Szánhúzó kutya"),
    ("Grönlandi kutya", "nagy", "Szánhúzó kutya"),
    ("Ír farkaskutya", "nagy", "Agár"),
    ("Skót szarvasagár", "nagy", "Agár"),
    ("Angol agár", "nagy", "Agár"),
    ("Afgán agár", "nagy", "Agár"),
    ("Whippet", "kozepes", "Agár"),
    ("Spanyol agár", "nagy", "Agár"),
    ("Olasz agár", "kicsi", "Agár"),
    ("Magyar agár", "nagy", "Agár"),
    ("Rodéziai ridgeback", "nagy", "Vadászkutya"),
    ("Bloodhound", "nagy", "Vadászkutya"),
    ("Basset artésien normand", "kozepes", "Vadászkutya"),
    ("Beagle harrier", "kozepes", "Vadászkutya"),
    ("Törpetacskó", "kicsi", "Vadászkutya"),
    ("Normál tacskó", "kicsi", "Vadászkutya"),
    ("Chihuahua", "kicsi", "Társasági kutya"),
    ("Pomerániai törpespicc", "kicsi", "Társasági kutya"),
    ("Keeshond", "kozepes", "Társasági kutya"),
    ("Walesi corgi pembroke", "kicsi", "Pásztorkutya"),
    ("Walesi corgi cardigan", "kicsi", "Pásztorkutya"),
    ("Ausztrál cattle dog", "kozepes", "Pásztorkutya"),
    ("Ausztrál kelpie", "kozepes", "Pásztorkutya"),
    ("Angol ószövegű juhászkutya (bobtail)", "nagy", "Pásztorkutya"),
    ("Shetlandi juhászkutya", "kicsi", "Pásztorkutya"),
    ("Skót juhászkutya (collie)", "nagy", "Pásztorkutya"),
    ("Beauceron", "nagy", "Pásztorkutya"),
    ("Briard", "nagy", "Pásztorkutya"),
    ("Entlebuchi pásztorkutya", "kozepes", "Munkakutya"),
    ("Appenzelli pásztorkutya", "kozepes", "Munkakutya"),
    ("Portugál vízikutya", "kozepes", "Vízikutya"),
    ("Spanyol vízikutya", "kozepes", "Vízikutya"),
    ("Göndörszőrű retriever", "nagy", "Retriever"),
    ("Egyenesszőrű retriever", "nagy", "Retriever"),
    ("Nova Scotia Duck Tolling Retriever", "kozepes", "Retriever"),
    ("Toy foxterrier", "kicsi", "Terrier"),
    ("Manchester terrier", "kicsi", "Terrier"),
    ("Bedlington terrier", "kicsi", "Terrier"),
    ("Skye terrier", "kicsi", "Terrier"),
    ("Norfolk terrier", "kicsi", "Terrier"),
    ("Norwich terrier", "kicsi", "Terrier"),
    ("Ausztrál silky terrier", "kicsi", "Társasági kutya"),
    ("Kínai meztelen kutya", "kicsi", "Társasági kutya"),
    ("Amerikai akita", "nagy", "Testőrkutya"),
]

# --- Fajtaleírások ------------------------------------------------------
# Minden fajtához pontosan 10 erősség és 10 hátrány/figyelmeztetés tartozik.
# A szótár feltöltése körönként, 10 fajtánként történik.
# Import a scripts/fajtak_adatok/ mappából (fajták betűrendi csoportokban).
from fajtak_adatok import SZOVEGEK  # noqa: E402


def epit():
    gyoker = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_kimenet = os.path.join(gyoker, "data", "fajtak.json")
    js_kimenet = os.path.join(gyoker, "data", "fajtak.js")

    fajtak = []
    for nev, meret, csoport in ALAPADATOK:
        szoveg = SZOVEGEK.get(nev, {})
        fajtak.append({
            "nev": nev,
            "meret": meret,
            "csoport": csoport,
            "erossegek": szoveg.get("erossegek", []),
            "hatranyok": szoveg.get("hatranyok", []),
        })

    with open(json_kimenet, "w", encoding="utf-8") as f:
        json.dump(fajtak, f, ensure_ascii=False, indent=2)

    # A fajtak.js ugyanazt az adatot adja, script tagként betölthető formában,
    # hogy a fajtak.html file:// (letöltött mappából, szerver nélkül) megnyitva
    # is működjön — fetch() helyi fájlokon böngészőben CORS miatt nem működik.
    with open(js_kimenet, "w", encoding="utf-8") as f:
        f.write("// Generált fájl — NE szerkeszd kézzel, a scripts/fajtak_epit.py generálja.\n")
        f.write("window.FAJTAK_ADATOK = ")
        json.dump(fajtak, f, ensure_ascii=False, indent=2)
        f.write(";\n")

    print(f"Kiírva: {json_kimenet} és {js_kimenet} ({len(fajtak)} fajta)")


if __name__ == "__main__":
    epit()
