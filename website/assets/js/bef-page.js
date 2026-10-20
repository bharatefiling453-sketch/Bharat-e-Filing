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

  /* ---- Local nav scroll-spy (highlights the section in view) ---- */
  var tocLinks = document.querySelectorAll(".localnav ul a[href^='#'], .toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      (byId[id] = byId[id] || []).push(a);
    });
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          tocLinks.forEach(function (a) {
            a.classList.remove("is-active");
          });
          (byId[entry.target.id] || []).forEach(function (l) {
            l.classList.add("is-active");
          });
        });
      },
      { rootMargin: "-30% 0px -60% 0px" },
    );
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  /* ---- Blog: reading progress bar and copy-link button ---- */
  var bar = document.querySelector(".read-progress");
  var article = document.querySelector("[data-article]");
  if (bar && article) {
    var ticking = false;
    var paint = function () {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      bar.style.transform = "scaleX(" + p.toFixed(3) + ")";
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(paint);
        }
      },
      { passive: true },
    );
    paint();
  }
  document.querySelectorAll("[data-copy-link]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var done = function () {
        btn.setAttribute("data-copied", "true");
        btn.querySelector("span").textContent = "Link copied";
        track("share", { method: "copy_link" });
      };
      var url = (document.querySelector("link[rel=canonical]") || {}).href || location.href;
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, done);
      else done();
    });
  });

  /* ---- Gentle reveal-on-scroll (disabled by CSS for reduced-motion users) ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var revealer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            revealer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -10% 0px" },
    );
    reveals.forEach(function (el) {
      revealer.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add("is-in");
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

  var leadSubmitted = false;

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
      var plan =
        form.querySelector("[name='plan']:checked") || form.elements.plan;
      var planOption =
        plan && plan.options ? plan.options[plan.selectedIndex] : plan;
      track("generate_lead", {
        form_id: form.id,
        plan: plan ? plan.value : "",
        value: Number(
          (planOption && planOption.dataset.price) || form.dataset.value || 0,
        ),
        currency: "INR",
      });
      leadSubmitted = true;
      try {
        sessionStorage.setItem("bef_lead", "1");
      } catch (err) {
        /* ignore */
      }
      form.innerHTML =
        '<p class="form-success" role="status">Thank you! A GST expert will call you within 30 working minutes.</p>';
    });
  });
  /* ---- Count-up numbers: [data-count-to]. The HTML already holds the final value (no-JS and SEO safe). ---- */
  var counters = document.querySelectorAll("[data-count-to]");
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (counters.length && "IntersectionObserver" in window && !calm) {
    var countIo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          countIo.unobserve(entry.target);
          var el = entry.target, to = Number(el.getAttribute("data-count-to")), t0 = null;
          var step = function (t) {
            if (t0 === null) t0 = t;
            var k = Math.min(1, (t - t0) / 1200);
            el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))).toLocaleString("en-IN");
            if (k < 1) window.requestAnimationFrame(step);
          };
          el.textContent = "0";
          window.requestAnimationFrame(step);
        });
      },
      { threshold: 0.6 },
    );
    counters.forEach(function (el) {
      countIo.observe(el);
    });
  }

  /* ---- Reviews carousel: [data-t-scroll="-1|1"] buttons scroll the .t-track by one card ---- */
  document.querySelectorAll("[data-t-scroll]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var track = document.getElementById(btn.getAttribute("aria-controls"));
      if (!track) return;
      var card = track.firstElementChild;
      var w = card ? card.getBoundingClientRect().width + 20 : track.clientWidth * 0.8;
      track.scrollBy({ left: Number(btn.getAttribute("data-t-scroll")) * w, behavior: calm ? "auto" : "smooth" });
    });
  });

  /* ---- Optional images: hide a missing photo so its gradient panel still looks finished ---- */
  document.querySelectorAll("img[data-optional]").forEach(function (img) {
    var hide = function () {
      img.hidden = true;
    };
    if (img.complete && img.naturalWidth === 0 && img.getAttribute("src")) hide();
    img.addEventListener("error", hide);
  });

  /* ---- Promo slider: autoplay, dots, progress bar, swipe; pauses on hover/focus and when off screen ---- */
  document.querySelectorAll("[data-promo]").forEach(function (frame) {
    var track = frame.querySelector(".promo__track");
    var slides = Array.prototype.slice.call(track.children);
    var dotsBox = frame.parentElement.querySelector("[data-promo-dots]");
    var bar = frame.querySelector("[data-promo-progress]");
    var DELAY = 5500, i = 0, t0 = performance.now(), paused = false, visible = true;
    var dots = slides.map(function (_, n) {
      var b = document.createElement("button");
      b.type = "button";
      b.innerHTML = '<span class="visually-hidden">Show slide ' + (n + 1) + "</span>";
      b.addEventListener("click", function () {
        go(n);
      });
      dotsBox && dotsBox.appendChild(b);
      return b;
    });
    function go(n) {
      i = (n + slides.length) % slides.length;
      track.style.transform = "translateX(" + -100 * i + "%)";
      slides.forEach(function (sl, k) {
        sl.setAttribute("aria-hidden", k === i ? "false" : "true");
        if ("inert" in sl) sl.inert = k !== i;
      });
      dots.forEach(function (d, k) {
        d.setAttribute("aria-current", k === i ? "true" : "false");
      });
      t0 = performance.now();
    }
    go(0);
    if (calm) return;
    frame.addEventListener("mouseenter", function () {
      paused = true;
    });
    frame.addEventListener("mouseleave", function () {
      paused = false;
      t0 = performance.now() - (parseFloat(bar && bar.style.width) || 0) * DELAY / 100;
    });
    frame.addEventListener("focusin", function () {
      paused = true;
    });
    frame.addEventListener("focusout", function () {
      paused = false;
    });
    if ("IntersectionObserver" in window)
      new IntersectionObserver(function (e) {
        visible = e[0].isIntersecting;
      }).observe(frame);
    var x0 = null;
    frame.addEventListener("touchstart", function (e) {
      x0 = e.touches[0].clientX;
    }, { passive: true });
    frame.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1));
      x0 = null;
    });
    (function loop(now) {
      if (paused || !visible) t0 += now - (loop.last || now);
      loop.last = now;
      var k = (now - t0) / DELAY;
      if (k >= 1) go(i + 1);
      else if (bar) bar.style.width = k * 100 + "%";
      window.requestAnimationFrame(loop);
    })(performance.now());
  });

  /* ---- "Fetching → done" loop on [data-fetch] lists ---- */
  document.querySelectorAll("[data-fetch]").forEach(function (list) {
    var rows = list.querySelectorAll("li");
    var step = 0;
    function paint() {
      rows.forEach(function (r, k) {
        r.classList.toggle("is-done", k < step);
        r.classList.toggle("is-active", k === step);
        r.querySelector("em").textContent = k < step ? "Auto-filled" : "Fetching";
      });
    }
    paint();
    if (calm) {
      step = rows.length;
      paint();
      return;
    }
    window.setInterval(function () {
      step = step >= rows.length + 1 ? 0 : step + 1;
      paint();
    }, 1100);
  });

  /* ---- Call timers: count up mm:ss ---- */
  document.querySelectorAll("[data-call-timer]").forEach(function (el) {
    var p = el.textContent.split(":"), sec = Number(p[0]) * 60 + Number(p[1]);
    window.setInterval(function () {
      sec++;
      el.textContent = String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
    }, 1000);
  });

  /* ---- Sticky promo bar: after the first screen, hidden over the footer and once closed (per session) ---- */
  var promoBar = document.querySelector("[data-promo-bar]");
  if (promoBar) {
    var closed = false;
    try {
      closed = sessionStorage.getItem("bef_promo_bar") === "closed";
    } catch (e) {}
    var foot = document.querySelector(".footer");
    var paintBar = function () {
      var footTop = foot ? foot.getBoundingClientRect().top : Infinity;
      promoBar.classList.toggle("is-on", !closed && window.scrollY > window.innerHeight * 0.9 && footTop > window.innerHeight);
    };
    window.addEventListener("scroll", paintBar, { passive: true });
    paintBar();
    var x = promoBar.querySelector("[data-promo-bar-close]");
    x &&
      x.addEventListener("click", function () {
        closed = true;
        try {
          sessionStorage.setItem("bef_promo_bar", "closed");
        } catch (e) {}
        paintBar();
      });
  }

  /* ---- "In view" markers for timeline dots and the process stepper ---- */
  var inViewEls = document.querySelectorAll(".timeline__item, .stepper");
  if ("IntersectionObserver" in window) {
    var inView = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            inView.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -25% 0px" },
    );
    inViewEls.forEach(function (el) {
      inView.observe(el);
    });
  } else {
    inViewEls.forEach(function (el) {
      el.classList.add("is-in");
    });
  }

  /* ---- Timeline line fills with scroll ---- */
  var timelines = document.querySelectorAll(".timeline");
  var ticking = false;
  function paintTimelines() {
    ticking = false;
    var mid = window.innerHeight * 0.6;
    timelines.forEach(function (tl) {
      var r = tl.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
      tl.style.setProperty("--progress", p.toFixed(3));
    });
  }
  if (timelines.length) {
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          window.requestAnimationFrame(paintTimelines);
        }
      },
      { passive: true },
    );
    window.requestAnimationFrame(paintTimelines);
  }

  /* ---- Lead pop-up: opens from CTAs, on exit intent, or after 45 s (once per session) ---- */
  var modal = document.getElementById("lead-modal");
  var canModal = modal && typeof modal.showModal === "function";

  function seen(key) {
    try {
      return sessionStorage.getItem(key) === "1";
    } catch (err) {
      return false;
    }
  }

  function remember(key) {
    try {
      sessionStorage.setItem(key, "1");
    } catch (err) {
      /* ignore */
    }
  }

  function openModal(trigger, plan) {
    if (!canModal || modal.open) return false;
    var select = modal.querySelector("select[name='plan']");
    if (select && plan) select.value = plan;
    modal.showModal();
    remember("bef_popup_seen");
    track("popup_open", { trigger: trigger });
    return true;
  }

  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-modal-open]");
    if (!opener) return;
    if (openModal(opener.dataset.location || "button", opener.dataset.plan))
      e.preventDefault();
  });

  if (canModal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) modal.close();
    });
    modal.querySelectorAll("[data-modal-close]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        modal.close();
      });
    });

    var autoAllowed = function () {
      return !leadSubmitted && !seen("bef_popup_seen") && !seen("bef_lead");
    };
    // Desktop exit intent: pointer leaves through the top of the window
    document.addEventListener("mouseout", function (e) {
      if (
        !e.relatedTarget &&
        e.clientY <= 0 &&
        window.innerWidth >= 1024 &&
        autoAllowed()
      ) {
        openModal("exit_intent");
      }
    });
    // Gentle timed prompt — only if the visitor has been reading for a while
    window.setTimeout(function () {
      var scrolled = window.scrollY > window.innerHeight * 0.8;
      var typing =
        document.activeElement &&
        /INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName);
      if (scrolled && !typing && autoAllowed()) openModal("timer");
    }, 45000);
  }
})();
