    <script>
      /* Trust registration: live trust calendar, trust deed checker, 85% income application check (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Indian Trusts Act, 1882, section 5: a trust of immovable property must be declared by a registered non-testamentary instrument
           (or by will). A registered charitable trust must apply at least 85% of its income to its objects or accumulate it within the rules
           (section 11(1)(a) of the Income-tax Act, 1961; sections 336, 341 and 342 of the Income-tax Act, 2025 from tax year 2026-27).
           Provisional registration lasts three years; regular registration is applied for within six months of starting activities, or
           earlier if provisional registration ends first. Tax years end on 31 March. */
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function lakh(n) {
          return "₹" + (Math.round(n * 100) / 100).toLocaleString("en-IN") + " lakh";
        }
        var setText = function (sel, text) {
          document.querySelectorAll(sel).forEach(function (el) {
            if (el.textContent !== text) el.textContent = text;
          });
        };
        var used = {};
        function trackUse(tool) {
          if (used[tool]) return;
          used[tool] = true;
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({ event: "calculator_use", service: "trust-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live trust calendar ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var endYear = today.getMonth() >= 3 ? today.getFullYear() + 1 : today.getFullYear();
          var yEnd = new Date(endYear, 2, 31), end = new Date(endYear, 2, 31, 23, 59, 59);
          setText("[data-ty-end]", dmy(yEnd));
          setText("[data-ty-label]", "Tax year " + (endYear - 1) + "-" + String(endYear).slice(2));
          setText("[data-reg-by]", dmy(new Date(today.getFullYear(), today.getMonth() + 6, today.getDate())));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='ty']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the tax year ends");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Trust deed checker ---- */
        var dc = document.getElementById("deed-check");
        if (dc) {
          var renderDeed = function () {
            var t = Math.max(0, Math.round(Number(dc.querySelector("[name='trustees']").value) || 0));
            var objects = dc.querySelector("[name='objects']").checked, irr = dc.querySelector("[name='irrevocable']").checked;
            var dis = dc.querySelector("[name='dissolution']").checked, prop = dc.querySelector("[name='property']").checked;
            var issues = [];
            if (t < 1) issues.push("A trust needs at least one trustee.");
            if (!objects) issues.push("For income tax registration as a charity, the objects must be charitable or religious and for the public.");
            if (!irr) issues.push("A revocable trust can make the income taxable in the settlor’s hands and block tax registration. Make the deed irrevocable.");
            if (!dis) issues.push("Add a dissolution clause so that remaining assets go to another charity with similar objects, not to the trustees.");
            var v = document.getElementById("dc-verdict");
            if (issues.length) {
              v.textContent = issues.length + (issues.length === 1 ? " thing" : " things") + " to fix before signing.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Your deed covers the key points.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("dc-out").innerHTML = [
              row("Trustees", t + (t >= 2 ? " ✓" : t === 1 ? " (2+ advised)" : " (min 1)")),
              row("Irrevocable", irr ? "Yes" : "Needed"),
              row("Dissolution clause", dis ? "Yes" : "Needed"),
              row("Registration", prop ? "Compulsory" : "Strongly advised", true),
            ].join("");
            var note = issues.length ? issues[0] : t === 1 ? "A single trustee is allowed, but two or more spread decisions and bank operations." : "Have the settlor and two witnesses sign the deed before the Sub-Registrar.";
            if (!issues.length && prop) note = "With immovable property, the deed must be registered under section 5 of the Indian Trusts Act, 1882.";
            document.getElementById("dc-note").textContent = note;
          };
          dc.addEventListener("input", function () {
            trackUse("trust_deed");
            renderDeed();
          });
          dc.addEventListener("change", renderDeed);
          renderDeed();
        }

        /* ---- 85% income application check ---- */
        var ac = document.getElementById("apply-calc");
        if (ac) {
          var renderApply = function () {
            var inc = Math.max(0, Number(ac.querySelector("[name='income']").value) || 0);
            var app = Math.max(0, Number(ac.querySelector("[name='applied']").value) || 0);
            var acc = Math.max(0, Number(ac.querySelector("[name='accum']").value) || 0);
            var need = inc * 0.85, done = app + acc, short = Math.max(0, need - done);
            var v = document.getElementById("ac-verdict");
            if (short > 0.004) {
              v.textContent = "Short of 85% by " + lakh(short) + ".";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "85% condition met.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("ac-out").innerHTML = [
              row("Must apply (85%)", lakh(need)),
              row("Spent on objects", lakh(app)),
              row("Set aside", lakh(acc)),
              row("Shortfall", short > 0.004 ? lakh(short) : "None", true),
            ].join("");
            document.getElementById("ac-note").textContent =
              (short > 0.004 ? "A shortfall may be taxable unless it is covered by the deemed application or accumulation options within the time limits. " : "") +
              (acc > 0 ? "Setting aside needs a specific purpose, a prescribed form filed in time, and investment in permitted modes. " : "") +
              "Ask your CA before the year ends.";
          };
          ac.addEventListener("input", function () {
            trackUse("trust_85pc");
            renderApply();
          });
          ac.addEventListener("change", renderApply);
          renderApply();
        }
      })();
    </script>
