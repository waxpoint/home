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
  function resolve(el, attr) {
    var key = el.getAttribute(attr);
    return resolvers[key] ? resolvers[key](el) : "";
  }

  // Configurable links: hide anything not set yet
  document.querySelectorAll("[data-link]").forEach(function (el) {
    var url = resolve(el, "data-link");
    if (url) {
      el.setAttribute("href", url);
      if (/^https?:/.test(url)) { el.target = "_blank"; el.rel = "noopener"; }
    } else el.setAttribute("data-link-hidden", "");
  });
  document.querySelectorAll("[data-needs]").forEach(function (el) { if (!resolve(el, "data-needs")) el.setAttribute("data-link-hidden", ""); });
  document.querySelectorAll("[data-missing]").forEach(function (el) { if (resolve(el, "data-missing")) el.setAttribute("data-link-hidden", ""); });

  // Stripe / Klarna course links
  var links = C.payLinks || {};
  document.querySelectorAll("[data-pay]").forEach(function (el) {
    var url = links[el.getAttribute("data-pay")];
    if (url) { el.href = url; el.target = "_blank"; el.rel = "noopener"; }
    else el.setAttribute("data-link-hidden", "");
  });
  if (!Object.keys(links).length) document.querySelectorAll("[data-pay-note]").forEach(function (el) { el.setAttribute("data-link-hidden", ""); });

  // Header: show the scroll-edge shadow only once content passes under it
  var header = document.querySelector(".site-header");
  function onScroll() { header && header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Mobile sheet — opens from the header, closes the same way; never locks input
  var btn = document.querySelector(".menu-btn"), sheet = document.querySelector(".sheet"), scrim = document.querySelector(".scrim");
  function setMenu(open) {
    if (!sheet) return;
    sheet.classList.toggle("open", open); scrim.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.querySelector(".i-open").style.display = open ? "none" : "";
    btn.querySelector(".i-close").style.display = open ? "" : "none";
  }
  if (btn) {
    btn.addEventListener("click", function () { setMenu(!sheet.classList.contains("open")); });
    scrim.addEventListener("click", function () { setMenu(false); });
    sheet.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  }

  // Ladies / Gents segmented control
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var bar = group.querySelector(".tabs"), buttons = group.querySelectorAll("[role=tab]");
    buttons.forEach(function (b, i) {
      b.addEventListener("click", function () {
        bar.setAttribute("data-active", i);
        buttons.forEach(function (x) {
          var on = x === b;
          x.setAttribute("aria-selected", on ? "true" : "false");
          document.getElementById(x.getAttribute("aria-controls")).hidden = !on;
        });
      });
    });
  });

  // Gentle reveal as sections enter the viewport
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add("in"); });

  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
