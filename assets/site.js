(function () {
  var C = window.WAXPOINT || {};

  function waLink(text) {
    if (!C.whatsapp) return "";
    return "https://wa.me/" + C.whatsapp + (text ? "?text=" + encodeURIComponent(text) : "");
  }

  var resolvers = {
    book: function () { return C.treatwellWidget || C.treatwell || ""; },
    treatwell: function () { return C.treatwell || ""; },
    whatsapp: function (el) { return waLink(el.getAttribute("data-wa-text") || "Hi Wax Point, I'd like to ask about an appointment."); },
    phone: function () { return C.phone ? "tel:" + C.phone : ""; },
    instagram: function () { return C.instagram || ""; },
    form: function () { return C.consultationForm || ""; }
  };

  // Fill configurable links; hide anything whose link isn't set yet.
  document.querySelectorAll("[data-link]").forEach(function (el) {
    var key = el.getAttribute("data-link");
    var url = resolvers[key] ? resolvers[key](el) : "";
    if (url) {
      el.setAttribute("href", url);
      if (/^https?:/.test(url)) { el.setAttribute("target", "_blank"); el.setAttribute("rel", "noopener"); }
    } else {
      el.setAttribute("data-link-hidden", "");
    }
  });
  // Sections that only make sense once a link exists
  document.querySelectorAll("[data-needs]").forEach(function (el) {
    var key = el.getAttribute("data-needs");
    var url = resolvers[key] ? resolvers[key](el) : "";
    if (!url) el.setAttribute("data-link-hidden", "");
  });
  document.querySelectorAll("[data-missing]").forEach(function (el) {
    var key = el.getAttribute("data-missing");
    var url = resolvers[key] ? resolvers[key](el) : "";
    if (url) el.setAttribute("data-link-hidden", "");
  });

  // Stripe / Klarna pay links for laser courses
  var links = C.payLinks || {};
  document.querySelectorAll("[data-pay]").forEach(function (el) {
    var url = links[el.getAttribute("data-pay")];
    if (url) { el.href = url; el.target = "_blank"; el.rel = "noopener"; }
    else el.setAttribute("data-link-hidden", "");
  });
  if (Object.keys(links).length === 0) {
    document.querySelectorAll("[data-pay-note]").forEach(function (el) { el.setAttribute("data-link-hidden", ""); });
  }

  // Mobile menu
  var btn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Ladies / Gents tabs
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var buttons = group.querySelectorAll("[role=tab]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        buttons.forEach(function (x) {
          var on = x === b;
          x.setAttribute("aria-selected", on ? "true" : "false");
          var panel = document.getElementById(x.getAttribute("aria-controls"));
          if (panel) panel.hidden = !on;
        });
      });
    });
  });

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
