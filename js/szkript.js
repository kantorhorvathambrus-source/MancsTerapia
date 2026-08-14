// Tappancs Terápia — közös viselkedés (menü, kapcsolatűrlap)

document.addEventListener("DOMContentLoaded", function () {
  var menuGomb = document.getElementById("menu-gomb");
  var navigacio = document.getElementById("navigacio");

  if (menuGomb && navigacio) {
    menuGomb.addEventListener("click", function () {
      var nyitva = navigacio.classList.toggle("nyitva");
      menuGomb.setAttribute("aria-expanded", nyitva ? "true" : "false");
    });

    navigacio.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navigacio.classList.remove("nyitva");
        menuGomb.setAttribute("aria-expanded", "false");
      });
    });
  }

  var urlap = document.getElementById("kapcsolat-urlap");
  if (urlap) {
    urlap.addEventListener("submit", function (esemeny) {
      esemeny.preventDefault();

      var nev = urlap.nev.value.trim();
      var intezmeny = urlap.intezmeny.value.trim();
      var email = urlap.email.value.trim();
      var temakor = urlap.temakor.value;
      var uzenet = urlap.uzenet.value.trim();

      var targy = "Kapcsolatfelvétel – " + temakor;
      var torzs = "Név: " + nev + "\n" +
        (intezmeny ? "Intézmény: " + intezmeny + "\n" : "") +
        "E-mail: " + email + "\n" +
        "Témakör: " + temakor + "\n\n" +
        uzenet;

      var mailtoLink = "mailto:terapiasfoglalkozas@gmail.com" +
        "?subject=" + encodeURIComponent(targy) +
        "&body=" + encodeURIComponent(torzs);

      window.location.href = mailtoLink;
    });
  }
});
