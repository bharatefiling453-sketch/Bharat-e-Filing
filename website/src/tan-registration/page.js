    <script>
      /* TAN registration: live TDS clock, TAN need checker, TDS late fee & interest calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Quarterly TDS statements: Q1 31 Jul, Q2 31 Oct, Q3 31 Jan, Q4 31 May; deposit by the 7th (30 April for March) */
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
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
        }
        /* Working days: Monday to Friday. Public holidays are not excluded (estimate). */
        function addWorkingDays(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth(), from.getDate());
          while (n > 0) {
            d.setDate(d.getDate() + 1);
            if (d.getDay() !== 0 && d.getDay() !== 6) n--;
          }
          return d;
        }
        /* Months or part of a month between two dates (interest on late TDS deposit) */
        function monthsOrPart(from, to) {
          if (to <= from) return 0;
          var n = (to.getFullYear() - from.getFullYear()) * 12 + to.getMonth() - from.getMonth();
          return to.getDate() >= from.getDate() ? n + 1 : Math.max(n, 1);
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
          window.dataLayer.push({ event: "calculator_use", service: "tan-registration", tool: tool });
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

        /* ---- Live TDS clock ---- */
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
          setText("[data-q-label]", "Quarterly TDS statement (" + next[2] + ") is due in");
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
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file the " + next[1] + " TDS statement");
          }
          var late = Math.round((today - prev[0]) / 86400000);
          setText("[data-late-label]", prev[1] + " statement (due " + dmy(prev[0]) + ") still pending? Fee so far");
          setText("[data-late-fee]", inr(late * 200));
          var dep = today.getMonth() === 2 ? new Date(today.getFullYear(), 3, 30) : new Date(today.getFullYear(), today.getMonth() + 1, 7);
          setText("[data-dep-by]", dmy(dep));
          setText("[data-tan-by]", dmy(addWorkingDays(today, 10)));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Do I need a TAN? (Section 203A; PAN-based challans for non-audited individuals/HUFs) ---- */
        var PAN_FORMS = { property: ["Form 26QB", "Section 194-IA"], rent: ["Form 26QC", "Section 194-IB"], contract: ["Form 26QD", "Section 194M"] };
        var tc = document.getElementById("tan-check");
        if (tc) {
          var renderTan = function () {
            var who = tc.querySelector("[name='who']").value, pay = tc.querySelector("[name='pay']").value;
            var v = document.getElementById("tc-verdict"), rows = [], note = "";
            if (pay === "property") {
              v.textContent = "No TAN needed. Use your PAN in Form 26QB.";
              v.className = "result__verdict is-no";
              rows.push(row("TDS", "1% under Section 194-IA"), row("Pay with PAN in", "Form 26QB", true));
              note = "Every buyer, including companies, can pay TDS on property with PAN through Form 26QB.";
            } else if (who === "individual" && PAN_FORMS[pay]) {
              v.textContent = "No TAN needed. Use your PAN in " + PAN_FORMS[pay][0] + ".";
              v.className = "result__verdict is-no";
              rows.push(row("Provision", PAN_FORMS[pay][1]), row("Pay with PAN in", PAN_FORMS[pay][0], true));
              note = pay === "rent" ? "Applies to rent above ₹50,000 a month." : "Applies to contractor and professional payments above ₹50 lakh in the year.";
            } else {
              v.textContent = "Yes, you need a TAN before deducting TDS.";
              v.className = "result__verdict is-yes";
              rows.push(row("Apply in", "Form 49B"), row("Then deposit by", "7th of the next month"), row("Quarterly statement", pay === "salary" ? "TDS on salary" : pay === "nri" ? "TDS on non-resident payments" : "TDS on other payments", true));
              note = "Penalty for deducting without a TAN or quoting a wrong one: ₹10,000 (Section 272BB).";
            }
            document.getElementById("tc-out").innerHTML = rows.join("");
            document.getElementById("tc-note").textContent = note;
          };
          tc.addEventListener("change", function () {
            trackUse("tan_need_checker");
            renderTan();
          });
          renderTan();
        }

        /* ---- TDS late fee & interest (1.5% a month or part for late deposit; ₹200 a day late statement fee capped at TDS) ---- */
        var tl = document.getElementById("tds-late");
        if (tl) {
          var renderLate = function () {
            var amount = Math.max(0, Number(tl.querySelector("[name='amount']").value) || 0);
            var ded = parse(tl.querySelector("[name='deducted']").value), paid = parse(tl.querySelector("[name='paid']").value);
            var due = parse(tl.querySelector("[name='due']").value), filed = parse(tl.querySelector("[name='filed']").value);
            if (!ded || !paid || !due || !filed) return;
            var depDue = ded.getMonth() === 2 ? new Date(ded.getFullYear(), 3, 30) : new Date(ded.getFullYear(), ded.getMonth() + 1, 7);
            var months = paid > depDue ? monthsOrPart(ded, paid) : 0;
            var interest = amount * 0.015 * months;
            var daysLate = Math.max(0, Math.round((filed - due) / 86400000));
            var fee = Math.min(daysLate * 200, amount);
            var v = document.getElementById("tl-verdict");
            v.textContent = interest || fee ? "Extra cost: " + inr(interest + fee) + "." : "On time. No interest or late fee.";
            v.className = "result__verdict " + (interest || fee ? "is-yes" : "is-no");
            document.getElementById("tl-out").innerHTML = [
              row("Deposit was due by", dmy(depDue)),
              row("Interest (" + months + " month" + (months === 1 ? "" : "s") + " at 1.5%)", inr(interest)),
              row("Late statement fee (" + daysLate + " day" + (daysLate === 1 ? "" : "s") + ")", inr(fee)),
              row("Total to pay", inr(interest + fee), true),
            ].join("");
          };
          tl.addEventListener("input", function () {
            trackUse("tds_late_fee");
            renderLate();
          });
          tl.addEventListener("change", renderLate);
          renderLate();
        }
      })();
    </script>
