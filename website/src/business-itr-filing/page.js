    <script>
      /* Business ITR: live business tax clock, presumptive & audit checker, partner remuneration calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26 (AY 2026-27): Section 139(1) as amended; CBDT Circular 7/2026 for audit cases */
        var DUE = { nonAudit: new Date(2026, 7, 31), audit: new Date(2026, 10, 21) };
        var DEADLINES = [
          [new Date(2026, 9, 21), "Tax audit reports are due on", "Tax audit reports are due by"],
          [new Date(2026, 10, 21), "Tax-audit cases file ITR by", "Audit-case ITRs are due by"],
          [new Date(2026, 10, 30), "Transfer-pricing cases file ITR by", "Transfer-pricing ITRs are due by"],
          [new Date(2026, 11, 31), "Belated business returns close on", "Belated business ITRs close on"],
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
        /* Months or part of a month after the due date (Section 234A) */
        function monthsLate(due, on) {
          if (on <= due) return 0;
          var n = (on.getFullYear() - due.getFullYear()) * 12 + on.getMonth() - due.getMonth();
          return on.getDate() > due.getDate() ? n + 1 : Math.max(n, 1);
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
          window.dataLayer.push({ event: "calculator_use", service: "business-itr-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live business tax clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var next = DEADLINES.filter(function (d) {
            return d[0] >= today;
          })[0] || DEADLINES[DEADLINES.length - 1];
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-next-label]", next[1]);
          var itr = DEADLINES.slice(1).filter(function (d) {
            return d[0] >= today;
          })[0] || DEADLINES[DEADLINES.length - 1];
          setText("[data-itr-label]", itr[2]);
          setText("[data-itr-date]", dmy(itr[0]));
          setText("[data-next-date]", dmy(next[0]));
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
          var m = monthsLate(DUE.nonAudit, today);
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
          /* TDS deducted in a month is deposited by the 7th of the next month (30 April for March) */
          var tds = today.getMonth() === 2 ? new Date(today.getFullYear(), 3, 30) : new Date(today.getFullYear(), today.getMonth() + 1, 7);
          setText("[data-tds-by]", dmy(tds));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Presumptive & audit checker (Sections 44AB, 44AD, 44ADA) ---- */
        var ac = document.getElementById("audit-check");
        if (ac) {
          var renderAudit = function () {
            var entity = ac.querySelector("[name='entity']").value, nature = ac.querySelector("[name='nature']").value;
            var t = Math.max(0, Number(ac.querySelector("[name='turnover']").value) || 0);
            var profit = Math.max(0, Number(ac.querySelector("[name='profit']").value) || 0);
            var digital = ac.querySelector("[name='digital']").checked;
            var canPresume = entity === "proprietor" || entity === "firm";
            var limit, rate, presumptive = false, audit, note = "";
            if (nature === "business") {
              limit = digital ? 3e7 : 2e7;
              rate = digital ? 6 : 8;
              presumptive = canPresume && t <= limit;
              audit = t > (digital ? 1e8 : 1e7);
            } else {
              limit = digital ? 75e5 : 5e6;
              rate = 50;
              presumptive = entity === "proprietor" || entity === "firm" ? t <= limit : false;
              audit = t > 5e6;
            }
            if (presumptive) audit = profit < rate;
            var form = entity === "company" ? "ITR-6" : entity === "llp" ? "ITR-5" : presumptive && profit >= rate ? "ITR-4" : entity === "firm" ? "ITR-5" : "ITR-3";
            var v = document.getElementById("ac-verdict");
            v.textContent = audit ? "Tax audit applies. File " + form + "." : "No tax audit needed. File " + form + ".";
            v.className = "result__verdict " + (audit ? "is-yes" : "is-no");
            var rows = [];
            rows.push(row("Presumptive taxation", !canPresume ? "Not available for " + (entity === "llp" ? "LLPs" : "companies") : presumptive ? "Available (" + (nature === "business" ? "44AD" : "44ADA") + ")" : "Above the " + inr(limit) + " limit"));
            if (presumptive) rows.push(row("Minimum profit to declare", rate + "% · " + inr((t * rate) / 100)));
            rows.push(row("ITR due date", dmy(audit || entity === "company" ? DUE.audit : DUE.nonAudit), true));
            if (presumptive && profit < rate) note = "Declaring profit below " + rate + "% needs books and a tax audit if your income exceeds the basic exemption limit.";
            else if (presumptive && nature === "business" && digital) note = "Use 6% on receipts by bank or UPI and 8% on cash receipts.";
            else if (entity === "company") note = "Companies also need a statutory audit under the Companies Act, so they file by the audit-case date.";
            else if (audit) note = "The audit report must be filed before the return. Penalty for missing it: up to ₹1.5 lakh.";
            else note = "Keep books if you are not on presumptive taxation. An audit can still apply if you left Section 44AD in the last five years.";
            document.getElementById("ac-out").innerHTML = rows.join("");
            document.getElementById("ac-note").textContent = note;
          };
          ac.addEventListener("input", function () {
            trackUse("business_audit_checker");
            renderAudit();
          });
          ac.addEventListener("change", renderAudit);
          renderAudit();
        }

        /* ---- Partner remuneration calculator (Section 40(b)(v) as amended from FY 2024-25; Section 194T) ---- */
        var pc = document.getElementById("partner-calc");
        if (pc) {
          var renderPartner = function () {
            var bp = Number(pc.querySelector("[name='bookprofit']").value) || 0;
            var paid = Math.max(0, Number(pc.querySelector("[name='paid']").value) || 0);
            var allowed = bp <= 6e5 ? Math.max(3e5, 0.9 * Math.max(bp, 0)) : Math.max(3e5, 0.9 * 6e5) + 0.6 * (bp - 6e5);
            var excess = Math.max(0, paid - allowed);
            var v = document.getElementById("pc-verdict");
            v.textContent = excess ? "Above the limit by " + inr(excess) + "." : "Within the Section 40(b) limit.";
            v.className = "result__verdict " + (excess ? "is-yes" : "is-no");
            document.getElementById("pc-out").innerHTML = [
              row("Maximum deductible remuneration", inr(allowed)),
              row("Disallowed (added back to firm income)", inr(excess)),
              row("TDS at 10% under Section 194T", inr(paid * 0.1), true),
            ].join("");
          };
          pc.addEventListener("input", function () {
            trackUse("partner_remuneration");
            renderPartner();
          });
          pc.addEventListener("change", renderPartner);
          renderPartner();
        }
      })();
    </script>
