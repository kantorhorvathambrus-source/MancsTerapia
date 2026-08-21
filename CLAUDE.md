# Szívhíd terápia — projekt jegyzetek

Statikus weboldal: sima HTML + CSS + vanilla JS. Nincs build lépés, nincs
npm, nincs keretrendszer. Bármilyen statikus fájlszerverrel kiszolgálható.

## Fájlstruktúra

```
index.html          Főoldal
fajtak.html          Kutyafajták oldal (adatvezérelt, data/fajtak.js-t tölti be)
css/stilus.css        Egyetlen közös stíluslap mindkét oldalhoz
js/szkript.js          Közös viselkedés: mobil menü, kapcsolatűrlap → mailto
js/fajtak.js            Fajtaoldal logikája: keresés, méretszűrés (window.FAJTAK_ADATOK-ból)
data/fajtak.json         Generált fájl — NE szerkeszd kézzel, a scripts/ generálja
data/fajtak.js           Generált fájl — ugyanaz az adat, mint fajtak.json, de
                          `window.FAJTAK_ADATOK = [...]` script-tagként betölthető
                          formában. Azért kell fetch() helyett, mert a fetch()
                          helyi fájlokon (file://, pl. letöltött ZIP-ből megnyitva)
                          böngészőben CORS-hiba miatt nem működik — script tag igen.
assets/kep/               Képek helye (hero-kutyak.jpg ide kerül, ha lesz fotó)
assets/kep/fajtak/         Fajtakártya-fényképek, fájlnév = a fajta nevének
                            ékezet nélküli, kisbetűs, kötőjeles változata
                            (pl. `magyar-vizsla.png`). Csak azoknál a
                            fajtáknál van kép, amelyeknél a `KEPEK` szótárban
                            (`scripts/fajtak_kepek.py`) szerepel bejegyzés —
                            3 fajtánál (Chow chow, Nagypudli, Pekingi
                            palotakutya) szándékosan nincs kép, mert a
                            forráskép náluk rossz/másik fajtát mutatott.
scripts/fajtak_epit.py      ALAPADATOK (120 fajta neve/mérete/csoportja) + generátor
                             (fajtak.json ÉS fajtak.js), a KEPEK szótárból tölti a "kep" mezőt
scripts/fajtak_adatok.py     SZOVEGEK szótár: minden fajtához 10 erősség + 10 hátrány
scripts/fajtak_kepek.py       KEPEK szótár: fajta név -> assets/kep/fajtak/ fájlnév
                               (csak azoknál a fajtáknál, ahol van beazonosított kép)
scripts/ellenoriz.py          Ellenőrző szkript: minden fajtánál megvan-e a 10+10
```

Fajtaszöveg módosításakor mindig ezt a sorrendet kövesd:
1. Szerkeszd a `scripts/fajtak_adatok.py`-t (SZOVEGEK szótár).
2. Futtasd: `python3 scripts/fajtak_epit.py` (újragenerálja a `data/fajtak.json`-t
   ÉS a `data/fajtak.js`-t).
3. Futtasd: `python3 scripts/ellenoriz.py` (ellenőrzi a 10+10 szabályt, nem nulla
   kilépési kóddal jelez, ha valami hiányos).
4. Soha ne szerkeszd közvetlenül a `data/fajtak.json`-t vagy `data/fajtak.js`-t,
   mindig felülíródik.

Fajtakártya-fénykép hozzáadásakor/cseréjekor:
1. Tedd be a képet az `assets/kep/fajtak/` mappába (átlátszó hátterű PNG
   ajánlott, hogy illeszkedjen a kártya pasztell körkeretéhez).
2. Vedd fel a `scripts/fajtak_kepek.py` `KEPEK` szótárába: `"Fajta neve":
   "fajlnev.png"`.
3. Futtasd újra a `python3 scripts/fajtak_epit.py`-t.
4. `js/fajtak.js` a `fajta.kep` mező alapján dönti el, hogy legyen-e fotó a
   kártyán (`.fajta-fenykep` — ha nincs `kep` mező, nem jelenik meg semmi,
   nincs törött kép ikon).

## Márka / vizuális szabályok

Pasztell, kézzel rajzolt, családbarát hangulat. Sok fehér tér, erősen
lekerekített formák. **Csak** a lenti CSS-változókat használd színekhez — ne
vezess be új hexát.

```css
--rozsaszin: #F97BA6;       /* fő rózsaszín */
--rozsaszin-sotet: #E85D8D;  /* sötétebb rózsaszín (hover, cím-kiemelés) */
--rozsaszin-halvany: #FDEDF2; /* halvány rózsaszín háttér */
--sarga: #F5C518;
--sarga-halvany: #FDF4DC;
--kek: #7FB9E6;
--kek-halvany: #E8F2FB;
--szoveg: #3D3A38;
--szoveg-halvany: #6E6764;
--sugar-kartya: 26px;   /* kártyák lekerekítése */
--sugar-gomb: 99px;      /* gombok lekerekítése (pill) */
```

**Fix színkódolás** — mindenhol (kártyák, gombok, árlista) ugyanaz:
- Terápiás foglalkozások intézményeknek → **rózsaszín**
- Kölyökkutya felkészítés → **sárga**
- Fajtaválasztási tanácsadás → **kék**

Betűtípusok (Google Fontsról, `<link>` tag, nincs helyi másolat):
- **Caveat** — címsorok, logó, fajtanevek a fajtakártyákon
- **Nunito** — törzsszöveg, gombok, navigáció

## Árazás (mindig ezt tükrözze az oldal)

| Szolgáltatás | Ár |
|---|---|
| Terápiás foglalkozás intézményeknek (iskolák, kórházak, idősotthonok, munkahelyek; kiégés-megelőző beszélgetések) | Egyéni megbeszélés alapján |
| Kölyökkutya felkészítés (max. 5 hónapos korig; szobatisztaság, alaptrükkök, kezelési tanácsok) | 100.000 Ft / hó |
| Fajtaválasztási tanácsadás (mely fajta illik, melyiktől óvnánk) | 7.500 Ft |

## Elérhetőségek

- Telefon: +36 20 379 6098
- E-mail: terapiasfoglalkozas@gmail.com
- Helyszín: Nágocs, Magyarország
- Szlogen: „Együtt · Gyógyítunk · Nevelünk" / „Mert a szeretet négy lábon jár."

## Tartalmi szabályok

- Minden felhasználó felé mutatott szöveg magyarul, az osztálynevek és
  azonosítók is magyarul (pl. `.kartya`, `.gomb--rozsaszin`, `.fajta-kartya`).
- Fajtaszövegek: fajtánként pontosan 10 erősség + 10 hátrány, mondatonként
  6–16 szó, konkrét és ellenőrizhető állítás (ne "aranyos", hanem konkrét
  tulajdonság). Legalább 2 erősség a terápiás/intézményi alkalmasságról
  szóljon fajtánként. Egyetlen mondat se ismétlődjön szó szerint két fajta
  között — ezt a `scripts/` mappában lévő szkriptek nem ellenőrzik
  automatikusan, kézzel/ad hoc szkripttel kell validálni módosítás után
  (lásd a `Counter`-alapú duplikátumkeresést a git történetben).
- Nincs gyógyhatású ígéret ("garantáltan csökkenti", "gyógyítja"), a hangnem
  óvatos: megelőzés, jóllét, feszültségoldás.
- Nincs stockfotó / harmadik féltől származó kép. Csak a tulajdonos által
  biztosított, saját képek kerülhetnek be. Képek helye és névkonvenciója az
  `assets/kep/` mappában:
  - `logo.png` — a "Szívhíd" felirat logó a fejlécben (`.logo-kep`). Ha
    hiányzik, a JS `onerror` eltünteti a képet, és a `.logo-nev` span
    (elrejtve `display:none`-nal) megjelenik helyette, így a fejléc "Szívhíd
    terápia" szöveggé esik vissza.
  - `hero-kutyak.jpg` — a főoldal hero szekciójának fotója. Amíg nincs
    feltöltve, pasztell placeholder látszik (`index.html`
    `.hero-kep-placeholder`, JS `onerror` kezeli az eltüntetést).
  - `rolunk-kislany-kutya.jpg` — a Rólunk szekció illusztrációja. Ugyanaz az
    onerror-alapú placeholder-minta, mint a hero képnél
    (`.rolunk-kep-placeholder`).

## Technikai elvárások

- Működjön 360px széles nézetben (tesztelve Playwright-tal).
- Látható fókuszgyűrű minden interaktív elemen (`:focus-visible` a
  `stilus.css`-ben, ne távolítsd el).
- `prefers-reduced-motion: reduce` esetén az animációk/átmenetek gyakorlatilag
  kikapcsolnak (lásd a `stilus.css` tetején).
- A kapcsolatűrlapnak nincs backend párja: a "Üzenet küldése" gomb egy
  `mailto:` linket nyit meg előre kitöltött tárggyal és törzzsel
  (`js/szkript.js`).
- A fajták oldal keresése ékezet-független (NFD normalizálás + ékezetek
  eltávolítása, lásd `js/fajtak.js` `ekezetNelkul` függvénye).
