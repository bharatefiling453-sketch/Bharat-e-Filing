    <script>
      /* Company ITR: live company compliance clock, 115BAA vs normal tax calculator, ROC & ITR due date planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26 (AY 2026-27): Section 139(1) with CBDT Circular 7/2026; Companies Act Section 137 (AOC-4, 30 days) and 92 (MGT-7, 60 days) after an AGM on 30 Sep */
        var DUE = { itr: new Date(2026, 10, 21), tp: new Date(2026, 10, 30), belated: new Date(2026, 11, 31) };
        var AGM = new Date(2026, 8, 30);
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        var DEADLINES = [
          [addDays(AGM, 30), "AOC-4 is due on", false],
          [DUE.itr, "Company ITR-6 is due on", true],
          [addDays(AGM, 60), "MGT-7 is due on", false],
          [DUE.tp, "Transfer-pricing ITR-6 is due on", true],
          [new Date(2026, 11, 15), "Advance tax (75%) is due on", false],
          [DUE.belated, "Belated ITR-6 can be filed until", true],
        ];
        var ADVANCE = [[5, 15, "15%"], [8, 15, "45%"], [11, 15, "75%"], [2, 15, "100%"]]; /* month index, day, cumulative share */
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
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
          window.dataLayer.push({ event: "calculator_use", service: "company-itr-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        function upcoming(list, today) {
          return list.filter(function (d) {
            return d[0] >= today;
          })[0] || list[list.length - 1];
        }
        function daysLate(due, on) {
          return Math.max(0, Math.round((on - due) / 86400000));
        }

        /* ---- Live company compliance clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var next = upcoming(DEADLINES, today);
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-next-label]", next[1]);
          setText("[data-next-date]", dmy(next[0]));
          var itr = upcoming(DEADLINES.filter(function (d) {
            return d[2];
          }), today);
          setText("[data-itr-label]", itr[1].replace(/ on$/, " by"));
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
          /* ROC card: AOC-4 then MGT-7 for an AGM on 30 September; after a due date, the running fee (₹100 a day each) */
          var aoc = addDays(AGM, 30), mgt = addDays(AGM, 60);
          if (today <= aoc) {
            setText("[data-roc-label]", "AGM held on 30 September? AOC-4 is due on");
            setText("[data-roc-big]", dmy(aoc));
            setText("[data-roc-sub]", "MGT-7 follows by " + dmy(mgt) + ". After the due date, ₹100 a day for each form.");
          } else if (today <= mgt) {
            setText("[data-roc-label]", "AOC-4 still pending? Additional fee so far");
            setText("[data-roc-big]", inr(daysLate(aoc, today) * 100));
            setText("[data-roc-sub]", "MGT-7 is due by " + dmy(mgt) + ". Fees keep running at ₹100 a day for each form.");
          } else {
            setText("[data-roc-label]", "Both forms pending? Additional fee so far");
            setText("[data-roc-big]", inr((daysLate(aoc, today) + daysLate(mgt, today)) * 100));
            setText("[data-roc-sub]", "AOC-4 was due " + dmy(aoc) + " and MGT-7 " + dmy(mgt) + ", for an AGM on 30 September.");
          }
          for (var y = today.getFullYear(), i = 0, adv = null; !adv && i < 8; i++) {
            var a = ADVANCE[i % 4], d = new Date(y + (i >= 4 ? 1 : 0), a[0], a[1]);
            if (d >= today) adv = [d, a[2]];
          }
          if (adv) {
            setText("[data-adv-date]", dmy(adv[0]));
            setText("[data-adv-pct]", adv[1]);
          }
          setText("[data-10ic-by]", dmy(DUE.itr));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- 115BAA vs normal tax calculator (Sections 115BAA, 115JB; surcharge 7% / 12% normal, 10% for 115BAA; 4% cess) ---- */
        var ct = document.getElementById("co-tax");
        if (ct) {
          var val = function (n) {
            return Math.max(0, Number(ct.querySelector("[name='" + n + "']").value) || 0);
          };
          var sur = function (inc) {
            return inc > 1e8 ? 1.12 : inc > 1e7 ? 1.07 : 1;
          };
          var renderTax = function () {
            var income = val("income"), ded = Math.min(val("ded"), val("income")), book = val("book");
            var rate = ct.querySelector("[name='small']").checked ? 0.25 : 0.3;
            var normalInc = income - ded;
            var normal = normalInc * rate * sur(normalInc) * 1.04;
            var mat = book * 0.15 * sur(book) * 1.04;
            var payNormal = Math.max(normal, mat);
            var baa = income * 0.22 * 1.1 * 1.04;
            var v = document.getElementById("ct-verdict");
            var save = Math.abs(payNormal - baa);
            v.textContent = baa < payNormal ? "Section 115BAA saves about " + inr(save) + " this year." : "The normal regime saves about " + inr(save) + " this year.";
            v.className = "result__verdict " + (baa < payNormal ? "is-yes" : "is-no");
            document.getElementById("ct-out").innerHTML = [
              row("Normal tax at " + rate * 100 + "% on " + inr(normalInc), inr(normal)),
              row("MAT at 15% on book profit", inr(mat)),
              row("Payable under the normal regime", inr(payNormal) + (mat > normal ? " (MAT)" : "")),
              row("Tax under Section 115BAA", inr(baa), true),
            ].join("");
          };
          ct.addEventListener("input", function () {
            trackUse("company_115baa_calculator");
            renderTax();
          });
          ct.addEventListener("change", renderTax);
          renderTax();
        }

        /* ---- ROC & ITR due date planner (AOC-4 30 days, MGT-7 60 days, ADT-1 15 days after AGM; ₹100 a day late fee) ---- */
        var rp = document.getElementById("roc-plan");
        if (rp) {
          var renderPlan = function () {
            var agm = parse(rp.querySelector("[name='agm']").value);
            if (!agm) return;
            var tp = rp.querySelector("[name='tp']").checked, today = day(new Date());
            var aoc = addDays(agm, 30), mgt = addDays(agm, 60), adt = addDays(agm, 15);
            var lateAgm = agm > new Date(2026, 8, 30);
            var fee = (daysLate(aoc, today) + daysLate(mgt, today)) * 100;
            var v = document.getElementById("rp-verdict");
            v.textContent = lateAgm ? "AGM after 30 September needs an extension from the ROC." : fee ? "ROC forms are late: about " + inr(fee) + " in fees so far." : "All on track. Next: AOC-4 by " + dmy(aoc) + ".";
            v.className = "result__verdict " + (lateAgm || fee ? "is-yes" : "is-no");
            document.getElementById("rp-out").innerHTML = [
              row("ADT-1 (auditor)", dmy(adt)),
              row("AOC-4 (financial statements)", dmy(aoc)),
              row("MGT-7 or MGT-7A (annual return)", dmy(mgt)),
              row("ITR-6 and Form 10-IC", dmy(tp ? DUE.tp : DUE.itr), true),
            ].join("");
          };
          rp.addEventListener("input", function () {
            trackUse("company_roc_planner");
            renderPlan();
          });
          rp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
