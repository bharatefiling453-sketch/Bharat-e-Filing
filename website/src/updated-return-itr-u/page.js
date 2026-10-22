    <script>
      /* Revised & updated return: live correction clock, route finder, ITR-U additional tax calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26 (AY 2026-27): belated by 31 Dec 2026; revised by 31 Mar 2027 with a fee after 31 Dec 2026 (Budget 2026) */
        var BELATED_BY = new Date(2026, 11, 31), REVISE_BY = new Date(2027, 2, 31);
        /* ITR-U (Section 139(8A) as amended by the Finance Act, 2025): 48 months from the end of the AY; 25/50/60/70% additional tax */
        var BANDS = [25, 50, 60, 70];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function ayLabel(start) {
          return "AY " + start + "-" + String(start + 1).slice(2);
        }
        /* AY start-year X ends on 31 March of X+1; ITR-U band k (0..3) runs to 31 March of X+2+k */
        function band(x, today) {
          for (var k = 0; k < 4; k++) if (today <= new Date(x + 2 + k, 2, 31)) return k;
          return -1;
        }
        function openYears(today) {
          var newest = (today.getMonth() >= 3 ? today.getFullYear() : today.getFullYear() - 1) - 1;
          var list = [];
          for (var x = newest; x >= newest - 4; x--) if (band(x, today) >= 0 && today > new Date(x + 1, 2, 31)) list.push(x);
          return list;
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
          window.dataLayer.push({ event: "calculator_use", service: "updated-return-itr-u", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live correction clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var years = openYears(today);
          var newest = years[0], oldest = years[years.length - 1];
          setText("[data-newest-ay]", ayLabel(newest));
          setText("[data-oldest-ay]", ayLabel(oldest));
          setText("[data-oldest-close]", dmy(new Date(oldest + 5, 2, 31)));
          var step = new Date(today.getMonth() >= 3 ? today.getFullYear() + 1 : today.getFullYear(), 2, 31, 23, 59, 59);
          setText("[data-step-date]", dmy(step));
          setText("[data-revise-by]", dmy(REVISE_BY));
          setText("[data-revise-fee]", dmy(BELATED_BY));
          setText("[data-belated-by]", dmy(BELATED_BY));
          var ms = Math.max(0, step - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='step']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until ITR-U additional tax rises");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Which route fits? ---- */
        var rc = document.getElementById("route-check");
        if (rc) {
          var renderRoute = function () {
            var current = rc.querySelector("[name='year']").value === "current";
            var filed = rc.querySelector("[name='filed']:checked").value === "yes";
            var up = rc.querySelector("[name='dir']:checked").value === "up";
            var today = day(new Date()), v = document.getElementById("rc-verdict"), rows = [], note = "", route;
            if (current && !filed && today <= BELATED_BY) {
              route = "Belated return";
              rows.push(row("Section", "139(4)"), row("File by", dmy(BELATED_BY), true));
              note = "Late fee up to ₹5,000 and interest apply, but no additional tax. Cheaper than ITR-U.";
            } else if (current && filed && today <= REVISE_BY) {
              route = "Revised return";
              rows.push(row("Section", "139(5)"), row("File by", dmy(REVISE_BY) + (today > BELATED_BY ? " (fee applies)" : ""), true));
              note = "Works whether the correction raises or cuts tax. You can revise more than once.";
            } else if (up) {
              route = "Updated return (ITR-U)";
              rows.push(row("Section", "139(8A)"), row("Extra cost", "25% to 70% additional tax", true));
              note = "Check the year is within 48 months and not barred. Use the calculator for the exact amount.";
            } else {
              route = "Rectification or condonation";
              rows.push(row("Options", "Section 154 or 119(2)(b)"), row("ITR-U", "Not allowed", true));
              note = "Rectification fixes mistakes apparent from the record; condonation is for genuine hardship cases.";
            }
            v.textContent = "Best route: " + route + ".";
            v.className = "result__verdict " + (route.indexOf("ITR-U") >= 0 || route.indexOf("Rectification") === 0 ? "is-yes" : "is-no");
            document.getElementById("rc-out").innerHTML = rows.join("");
            document.getElementById("rc-note").textContent = note;
          };
          rc.addEventListener("change", function () {
            trackUse("itr_route_finder");
            renderRoute();
          });
          renderRoute();
        }

        /* ---- ITR-U additional tax calculator ---- */
        var ic = document.getElementById("itru-calc");
        if (ic) {
          var sel = ic.querySelector("[name='ay']");
          openYears(day(new Date())).forEach(function (x) {
            var o = document.createElement("option");
            o.value = x;
            o.textContent = ayLabel(x) + " (FY " + (x - 1) + "-" + String(x).slice(2) + ")";
            sel.appendChild(o);
          });
          var renderCalc = function () {
            var x = Number(sel.value), today = day(new Date()), k = band(x, today);
            var tax = Math.max(0, Number(ic.querySelector("[name='tax']").value) || 0);
            var interest = Math.max(0, Number(ic.querySelector("[name='interest']").value) || 0);
            var barred = ic.querySelector("[name='barred']").checked;
            var pct = BANDS[k], extra = ((tax + interest) * pct) / 100;
            var v = document.getElementById("ic-verdict");
            if (barred) {
              v.textContent = "ITR-U may be barred for this year. Talk to a CA first.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Additional tax today: " + pct + "%, about " + inr(extra) + ".";
              v.className = "result__verdict is-no";
            }
            var rows = [row("Rate applies until", dmy(new Date(x + 2 + k, 2, 31)))];
            if (k < 3) rows.push(row("After that", BANDS[k + 1] + "% · " + inr(((tax + interest) * BANDS[k + 1]) / 100)));
            rows.push(row("Last date for this year", dmy(new Date(x + 5, 2, 31))));
            rows.push(row("Total to pay before filing", inr(tax + interest + extra), true));
            document.getElementById("ic-out").innerHTML = rows.join("");
          };
          ic.addEventListener("input", function () {
            trackUse("itr_u_calculator");
            renderCalc();
          });
          ic.addEventListener("change", renderCalc);
          renderCalc();
        }
      })();
    </script>
