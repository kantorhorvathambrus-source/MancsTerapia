// Tappancs Terápia — fajták oldal: adatbetöltés, keresés, méretszűrés

document.addEventListener("DOMContentLoaded", function () {
  var racs = document.getElementById("fajta-racs");
  var kereso = document.getElementById("fajta-kereso");
  var talalatokSzam = document.getElementById("talalatok-szam");
  var nincsTalalat = document.getElementById("nincs-talalat");
  var meretGombok = document.querySelectorAll(".meret-gomb");

  var osszesFajta = [];
  var aktivMeret = "mind";
  var aktivKereses = "";

  function ekezetNelkul(szoveg) {
    return szoveg
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "");
  }

  function kartyaLetrehozasa(fajta) {
    var details = document.createElement("details");
    details.className = "fajta-kartya";
    details.dataset.nev = ekezetNelkul(fajta.nev);
    details.dataset.meret = fajta.meret;

    var summary = document.createElement("summary");
    summary.innerHTML =
      '<div>' +
        '<h3 class="fajta-nev">' + fajta.nev + '</h3>' +
        '<div class="fajta-cimkek">' +
          '<span class="cimke">' + meretCimke(fajta.meret) + '</span>' +
          '<span class="cimke cimke--csoport">' + fajta.csoport + '</span>' +
        '</div>' +
      '</div>' +
      '<span class="fajta-nyil" aria-hidden="true">▾</span>';

    var reszletek = document.createElement("div");
    reszletek.className = "fajta-reszletek";
    reszletek.innerHTML =
      '<div class="fajta-oszlop fajta-oszlop--erossegek">' +
        '<h4>Erősségek</h4>' +
        '<ul>' + fajta.erossegek.map(function (e) { return "<li>" + e + "</li>"; }).join("") + '</ul>' +
      '</div>' +
      '<div class="fajta-oszlop fajta-oszlop--hatranyok">' +
        '<h4>Amire figyelni kell</h4>' +
        '<ul>' + fajta.hatranyok.map(function (h) { return "<li>" + h + "</li>"; }).join("") + '</ul>' +
      '</div>';

    details.appendChild(summary);
    details.appendChild(reszletek);
    return details;
  }

  function meretCimke(meret) {
    if (meret === "kicsi") return "Kis testű";
    if (meret === "kozepes") return "Közepes testű";
    if (meret === "nagy") return "Nagy testű";
    return meret;
  }

  function listaFrissitese() {
    var lathatokSzama = 0;
    var elemek = racs.querySelectorAll(".fajta-kartya");

    elemek.forEach(function (elem) {
      var meretMegfelel = aktivMeret === "mind" || elem.dataset.meret === aktivMeret;
      var keresesMegfelel = aktivKereses === "" || elem.dataset.nev.indexOf(aktivKereses) !== -1;
      var lathato = meretMegfelel && keresesMegfelel;
      elem.style.display = lathato ? "" : "none";
      if (lathato) lathatokSzama++;
    });

    talalatokSzam.textContent = lathatokSzama + " fajta látható a(z) " + osszesFajta.length + " közül";
    nincsTalalat.classList.toggle("lathato", lathatokSzama === 0);
  }

  fetch("data/fajtak.json")
    .then(function (valasz) { return valasz.json(); })
    .then(function (adatok) {
      osszesFajta = adatok;
      var toredek = document.createDocumentFragment();
      adatok.forEach(function (fajta) {
        toredek.appendChild(kartyaLetrehozasa(fajta));
      });
      racs.appendChild(toredek);
      listaFrissitese();
    })
    .catch(function (hiba) {
      racs.innerHTML = '<p>A fajták betöltése sikertelen. Próbáld frissíteni az oldalt.</p>';
      console.error(hiba);
    });

  if (kereso) {
    kereso.addEventListener("input", function () {
      aktivKereses = ekezetNelkul(kereso.value.trim());
      listaFrissitese();
    });
  }

  meretGombok.forEach(function (gomb) {
    gomb.addEventListener("click", function () {
      meretGombok.forEach(function (g) { g.setAttribute("aria-pressed", "false"); });
      gomb.setAttribute("aria-pressed", "true");
      aktivMeret = gomb.dataset.meret;
      listaFrissitese();
    });
  });
});
