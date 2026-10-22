    <script>
      /* TDS return filing: live TDS return clock, due date & late fee planner, TDS rate & threshold finder (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* TDS returns: Q1 31 Jul, Q2 31 Oct, Q3 31 Jan, Q4 31 May; TCS 15th of the month after the quarter; Form 16A 15 days after the TDS due date */
        var QUARTERS = [[6, 31, "Q1", "Apr–Jun"], [9, 31, "Q2", "Jul–Sep"], [0, 31, "Q3", "Oct–Dec"], [4, 31, "Q4", "Jan–Mar"]];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function isoDate(d) {
          return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
        }
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
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
          window.dataLayer.push({ event: "calculator_use", service: "tds-return-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        function quarterDates(today) {
          var y = today.getFullYear(), list = [];
          for (var k = -1; k <= 1; k++) {
            QUARTERS.forEach(function (q) {
              list.push([new Date(y + k, q[0], q[1]), q[2], q[3]]);
            });
          }
          return list.sort(function (a, b) {
            return a[0] - b[0];
          });
        }

        /* ---- Live TDS return clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var list = quarterDates(today);
          var next = list.filter(function (q) {
            return q[0] >= today;
          })[0];
          var prev = list.filter(function (q) {
            return q[0] < today;
          }).pop();
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-q-label]", "TDS return (" + next[2] + ") is due in");
          setText("[data-hero-label]", "The " + next[1] + " TDS return is due by");
          setText("[data-q-date]", dmy(next[0]));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='next']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file the " + next[1] + " TDS return");
          }
          /* Form 16A: 15 days after the TDS return due date, for the most recent quarter whose certificate date is still ahead */
          var cert = list.map(function (q) {
            return [addDays(q[0], 15), q[2]];
          }).filter(function (c) {
            return c[0] >= today;
          })[0];
          setText("[data-cert-label]", "Certificates for " + cert[1] + " must reach payees by");
          setText("[data-cert-by]", dmy(cert[0]));
          var late = Math.round((today - prev[0]) / 86400000);
          setText("[data-late-label]", prev[1] + " return (due " + dmy(prev[0]) + ") still pending? Fee so far");
          setText("[data-late-fee]", inr(late * 200));
          var dep = today.getMonth() === 2 ? new Date(today.getFullYear(), 3, 30) : new Date(today.getFullYear(), today.getMonth() + 1, 7);
          setText("[data-dep-by]", dmy(dep));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Due date & late fee planner (FY 2026-27; ₹200 a day capped at TDS; Section 271H after one year) ---- */
        var TDS_DUE = { 1: new Date(2026, 6, 31), 2: new Date(2026, 9, 31), 3: new Date(2027, 0, 31), 4: new Date(2027, 4, 31) };
        var TCS_DUE = { 1: new Date(2026, 6, 15), 2: new Date(2026, 9, 15), 3: new Date(2027, 0, 15), 4: new Date(2027, 4, 15) };
        var tp = document.getElementById("tds-plan");
        if (tp) {
          var filedIn = tp.querySelector("[name='filed']");
          filedIn.value = isoDate(new Date());
          var renderPlan = function () {
            var tcs = tp.querySelector("[name='form']").value === "tcs", q = tp.querySelector("[name='q']").value;
            var amount = Math.max(0, Number(tp.querySelector("[name='amount']").value) || 0), filed = parse(filedIn.value);
            if (!filed) return;
            var due = (tcs ? TCS_DUE : TDS_DUE)[q];
            var cert = addDays(due, 15);
            var daysLate = Math.max(0, Math.round((filed - due) / 86400000));
            var fee = Math.min(daysLate * 200, amount);
            var overYear = filed > new Date(due.getFullYear() + 1, due.getMonth(), due.getDate());
            var v = document.getElementById("tp-verdict");
            v.textContent = daysLate ? "Late by " + daysLate + " day" + (daysLate === 1 ? "" : "s") + ": fee " + inr(fee) + "." : "On time. No late fee.";
            v.className = "result__verdict " + (daysLate ? "is-yes" : "is-no");
            document.getElementById("tp-out").innerHTML = [
              row("Return due by", dmy(due)),
              row(tcs ? "Form 27D by" : "Form 16A by", dmy(cert) + (q === "4" && !tcs ? " (Form 16 by 15 Jun 2027)" : "")),
              row("Late fee (Section 234E)", inr(fee) + (daysLate * 200 > amount ? " (capped)" : "")),
              row("Penalty risk (Section 271H)", overYear ? "₹10,000 to ₹1 lakh" : "None if paid and filed in a year", true),
            ].join("");
            document.getElementById("tp-note").textContent = tcs
              ? "TCS returns in Form 27EQ are due 15 days after the quarter ends."
              : "Pay the late fee and any interest before filing, or TRACES will raise a default.";
          };
          tp.addEventListener("input", function () {
            trackUse("tds_due_date_planner");
            renderPlan();
          });
          tp.addEventListener("change", renderPlan);
          renderPlan();
        }

        /* ---- TDS rate & threshold finder (rates and thresholds from 1 April 2025; Section 206AA without PAN) ---- */
        var RATES = {
          contract: { sec: "194C", single: 30000, year: 100000, rate: function (ind) { return ind ? 1 : 2; } },
          prof: { sec: "194J", year: 50000, rate: function () { return 10; } },
          tech: { sec: "194J", year: 50000, rate: function () { return 2; } },
          rent: { sec: "194-I", month: 50000, rate: function () { return 10; } },
          commission: { sec: "194H", year: 20000, rate: function () { return 2; } },
          interest: { sec: "194A", year: 10000, rate: function () { return 10; } },
        };
        var tr = document.getElementById("tds-rate");
        if (tr) {
          var renderRate = function () {
            var r = RATES[tr.querySelector("[name='pay']").value];
            var amount = Math.max(0, Number(tr.querySelector("[name='payment']").value) || 0);
            var year = Math.max(amount, Number(tr.querySelector("[name='year']").value) || 0);
            var pan = tr.querySelector("[name='pan']").checked, ind = tr.querySelector("[name='indiv']").checked;
            var applies, limit;
            if (r.month) {
              applies = amount > r.month;
              limit = "₹50,000 a month";
            } else if (r.single) {
              applies = amount > r.single || year > r.year;
              limit = "₹30,000 a payment or ₹1 lakh a year";
            } else {
              applies = year > r.year;
              limit = inr(r.year) + " a year";
            }
            var base = r.rate(ind), rate = pan ? base : Math.max(20, base * 2);
            var v = document.getElementById("tr-verdict");
            v.textContent = applies ? "Deduct TDS at " + rate + "% under Section " + r.sec + "." : "Below the threshold. No TDS yet.";
            v.className = "result__verdict " + (applies ? "is-yes" : "is-no");
            document.getElementById("tr-out").innerHTML = [
              row("Threshold", limit),
              row("Rate", base + "%" + (pan ? "" : " → " + rate + "% without PAN")),
              row("TDS on this payment", applies ? inr((amount * rate) / 100) : "₹0", true),
            ].join("");
            document.getElementById("tr-note").textContent = !pan
              ? "Section 206AA: the higher of 20% or twice the rate applies when no valid PAN is given."
              : r.sec === "194C"
                ? "1% for individual or HUF contractors, 2% for others."
                : "Once the yearly threshold is crossed, TDS applies to the whole amount paid in the year.";
          };
          tr.addEventListener("input", function () {
            trackUse("tds_rate_finder");
            renderRate();
          });
          tr.addEventListener("change", renderRate);
          renderRate();
        }
      })();
    </script>
