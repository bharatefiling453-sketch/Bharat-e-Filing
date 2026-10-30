    <script>
      /* Partnership firm: live tax dates, registration readiness checker, partner remuneration limit calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Indian Partnership Act, 1932: registration under section 58; section 69 disabilities for unregistered firms. Partners: 2 to 50 (Companies
           Act, 2013, section 464 and rule 10 of the Companies (Miscellaneous) Rules, 2014). Partner remuneration limits on book profit (section 40(b)
           of the 1961 Act, as amended from AY 2025-26): first ₹6 lakh or a loss: higher of ₹3 lakh or 90%; balance: 60%. Interest on capital up to
           12% simple. TDS at 10% on partner payments above ₹20,000 a year from 1 April 2025 (section 194T, carried into the 2025 Act). */
        var STEPS = [[6, 15, "1st"], [9, 15, "2nd"], [12, 15, "3rd"], [3, 15, "4th"]];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function fyStart(d) {
          return d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1;
        }
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
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
          window.dataLayer.push({ event: "calculator_use", service: "partnership-firm-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live tax dates ---- */
        function tick() {
          var now = new Date(), today = day(now), fy = fyStart(today);
          var list = [];
          [fy, fy + 1].forEach(function (y) {
            STEPS.forEach(function (s) {
              list.push({ d: new Date(s[0] === 3 ? y + 1 : y, s[0] - 1, s[1]), n: s[2] });
            });
          });
          var next = list.filter(function (x) {
            return x.d >= today;
          })[0];
          var end = new Date(next.d.getFullYear(), next.d.getMonth(), next.d.getDate(), 23, 59, 59);
          setText("[data-adv-due]", dmy(next.d));
          setText("[data-adv-label]", "The firm’s " + next.n + " advance tax instalment is due in");
          var gst = new Date(today.getFullYear(), today.getMonth(), 20);
          if (gst < today) gst = new Date(today.getFullYear(), today.getMonth() + 1, 20);
          var gm = new Date(gst.getFullYear(), gst.getMonth() - 1, 1);
          setText("[data-gst-by]", dmy(gst));
          setText("[data-gst-label]", "GSTR-3B for " + MONTHS[gm.getMonth()] + " " + gm.getFullYear() + " is due by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='advtax']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next advance tax instalment");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Registration readiness checker ---- */
        var fc = document.getElementById("firm-check");
        if (fc) {
          var renderFirm = function () {
            var n = Math.max(0, Math.round(Number(fc.querySelector("[name='partners']").value) || 0));
            var items = [["deed", "Deed signed"], ["stamp", "Deed stamped"], ["pan", "Firm PAN"], ["premises", "Premises proof"]];
            var v = document.getElementById("fc-verdict"), rows = [row("Partners", String(n))], missing = [];
            if (n < 2 || n > 50) {
              v.textContent = n < 2 ? "A firm needs at least two partners." : "A firm can’t have more than 50 partners.";
              v.className = "result__verdict is-yes";
              rows.push(row("Allowed", "2 to 50", true));
              document.getElementById("fc-out").innerHTML = rows.join("");
              document.getElementById("fc-note").textContent =
                n < 2 ? "With one owner, consider a proprietorship or a one person company." : "With more than 50 partners, consider an LLP or a company.";
              return;
            }
            items.forEach(function (it) {
              var ok = fc.querySelector("[name='" + it[0] + "']").checked;
              if (!ok) missing.push(it[1].toLowerCase());
              rows.push(row(it[1], ok ? "Done" : "Pending"));
            });
            rows.push(row("Ready for Registrar", missing.length ? "Not yet" : "Yes", true));
            if (missing.length) {
              v.textContent = missing.length + (missing.length === 1 ? " step" : " steps") + " before you can file.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Ready to file with the Registrar of Firms.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("fc-out").innerHTML = rows.join("");
            document.getElementById("fc-note").textContent = missing.length
              ? "Next: " + missing[0] + ". The section 58 statement must be signed by all partners."
              : "File the section 58 statement with the deed, signed by all partners, in your state’s prescribed form.";
          };
          fc.addEventListener("input", function () {
            trackUse("firm_ready");
            renderFirm();
          });
          fc.addEventListener("change", renderFirm);
          renderFirm();
        }

        /* ---- Partner remuneration limit calculator ---- */
        var rm = document.getElementById("remun-calc");
        if (rm) {
          var renderRem = function () {
            var bp = (Number(rm.querySelector("[name='bookprofit']").value) || 0) * 100000;
            var cap = Math.max(0, Number(rm.querySelector("[name='capital']").value) || 0) * 100000;
            var working = Math.min(50, Math.max(1, Math.round(Number(rm.querySelector("[name='working']").value) || 1)));
            var limit = bp <= 600000 ? Math.max(300000, 0.9 * Math.max(0, bp)) : 540000 + 0.6 * (bp - 600000);
            var each = limit / working, interest = cap * 0.12;
            var v = document.getElementById("rm-verdict");
            v.textContent = "Up to " + inr(limit) + " of remuneration is deductible.";
            v.className = "result__verdict is-no";
            document.getElementById("rm-out").innerHTML = [
              row("Book profit", inr(bp)),
              row("Remuneration limit", inr(limit)),
              row("Each working partner", inr(each)),
              row("Max interest at 12%", inr(interest), true),
            ].join("");
            document.getElementById("rm-note").textContent =
              (each > 20000 ? "TDS at 10% applies to each partner’s payments above ₹20,000 a year. " : "") +
              "Only amounts authorised by the deed are deductible. Limits are from section 40(b) of the 1961 Act as amended from AY 2025-26; a CA confirms the provision for your tax year.";
          };
          rm.addEventListener("input", function () {
            trackUse("partner_remuneration");
            renderRem();
          });
          renderRem();
        }
      })();
    </script>
