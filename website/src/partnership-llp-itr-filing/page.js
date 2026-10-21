    <script>
      /* Firm & LLP ITR: live firm/LLP clock, firm tax calculator, compliance & due date checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26 (AY 2026-27): Section 139(1) as amended; CBDT Circular 7/2026 for audit cases; LLP Act Sections 34 and 35 */
        var DUE = { nonAudit: new Date(2026, 7, 31), audit: new Date(2026, 10, 21), form8: new Date(2026, 9, 30), form11: new Date(2027, 4, 30) };
        var DEADLINES = [
          [new Date(2026, 9, 21), "Tax audit reports are due on", false],
          [DUE.form8, "LLP Form 8 is due on", false],
          [DUE.audit, "Audit-case ITR-5 is due on", true],
          [new Date(2026, 10, 30), "Transfer-pricing ITR-5 is due on", true],
          [new Date(2026, 11, 31), "Belated ITR-5 can be filed until", true],
          [DUE.form11, "LLP Form 11 is due on", false],
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
          window.dataLayer.push({ event: "calculator_use", service: "partnership-llp-itr-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        function upcoming(list, today) {
          return list.filter(function (d) {
            return d[0] >= today;
          })[0] || list[list.length - 1];
        }

        /* ---- Live firm & LLP clock ---- */
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
          /* LLP Form 8: before the due date show the date, after it the running additional fee (₹100 a day, no cap) */
          var late = Math.round((today - DUE.form8) / 86400000);
          if (late > 0) {
            setText("[data-form8-label]", "Not filed yet? Additional fee so far for " + late + " day" + (late === 1 ? "" : "s"));
            setText("[data-form8-big]", inr(late * 100));
          } else {
            setText("[data-form8-label]", "Statement of account and solvency is due on");
            setText("[data-form8-big]", dmy(DUE.form8));
          }
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

        /* ---- Firm & LLP tax calculator (Section 40(b) as amended from FY 2024-25; 30% + 12% surcharge above ₹1 crore + 4% cess) ---- */
        var ft = document.getElementById("firm-tax");
        if (ft) {
          var val = function (n) {
            return Number(ft.querySelector("[name='" + n + "']").value) || 0;
          };
          var renderTax = function () {
            var profit = val("profit"), capital = Math.max(0, val("capital")), rate = Math.max(0, val("rate")), paid = Math.max(0, val("paid"));
            var interest = (capital * Math.min(rate, 12)) / 100;
            var bp = profit - interest;
            var limit = bp <= 6e5 ? Math.max(3e5, 0.9 * Math.max(bp, 0)) : 5.4e5 + 0.6 * (bp - 6e5);
            var allowed = Math.min(paid, limit);
            var taxable = Math.max(0, bp - allowed);
            var tax = taxable * 0.3 * (taxable > 1e7 ? 1.12 : 1) * 1.04;
            var v = document.getElementById("ft-verdict");
            v.textContent = paid > limit ? "Remuneration is " + inr(paid - limit) + " over the limit." : "Remuneration is within the Section 40(b) limit.";
            v.className = "result__verdict " + (paid > limit ? "is-yes" : "is-no");
            document.getElementById("ft-out").innerHTML = [
              row("Interest allowed (up to 12%)", inr(interest)),
              row("Book profit", inr(bp)),
              row("Remuneration limit", inr(limit)),
              row("Remuneration allowed", inr(allowed)),
              row("Taxable income of the firm", inr(taxable)),
              row("Partner TDS at 10% (Section 194T)", inr((interest + paid) * 0.1)),
              row("Firm’s tax with cess", inr(tax), true),
            ].join("");
          };
          ft.addEventListener("input", function () {
            trackUse("firm_tax_calculator");
            renderTax();
          });
          ft.addEventListener("change", renderTax);
          renderTax();
        }

        /* ---- Compliance & due date checker (Section 44AB, 44AD; LLP Act Section 34 with Rule 24) ---- */
        var lc = document.getElementById("llp-check");
        if (lc) {
          var renderCheck = function () {
            var llp = lc.querySelector("[name='entity']").value === "llp";
            var t = Math.max(0, Number(lc.querySelector("[name='turnover']").value) || 0);
            var c = Math.max(0, Number(lc.querySelector("[name='contribution']").value) || 0);
            var digital = lc.querySelector("[name='digital']").checked;
            var taxAudit = t > (digital ? 1e8 : 1e7);
            var llpAudit = llp && (t > 4e6 || c > 2.5e6);
            var presumptive = !llp && t <= (digital ? 3e7 : 2e7);
            var v = document.getElementById("lc-verdict");
            v.textContent = taxAudit ? "Tax audit applies. File ITR-5 by " + dmy(DUE.audit) + "." : "No tax audit. File " + (presumptive ? "ITR-4 or ITR-5" : "ITR-5") + " by " + dmy(DUE.nonAudit) + ".";
            v.className = "result__verdict " + (taxAudit ? "is-yes" : "is-no");
            var rows = [row("Tax audit (Section 44AB)", taxAudit ? "Required" : "Not required")];
            if (llp) {
              rows.push(row("Statutory audit (LLP Act)", llpAudit ? "Required" : "Not required"));
              rows.push(row("Form 8 · next Form 11", dmy(DUE.form8) + " · " + dmy(DUE.form11)));
            } else {
              rows.push(row("Presumptive (Section 44AD)", presumptive ? "Available, ITR-4" : "Above the limit"));
            }
            rows.push(row("ITR due date", dmy(taxAudit ? DUE.audit : DUE.nonAudit), true));
            document.getElementById("lc-out").innerHTML = rows.join("");
            document.getElementById("lc-note").textContent = llp
              ? llpAudit
                ? "Form 8 must be certified by the LLP’s auditor. LLPs cannot use presumptive taxation."
                : "Form 8 is signed by two designated partners. LLPs cannot use presumptive taxation."
              : "A firm on Section 44AD declares at least 8% of turnover, or 6% on digital receipts.";
          };
          lc.addEventListener("input", function () {
            trackUse("firm_llp_compliance");
            renderCheck();
          });
          lc.addEventListener("change", renderCheck);
          renderCheck();
        }
      })();
    </script>
