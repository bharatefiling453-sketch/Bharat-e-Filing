    <script>
      /* LLP registration: live LLP calendar, set-up checker, first-year calendar and audit check (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* LLP Act, 2008: at least two partners (section 6); at least two designated partners who are individuals, one resident in India,
           i.e. 120 days in the financial year (section 7, as amended in 2021). LLP agreement in Form 3 within 30 days of incorporation (rule 21);
           Form 11 by 30 May and Form 8 by 30 October, ₹100 a day each when late. An LLP incorporated after 30 September may end its first financial
           year on 31 March of the following year (section 2(1)(l)). Audit not required if turnover ≤ ₹40 lakh or contribution ≤ ₹25 lakh
           (rule 24(8)). */
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
        function isoDate(d) {
          return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
        }
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
        }
        function fyLabel(endYear) {
          return "FY " + (endYear - 1) + "-" + String(endYear).slice(2);
        }
        function nextYearly(today, m, d) {
          var x = new Date(today.getFullYear(), m, d);
          return x < today ? new Date(today.getFullYear() + 1, m, d) : x;
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
          window.dataLayer.push({ event: "calculator_use", service: "llp-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live LLP calendar ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var f3 = addDays(today, 30);
          var end = new Date(f3.getFullYear(), f3.getMonth(), f3.getDate(), 23, 59, 59);
          setText("[data-form3]", dmy(f3));
          var f11 = nextYearly(today, 4, 30), f8 = nextYearly(today, 9, 30);
          setText("[data-f11-by]", dmy(f11));
          setText("[data-f11-label]", "Form 11 for " + fyLabel(f11.getFullYear()) + " is due by");
          setText("[data-f8-by]", dmy(f8));
          setText("[data-f8-label]", "Form 8 for " + fyLabel(f8.getFullYear()) + " is due by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='form3']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours to file Form 3 for an LLP incorporated today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Set-up checker ---- */
        var sc = document.getElementById("setup-check");
        if (sc) {
          var renderSetup = function () {
            var p = Math.max(0, Math.round(Number(sc.querySelector("[name='partners']").value) || 0));
            var dp = Math.max(0, Math.round(Number(sc.querySelector("[name='dps']").value) || 0));
            var res = sc.querySelector("[name='resident']").checked;
            var issues = [];
            if (p < 2) issues.push("An LLP needs at least two partners.");
            if (dp < 2) issues.push("At least two designated partners, who are individuals, are needed.");
            if (dp > p) issues.push("Designated partners must also be partners, so they can’t outnumber the partners.");
            if (!res) issues.push("At least one designated partner must be resident in India (120 days in the financial year).");
            var v = document.getElementById("sc-verdict");
            if (issues.length) {
              v.textContent = issues.length + (issues.length === 1 ? " thing" : " things") + " to fix before filing.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Your set-up meets the LLP Act’s requirements.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("sc-out").innerHTML = [
              row("Partners", p + (p >= 2 ? " ✓" : " (min 2)")),
              row("Designated partners", dp + (dp >= 2 && dp <= p ? " ✓" : "")),
              row("Resident designated partner", res ? "Yes" : "Needed"),
              row("Ready for FiLLiP", issues.length ? "Not yet" : "Yes", true),
            ].join("");
            document.getElementById("sc-note").textContent = issues.length ? issues[0] : "There’s no maximum number of partners. Each designated partner needs a DIN, which can be allotted during incorporation.";
          };
          sc.addEventListener("input", function () {
            trackUse("llp_setup");
            renderSetup();
          });
          sc.addEventListener("change", renderSetup);
          renderSetup();
        }

        /* ---- First-year calendar and audit check ---- */
        var cc = document.getElementById("cal-calc");
        if (cc) {
          var dateIn = cc.querySelector("[name='incdate']");
          dateIn.value = isoDate(day(new Date()));
          var renderCal = function () {
            var inc = parse(dateIn.value);
            if (!inc) return;
            var turn = Math.max(0, Number(cc.querySelector("[name='turnover']").value) || 0);
            var contrib = Math.max(0, Number(cc.querySelector("[name='contribution']").value) || 0);
            var m = inc.getMonth(), y = inc.getFullYear();
            var fyEndYear = m >= 3 ? y + 1 : y;
            var option = m >= 9 || m <= 2;
            var audit = turn > 40 && contrib > 25;
            var v = document.getElementById("cc-verdict");
            v.textContent = audit ? "An LLP audit applies on these figures." : "No LLP audit needed on these figures.";
            v.className = "result__verdict " + (audit ? "is-yes" : "is-no");
            document.getElementById("cc-out").innerHTML = [
              row("Form 3 by", dmy(addDays(inc, 30))),
              row("First year ends", "31 Mar " + fyEndYear + (option ? " (or " + (fyEndYear + 1) + ")" : "")),
              row("Form 11 by", dmy(new Date(fyEndYear, 4, 30))),
              row("Form 8 by", dmy(new Date(fyEndYear, 9, 30)), true),
            ].join("");
            document.getElementById("cc-note").textContent =
              (option ? "Incorporated after 30 September, the LLP may end its first financial year on 31 March of the following year, which moves Form 8 and 11 a year later. " : "") +
              "Audit is needed only if turnover exceeds ₹40 lakh and contribution exceeds ₹25 lakh; tax audit rules apply separately.";
          };
          cc.addEventListener("input", function () {
            trackUse("llp_calendar");
            renderCal();
          });
          cc.addEventListener("change", renderCal);
          renderCal();
        }
      })();
    </script>
