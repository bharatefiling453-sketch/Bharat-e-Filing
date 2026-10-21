    <script>
      /* Income tax e-filing: live ITR clock, ITR form finder, late filing calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26 (AY 2026-27): Section 139(4) belated / 139(5) revised; CBDT Circular 7/2026 for audit cases */
        var BELATED_BY = new Date(2026, 11, 31, 23, 59, 59);
        var DEADLINES = [
          [new Date(2026, 9, 21), "Tax audit reports are due on"],
          [new Date(2026, 10, 21), "Tax-audit cases file ITR by"],
          [new Date(2026, 10, 30), "Transfer-pricing cases file ITR by"],
          [new Date(2026, 11, 31), "Belated returns close on"],
          [new Date(2027, 2, 31), "Revised returns close on"],
        ];
        var ADVANCE = [[5, 15, "15%"], [8, 15, "45%"], [11, 15, "75%"], [2, 15, "100%"]]; /* month index, day, cumulative share */
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function isoDate(d) {
          return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
        }
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        /* Months or part of a month after the due date (Section 234A) */
        function monthsLate(due, on) {
          if (on <= due) return 0;
          var n = (on.getFullYear() - due.getFullYear()) * 12 + on.getMonth() - due.getMonth();
          return on.getDate() > due.getDate() ? n + 1 : Math.max(n, 1);
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
          window.dataLayer.push({ event: "calculator_use", service: "income-tax-e-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live ITR clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var ms = Math.max(0, BELATED_BY - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='belated']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file a belated return for FY 2025-26");
          }
          var next = DEADLINES.filter(function (d) {
            return d[0] >= today;
          })[0] || DEADLINES[DEADLINES.length - 1];
          setText("[data-next-label]", next[1]);
          setText("[data-next-date]", dmy(next[0]));
          var m = monthsLate(new Date(2026, 6, 31), today);
          setText("[data-months-late]", m + "%");
          setText("[data-months-n]", m + " month" + (m === 1 ? "" : "s"));
          for (var y = today.getFullYear(), i = 0, adv = null; !adv && i < 8; i++) {
            var a = ADVANCE[i % 4], d = new Date(y + (i >= 4 ? 1 : 0), a[0], a[1]);
            if (d >= today) adv = [d, a[2]];
          }
          if (adv) {
            setText("[data-adv-date]", dmy(adv[0]));
            setText("[data-adv-pct]", adv[1]);
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- ITR form finder (individuals) ---- */
        var fc = document.getElementById("form-check");
        if (fc) {
          var renderForm = function () {
            var src = fc.querySelector("[name='source']").value;
            var on = function (n) {
              return fc.querySelector("[name='" + n + "']").checked;
            };
            var complex = on("nri") || on("foreign") || on("director");
            var form, note = "";
            if (src === "salary") {
              form = complex || on("above50") || on("houses") ? "ITR-2" : "ITR-1";
              note = form === "ITR-1" ? "Listed equity gains under 112A up to ₹1.25 lakh can also go in ITR-1." : "ITR-1 can’t be used with these, so ITR-2 is the right form.";
            } else if (src === "cg") {
              form = "ITR-2";
              note = "Only listed equity gains up to ₹1.25 lakh with salary fit ITR-1. Anything more needs ITR-2.";
            } else if (src === "presumptive") {
              form = complex || on("above50") ? "ITR-3" : "ITR-4";
              note = form === "ITR-4" ? "For presumptive income under Sections 44AD, 44ADA or 44AE." : "ITR-4 can’t be used with these, so ITR-3 is needed.";
            } else {
              form = "ITR-3";
              note = "F&O and intraday are business income. A tax audit may apply above the turnover limits.";
            }
            var business = form === "ITR-3" || form === "ITR-4";
            var v = document.getElementById("fc-verdict");
            v.textContent = "You should file " + form + ".";
            v.className = "result__verdict is-no";
            document.getElementById("fc-out").innerHTML = [
              row("Original due date", business ? "31 Aug 2026 (21 Nov if audited)" : "31 Jul 2026"),
              row("If missed", "Belated by 31 Dec 2026"),
              row("Our plan", form === "ITR-1" ? "Free self e-file, or ₹2,499 with a CA" : form === "ITR-2" && src === "salary" ? "₹2,499 with a CA" : "From ₹3,499 with a CA", true),
            ].join("");
            document.getElementById("fc-note").textContent = note;
          };
          fc.addEventListener("change", function () {
            trackUse("itr_form_finder");
            renderForm();
          });
          renderForm();
        }

        /* ---- Late filing calculator (Section 234F fee, Section 234A interest, ITR-U additional tax) ---- */
        var lc = document.getElementById("late-check");
        if (lc) {
          var dateIn = lc.querySelector("[name='date']");
          dateIn.value = isoDate(new Date());
          var renderLate = function () {
            var due = parse(lc.querySelector("[name='due']").value), on = parse(dateIn.value);
            if (!due || !on) return;
            var income = Math.max(0, Number(lc.querySelector("[name='income']").value) || 0);
            var tax = Math.max(0, Number(lc.querySelector("[name='tax']").value) || 0);
            var v = document.getElementById("lc-verdict"), rows = [];
            var months = monthsLate(due, on), interest = tax * 0.01 * months;
            if (!months) {
              v.textContent = "On time. No late fee.";
              v.className = "result__verdict is-no";
              rows.push(row("Tax to pay before filing", inr(tax), true));
            } else {
              var fee = income <= 500000 ? 1000 : 5000;
              var updated = on > day(BELATED_BY);
              v.textContent = updated ? "Belated window closed. Only an updated return (ITR-U)." : "Belated return, late by " + months + " month" + (months === 1 ? "" : "s") + ".";
              v.className = "result__verdict is-yes";
              rows.push(row("Late fee (Section 234F)", inr(fee)));
              rows.push(row("Interest (Section 234A, " + months + "%)", inr(interest)));
              if (updated) rows.push(row("Additional tax (ITR-U, 25% to 70%)", "from " + inr((tax + interest) * 0.25)));
              rows.push(row("Total to pay with tax", inr(tax + fee + interest + (updated ? (tax + interest) * 0.25 : 0)), true));
            }
            document.getElementById("lc-out").innerHTML = rows.join("");
          };
          lc.addEventListener("input", function () {
            trackUse("itr_late_fee");
            renderLate();
          });
          lc.addEventListener("change", renderLate);
          renderLate();
        }
      })();
    </script>
