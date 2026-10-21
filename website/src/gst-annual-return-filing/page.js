    <script>
      /* GSTR-9: live year-end clock, applicability checker, late fee calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function rupees(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
        }
        function fyLabel(y) {
          return "FY " + y + "-" + String(y + 1).slice(2);
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
          window.dataLayer.push({ event: "calculator_use", service: "gst-annual-return-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        /* Late fee per day and cap under Notification 7/2023-CT and Section 47(2) */
        function feeRule(aato, stateTo) {
          if (aato <= 5) return { perDay: 50, cap: stateTo * 1e7 * 0.0004 };
          if (aato <= 20) return { perDay: 100, cap: stateTo * 1e7 * 0.0004 };
          return { perDay: 200, cap: stateTo * 1e7 * 0.005 };
        }

        /* ---- Live year-end clock ---- */
        function tick() {
          var now = new Date();
          /* The GSTR-9 being prepared now: due 31 Dec of this calendar year for the FY that ended last March */
          var dueYear = now.getFullYear();
          var due = new Date(dueYear, 11, 31, 23, 59, 59);
          if (now > due) {
            dueYear++;
            due = new Date(dueYear, 11, 31, 23, 59, 59);
          }
          var fyStartYear = dueYear - 1;
          var opened = new Date(fyStartYear + 1, 3, 1);
          setText("[data-g9-fy]", fyLabel(fyStartYear));
          setText("[data-g9-due]", dmy(due));
          var ms = due - now;
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          setText("[data-g9-days]", parts[0] + " days");
          var box = document.querySelector("[data-cd='g9']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days left to file GSTR-9 for " + fyLabel(fyStartYear));
          }
          var gb = document.querySelector("[data-g9-bar]");
          if (gb) gb.style.width = Math.min(100, Math.max(0, ((now - opened) / (due - opened)) * 100)) + "%";
          /* Section 16(4): ITC for the year can be claimed up to 30 November after the year */
          var itc = new Date(dueYear, 10, 30, 23, 59, 59);
          setText("[data-itc-by]", dmy(itc));
          var left = Math.ceil((itc - now) / 86400000);
          setText("[data-itc-days]", left > 0 ? left + " days left" : "Deadline passed");
          /* Late fee meter: previous year's GSTR-9, ₹3 crore turnover in one state */
          var prevDue = new Date(dueYear - 1, 11, 31, 23, 59, 59);
          setText("[data-prev-fy]", fyLabel(fyStartYear - 1));
          var days = Math.max(0, Math.ceil((now - prevDue) / 86400000));
          var rule = feeRule(3, 3);
          var fee = Math.min(days * rule.perDay, rule.cap);
          setText("[data-late-fee]", rupees(fee));
          var lb = document.querySelector("[data-late-bar]");
          if (lb) lb.style.width = (fee / rule.cap) * 100 + "%";
          /* Section 44(2): no annual return after 3 years from its due date */
          var oldDue = new Date(dueYear - 3, 11, 31, 23, 59, 59);
          var oldBy = new Date(dueYear, 11, 31);
          setText("[data-old-fy]", fyLabel(fyStartYear - 3));
          setText("[data-old-by]", dmy(oldBy));
          var ob = document.querySelector("[data-old-bar]");
          if (ob) ob.style.width = Math.min(100, ((now - oldDue) / (oldBy - oldDue)) * 100) + "%";
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Applicability checker ---- */
        var gc = document.getElementById("g9-check");
        if (gc) {
          var renderCheck = function () {
            var type = gc.querySelector("[name='ttype']:checked").value;
            var to = Math.max(0, Number(gc.querySelector("[name='turnover']").value) || 0);
            var v = document.getElementById("gc-verdict"), rows = [], note = "", need = true;
            if (type === "composition") {
              v.textContent = "File GSTR-4, not GSTR-9.";
              rows.push(row("Annual return", "GSTR-4, due 30 June", true));
              note = "Composition taxpayers report the year in GSTR-4.";
            } else if (type === "other") {
              need = false;
              v.textContent = "GSTR-9 does not apply to you.";
              rows.push(row("Why", "ISD, TDS/TCS, casual and non-resident persons are excluded", true));
              note = "You still file the returns specific to your registration type.";
            } else if (to <= 2) {
              need = false;
              v.textContent = "Optional for you.";
              rows.push(row("GSTR-9", "Optional (turnover up to ₹2 crore)"));
              rows.push(row("GSTR-9C", "Not required", true));
              note = "Filing voluntarily gives you one clean record of the year, which helps if a notice ever comes.";
            } else if (to <= 5) {
              v.textContent = "Yes, GSTR-9 is mandatory.";
              rows.push(row("GSTR-9", "Mandatory"));
              rows.push(row("GSTR-9C", "Not required", true));
              note = "Reconcile GSTR-1, GSTR-3B and GSTR-2B for all 12 months before filing.";
            } else {
              v.textContent = "Yes, GSTR-9 and GSTR-9C.";
              rows.push(row("GSTR-9", "Mandatory"));
              rows.push(row("GSTR-9C", "Mandatory, self-certified", true));
              note = "The annual return is complete only when GSTR-9C is filed too (Circular 246/03/2025-GST).";
            }
            v.className = "result__verdict " + (need ? "is-yes" : "is-no");
            document.getElementById("gc-out").innerHTML = rows.join("");
            document.getElementById("gc-note").textContent = note;
          };
          gc.addEventListener("input", function () {
            trackUse("gstr9_applicability_checker");
            renderCheck();
          });
          gc.addEventListener("change", renderCheck);
          renderCheck();
        }

        /* ---- Late fee calculator ---- */
        var lf = document.getElementById("g9-fee");
        if (lf) {
          var dateIn = lf.querySelector("[name='date']");
          var t = new Date();
          dateIn.value = t.getFullYear() + "-" + pad(t.getMonth() + 1) + "-" + pad(t.getDate());
          var renderFee = function () {
            var fy = Number(lf.querySelector("[name='fy']").value);
            var due = new Date(fy + 1, 11, 31);
            var p = (dateIn.value || "").split("-");
            if (p.length < 3) return;
            var filed = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
            var days = Math.max(0, Math.round((filed - due) / 86400000));
            var aato = Math.max(0, Number(lf.querySelector("[name='aato']").value) || 0);
            var st = Math.max(0, Number(lf.querySelector("[name='state']").value) || 0);
            var rule = feeRule(aato, st);
            var fee = Math.min(days * rule.perDay, rule.cap);
            var barred = filed > new Date(fy + 4, 11, 31);
            document.getElementById("lf-out").innerHTML = [
              row("Due date", dmy(due)),
              row("Days late", days.toLocaleString("en-IN")),
              row("Fee per day (CGST + SGST)", rupees(rule.perDay)),
              row("Maximum for this state", rupees(rule.cap)),
              row(barred ? "Filing barred (Section 44(2))" : "Late fee" + (fee === rule.cap && days > 0 ? " (capped)" : ""), barred ? "After " + dmy(new Date(fy + 4, 11, 31)) : rupees(fee), true),
            ].join("");
          };
          lf.addEventListener("input", function () {
            trackUse("gstr9_late_fee_calculator");
            renderFee();
          });
          lf.addEventListener("change", renderFee);
          renderFee();
        }
      })();
    </script>
