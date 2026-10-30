    <script>
      /* Professional tax: live PT calendar, PT calculator (Maharashtra, Karnataka), Maharashtra PTRC due date checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var FULL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        /* Article 276(2): professional tax capped at ₹2,500 a year per person. Maharashtra salary slabs: men nil up to ₹7,500, ₹175 for
           ₹7,501–10,000, ₹200 above ₹10,000 (₹300 in February); women nil up to ₹25,000, ₹200 above (₹300 in February). Karnataka from
           1 April 2025: nil below ₹25,000, ₹200 from ₹25,000 (₹300 in February). Maharashtra PTRC (Profession Tax (Amendment) Rules, 2026):
           employers with previous-year liability of ₹50,000 or more file monthly by the 15th of the following month; others file an annual
           return by 15 March. */
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
        function rupees(n) {
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
          window.dataLayer.push({ event: "calculator_use", service: "professional-tax-return-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live PT calendar ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear(), m = today.getMonth();
          var due = today.getDate() <= 15 ? new Date(y, m, 15) : new Date(y, m + 1, 15);
          var salaryMonth = new Date(due.getFullYear(), due.getMonth() - 1, 1);
          var end = new Date(due.getFullYear(), due.getMonth(), 15, 23, 59, 59);
          setText("[data-ptrc-by]", dmy(due));
          setText("[data-ptrc-label]", "PTRC return and payment for " + FULL[salaryMonth.getMonth()] + " salary are due in");
          var annual = new Date(y, 2, 15);
          if (annual < today) annual = new Date(y + 1, 2, 15);
          setText("[data-annual-by]", dmy(annual));
          setText("[data-annual-label]", "The annual PTRC return for FY " + (annual.getFullYear() - 1) + "-" + String(annual.getFullYear()).slice(2) + " is due by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='ptrc']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the monthly PTRC return is due in Maharashtra");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- PT calculator ---- */
        var pc = document.getElementById("pt-calc");
        if (pc) {
          var renderPt = function () {
            var state = pc.querySelector("[name='state']").value, genderSel = pc.querySelector("[name='gender']");
            var female = genderSel.value === "f", sal = Math.max(0, Number(pc.querySelector("[name='salary']").value) || 0);
            genderSel.disabled = state === "ka";
            var monthly = 0, feb = 0, note;
            if (state === "ka") {
              if (sal >= 25000) { monthly = 200; feb = 300; }
              note = "Karnataka slab from 1 April 2025: nil below ₹25,000 a month.";
            } else if (female) {
              if (sal > 25000) { monthly = 200; feb = 300; }
              note = "In Maharashtra, women pay nothing up to ₹25,000 a month.";
            } else {
              if (sal > 10000) { monthly = 200; feb = 300; }
              else if (sal > 7500) { monthly = 175; feb = 175; }
              note = "In Maharashtra, men pay nothing up to ₹7,500 a month.";
            }
            var yearly = monthly * 11 + feb;
            var v = document.getElementById("pc-verdict");
            v.textContent = yearly ? "PT of " + rupees(yearly) + " a year." : "No professional tax at this salary.";
            v.className = "result__verdict " + (yearly ? "is-yes" : "is-no");
            document.getElementById("pc-out").innerHTML = [
              row("Monthly deduction", rupees(monthly)),
              row("February deduction", rupees(feb)),
              row("Yearly total", rupees(yearly), true),
            ].join("");
            document.getElementById("pc-note").textContent = note + " The yearly total can’t exceed ₹2,500.";
          };
          pc.addEventListener("input", function () {
            trackUse("pt_calc");
            renderPt();
          });
          pc.addEventListener("change", renderPt);
          renderPt();
        }

        /* ---- Maharashtra PTRC due date checker ---- */
        var dd = document.getElementById("due-calc");
        if (dd) {
          var monthIn = dd.querySelector("[name='month']"), filedIn = dd.querySelector("[name='filed']");
          var t0 = day(new Date());
          var prev = new Date(t0.getFullYear(), t0.getMonth(), 1);
          monthIn.value = prev.getFullYear() + "-" + pad(prev.getMonth() + 1);
          filedIn.value = isoDate(t0);
          var renderDue = function () {
            var liab = Math.max(0, Number(dd.querySelector("[name='liability']").value) || 0);
            var mp = (monthIn.value || "").split("-"), filed = parse(filedIn.value);
            if (mp.length !== 2 || !filed) return;
            var sy = Number(mp[0]), sm = Number(mp[1]) - 1;
            var monthlyFiler = liab >= 50000, due;
            if (monthlyFiler) due = new Date(sy, sm + 1, 15);
            else due = new Date(sm >= 3 ? sy + 1 : sy, 2, 15);
            var late = Math.round((filed - due) / 86400000);
            var v = document.getElementById("dd-verdict");
            if (late > 0) {
              v.textContent = "Late by " + late + (late === 1 ? " day." : " days.");
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "On time, with " + -late + (late === -1 ? " day" : " days") + " to spare.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("dd-out").innerHTML = [
              row("Filing frequency", monthlyFiler ? "Monthly" : "Annual"),
              row("Return for", monthlyFiler ? MONTHS[sm] + " " + sy : "FY " + (due.getFullYear() - 1) + "-" + String(due.getFullYear()).slice(2)),
              row("Due by", dmy(due), true),
            ].join("");
            document.getElementById("dd-note").textContent = late > 0
              ? "Interest on late payment and a late return fee can apply. File and pay as soon as possible."
              : monthlyFiler
              ? "Last year’s liability was ₹50,000 or more, so you file and pay every month."
              : "Last year’s liability was below ₹50,000, so one annual return covers the year.";
          };
          dd.addEventListener("input", function () {
            trackUse("pt_due");
            renderDue();
          });
          dd.addEventListener("change", renderDue);
          renderDue();
        }
      })();
    </script>
