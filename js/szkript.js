// Szívhíd terápia — közös viselkedés (menü, kapcsolatűrlap)

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
  var urlapSiker = document.getElementById("urlap-siker");
  var urlapHiba = document.getElementById("urlap-hiba");

  if (urlap) {
    urlap.addEventListener("submit", function (esemeny) {
      esemeny.preventDefault();

      if (urlapHiba) urlapHiba.hidden = true;

      var adatok = new URLSearchParams(new FormData(urlap)).toString();

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: adatok,
      })
        .then(function (valasz) {
          if (!valasz.ok) throw new Error("Sikertelen küldés: " + valasz.status);
          urlap.hidden = true;
          if (urlapSiker) {
            urlapSiker.hidden = false;
            urlapSiker.focus();
          }
        })
        .catch(function (hiba) {
          console.error(hiba);
          if (urlapHiba) {
            urlapHiba.hidden = false;
            urlapHiba.focus();
          }
        });
    });
  }
});
