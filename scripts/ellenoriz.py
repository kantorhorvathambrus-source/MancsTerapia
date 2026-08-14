#!/usr/bin/env python3
"""Ellenőrzi, hogy minden ALAPADATOK-beli fajtához pontosan 10 erősség és
10 hátrány tartozik a SZOVEGEK szótárban.

Kilépési kód: 0, ha minden fajta kész; 1, ha van hiányos vagy hiányzó fajta.
"""

import sys

from fajtak_epit import ALAPADATOK
from fajtak_adatok import SZOVEGEK


def ellenoriz():
    hianyos = []

    for nev, meret, csoport in ALAPADATOK:
        szoveg = SZOVEGEK.get(nev)
        if szoveg is None:
            hianyos.append((nev, "nincs bejegyzés", 0, 0))
            continue

        erossegek = szoveg.get("erossegek", [])
        hatranyok = szoveg.get("hatranyok", [])

        if len(erossegek) != 10 or len(hatranyok) != 10:
            hianyos.append((nev, "hibás elemszám", len(erossegek), len(hatranyok)))

    osszesen = len(ALAPADATOK)
    kesz = osszesen - len(hianyos)
    print(f"Kész fajták: {kesz} / {osszesen}")

    if hianyos:
        print("\nHiányos vagy hiányzó fajták:")
        for nev, ok, e_db, h_db in hianyos:
            print(f"  - {nev}: {ok} (erősség: {e_db}, hátrány: {h_db})")
        print(f"\nKövetkező kör (max 10): {[n for n, *_ in hianyos[:10]]}")
        return 1

    print("Minden fajta kész: pontosan 10 erősség és 10 hátrány mindenhol.")
    return 0


if __name__ == "__main__":
    sys.exit(ellenoriz())
