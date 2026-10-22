    <script>
      /* Trust & NGO tax: live trust compliance clock, 85% application calculator, trust compliance checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26 (AY 2026-27): ITR-7 for audited trusts with CBDT Circular 7/2026; FCRA FC-4 by 31 Dec; Form 10BD/10BE by 31 May */
        var DUE = { itr: new Date(2026, 10, 21), fc4: new Date(2026, 11, 31), belated: new Date(2026, 11, 31), f10bd: new Date(2027, 4, 31) };
        var DEADLINES = [
          [DUE.itr, "Audited trusts file ITR-7 by", true],
          [DUE.fc4, "FCRA Form FC-4 and belated ITR-7 are due on", true],
          [DUE.f10bd, "Form 10BD and 10BE are due on", false],
        ];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function inr(n) {
          var a = Math.abs(n);
          var s = a >= 1e7 ? (a / 1e7).toFixed(2).replace(/\.?0+$/, "") + " crore" : a >= 1e5 ? (a / 1e5).toFixed(2).replace(/\.?0+$/, "") + " lakh" : Math.round(a).toLocaleString("en-IN");
          return (n < 0 ? "−" : "") + "₹" + s;
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
          window.dataLayer.push({ event: "calculator_use", service: "trust-ngo-itr-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        function upcoming(list, today) {
          return list.filter(function (d) {
            return d[0] >= today;
          })[0] || list[list.length - 1];
        }

        /* ---- Live trust compliance clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var next = upcoming(DEADLINES, today);
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-next-label]", next[1]);
          setText("[data-next-date]", dmy(next[0]));
          var itr = upcoming(DEADLINES.filter(function (d) {
            return d[2];
          }), today);
          setText("[data-itr-label]", itr === DEADLINES[0] ? "Audited trusts file ITR-7 by" : "Belated ITR-7 can be filed until");
          setText("[data-itr-date]", dmy(itr[0]));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='next']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left: " + next[1] + " " + dmy(next[0]));
          }
          /* Next FC-4 (31 December) and next Form 10BD / 10BE (31 May) on or after today */
          var nextOn = function (m, d) {
            var x = new Date(today.getFullYear(), m, d);
            return x < today ? new Date(today.getFullYear() + 1, m, d) : x;
          };
          setText("[data-fc4-by]", dmy(nextOn(11, 31)));
          setText("[data-10bd-by]", dmy(nextOn(4, 31)));
          /* 12AB renewal: Form 10AB at least six months before expiry (registrations run to 31 March); next 30 September window */
          var renewBy = new Date(today.getFullYear(), 8, 30);
          if (renewBy < today) renewBy = new Date(today.getFullYear() + 1, 8, 30);
          setText("[data-renew-by]", dmy(renewBy));
          setText("[data-renew-expiry]", dmy(new Date(renewBy.getFullYear() + 1, 2, 31)));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- 85% application calculator (Section 11(1)(a): 15% set-aside; Section 11(2): Form 10 accumulation) ---- */
        var ac = document.getElementById("apply-calc");
        if (ac) {
          var val = function (n) {
            return Math.max(0, Number(ac.querySelector("[name='" + n + "']").value) || 0);
          };
          var renderApply = function () {
            var income = val("income"), applied = val("applied"), form10 = val("form10");
            var needed = income * 0.85;
            var shortfall = Math.max(0, needed - applied - form10);
            var pct = income ? Math.round((applied / income) * 1000) / 10 : 0;
            var v = document.getElementById("ac-verdict");
            v.textContent = shortfall ? "Short by " + inr(shortfall) + ". Accumulate it in Form 10 or it becomes taxable." : "85% rule met. No tax on this income.";
            v.className = "result__verdict " + (shortfall ? "is-yes" : "is-no");
            document.getElementById("ac-out").innerHTML = [
              row("Applied on objects", inr(applied) + " (" + pct + "%)"),
              row("Must apply (85%)", inr(needed)),
              row("Free set-aside (15%)", inr(income * 0.15)),
              row("Taxable shortfall", inr(shortfall)),
              row("Estimated tax at the maximum marginal rate", inr(shortfall * 0.3 * 1.04), true),
            ].join("");
          };
          ac.addEventListener("input", function () {
            trackUse("trust_85_percent");
            renderApply();
          });
          ac.addEventListener("change", renderApply);
          renderApply();
        }

        /* ---- Trust compliance checker (Rules 16CC/17B: Form 10B above ₹5 crore, foreign contribution or application outside India; else 10BB) ---- */
        var nc = document.getElementById("ngo-check");
        if (nc) {
          var renderCheck = function () {
            var total = Math.max(0, Number(nc.querySelector("[name='total']").value) || 0);
            var on = function (n) {
              return nc.querySelector("[name='" + n + "']").checked;
            };
            var audit = total > 250000 || on("fcra");
            var form = total > 5e7 || on("fcra") || on("abroad") ? "Form 10B" : "Form 10BB";
            var v = document.getElementById("nc-verdict");
            v.textContent = audit ? "Audit applies: " + form + ", then ITR-7 by " + dmy(DUE.itr) + "." : "No audit needed. File ITR-7 on time to keep the exemption.";
            v.className = "result__verdict " + (audit ? "is-yes" : "is-no");
            var rows = [row("Audit report", audit ? form + ", one month before the ITR" : "Not required")];
            if (on("fcra")) rows.push(row("FCRA Form FC-4", dmy(DUE.fc4)));
            if (on("g80")) rows.push(row("Form 10BD and 10BE", dmy(DUE.f10bd)));
            rows.push(row("ITR-7 due date", audit ? dmy(DUE.itr) : "General due date", true));
            document.getElementById("nc-out").innerHTML = rows.join("");
            document.getElementById("nc-note").textContent = on("fcra")
              ? "FCRA-registered NGOs file Form 10B whatever their income, and FC-4 even in a year with no foreign contribution."
              : "Audit applies when income before exemption exceeds the basic exemption limit. Form 10 and 9A are filed before the ITR.";
          };
          nc.addEventListener("input", function () {
            trackUse("trust_compliance_checker");
            renderCheck();
          });
          nc.addEventListener("change", renderCheck);
          renderCheck();
        }
      })();
    </script>
