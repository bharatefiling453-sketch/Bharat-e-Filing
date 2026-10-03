/*
 * Bharat eFiling — shared product-page behaviour (no dependencies, ~3 KB).
 * Every interaction pushes a GA4-style event into window.dataLayer so GTM can
 * forward it to GA4, Google Ads, Meta Pixel, Microsoft UET and Clarity tags.
 */
(function () {
  "use strict";

  window.dataLayer = window.dataLayer || [];
  var page = document.body.dataset.service || "unknown";

  function track(event, params) {
    var payload = Object.assign({ event: event, service: page }, params || {});
    window.dataLayer.push(payload);
  }

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* ---- Table-of-contents scroll-spy ---- */
  var tocLinks = document.querySelectorAll(".toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) {
      byId[a.getAttribute("href").slice(1)] = a;
    });
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          tocLinks.forEach(function (a) {
            a.classList.remove("is-active");
          });
          var link = byId[entry.target.id];
          if (link) link.classList.add("is-active");
        });
      },
      { rootMargin: "-30% 0px -60% 0px" },
    );
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  /* ---- CTA / phone / WhatsApp click tracking ---- */
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track]");
    if (!el) return;
    track(el.dataset.track, {
      cta_location: el.dataset.location || "",
      cta_text: (el.textContent || "").trim().slice(0, 60),
    });
  });

  /* ---- FAQ open tracking (which questions people actually read) ---- */
  document.querySelectorAll(".faq details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) {
        track("faq_open", {
          faq_question: d.querySelector("summary").textContent.trim(),
        });
      }
    });
  });

  /* ---- Scroll depth (25/50/75/100) ---- */
  var marks = [25, 50, 75, 100];
  window.addEventListener(
    "scroll",
    function () {
      var h = document.documentElement;
      var pct = ((h.scrollTop + window.innerHeight) / h.scrollHeight) * 100;
      while (marks.length && pct >= marks[0]) {
        track("scroll_depth", { percent: marks.shift() });
      }
    },
    { passive: true },
  );

  /* ---- UTM / click-ID capture → hidden form fields (lead attribution) ---- */
  var params = new URLSearchParams(window.location.search);
  [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gclid",
    "fbclid",
    "msclkid",
  ].forEach(function (key) {
    var v = params.get(key);
    try {
      if (v) sessionStorage.setItem(key, v);
      else v = sessionStorage.getItem(key);
    } catch (err) {
      /* storage blocked — attribution just falls back to empty */
    }
    document
      .querySelectorAll("input[name='" + key + "']")
      .forEach(function (input) {
        input.value = v || "";
      });
  });

  /* ---- Lead form: accessible inline validation ---- */
  var rules = {
    name: {
      test: /^[A-Za-zऀ-ॿ .'-]{2,60}$/,
      msg: "Please enter your full name.",
    },
    phone: {
      test: /^[6-9]\d{9}$/,
      msg: "Enter a valid 10-digit Indian mobile number.",
    },
    email: {
      test: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/,
      msg: "Enter a valid email address.",
    },
  };

  document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
    var started = false;
    form.addEventListener("input", function () {
      if (!started) {
        started = true;
        track("form_start", { form_id: form.id });
      }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      Object.keys(rules).forEach(function (name) {
        var input = form.elements[name];
        if (!input) return;
        var value = input.value
          .trim()
          .replace(/\s+/g, name === "phone" ? "" : " ");
        if (name === "phone") value = value.replace(/^(\+91|0)/, "");
        var ok = rules[name].test.test(value);
        var err = document.getElementById(
          input.getAttribute("aria-describedby"),
        );
        input.setAttribute("aria-invalid", String(!ok));
        if (err) err.textContent = ok ? "" : rules[name].msg;
        if (!ok && !firstBad) firstBad = input;
      });
      if (firstBad) {
        firstBad.focus();
        return;
      }

      // TODO(dev): POST to CRM / WooCommerce / Zoho endpoint here, then show success.
      track("generate_lead", {
        form_id: form.id,
        value: Number(form.dataset.value || 0),
        currency: "INR",
      });
      form.innerHTML =
        '<p class="form-success" role="status">Thank you! A GST expert will call you within 30 working minutes.</p>';
    });
  });
})();
