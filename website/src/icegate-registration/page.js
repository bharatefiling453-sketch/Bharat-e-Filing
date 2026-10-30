    <script>
      /* ICEGATE registration: live exporter dates, ICEGATE readiness checker, IGST refund readiness checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* GSTR-1 by the 11th and GSTR-3B by the 20th of the next month for monthly filers; IEC annual update with DGFT between April and June;
           LUT furnished for each financial year before exports without IGST. IGST refund on exports: the shipping bill is the refund claim
           (CGST Rule 96) once the EGM, GSTR-1 and GSTR-3B are filed, paid to a bank account registered with Customs and validated by PFMS. */
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function nextMonthly(today, dom) {
          var d = new Date(today.getFullYear(), today.getMonth(), dom);
          return d < today ? new Date(today.getFullYear(), today.getMonth() + 1, dom) : d;
        }
        function forMonth(due) {
          var m = new Date(due.getFullYear(), due.getMonth() - 1, 1);
          return MONTHS[m.getMonth()] + " " + m.getFullYear();
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
          window.dataLayer.push({ event: "calculator_use", service: "icegate-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live exporter dates ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear();
          var g1 = nextMonthly(today, 11), g3 = nextMonthly(today, 20);
          var end = new Date(g1.getFullYear(), g1.getMonth(), g1.getDate(), 23, 59, 59);
          setText("[data-gstr1-by]", dmy(g1));
          setText("[data-gstr1-label]", "Report export invoices for " + forMonth(g1) + " in GSTR-1 within");
          setText("[data-gstr3b-by]", dmy(g3));
          setText("[data-gstr3b-label]", "GSTR-3B for " + forMonth(g3) + " is due by");
          var m = today.getMonth();
          if (m >= 3 && m <= 5) {
            setText("[data-iec-label]", "This year’s IEC update window closes on");
            setText("[data-iec-by]", dmy(new Date(y, 5, 30)));
          } else {
            setText("[data-iec-label]", "The next IEC update window opens on");
            setText("[data-iec-by]", dmy(new Date(m > 5 ? y + 1 : y, 3, 1)));
          }
          var fy = m >= 3 ? y + 1 : y;
          setText("[data-lut-label]", "Your LUT for FY " + fy + "-" + String(fy + 1).slice(2) + " should be in place before exports from");
          setText("[data-lut-by]", dmy(new Date(fy, 3, 1)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='gstr1']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next GSTR-1 due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- ICEGATE readiness checker ---- */
        var rg = document.getElementById("reg-check");
        if (rg) {
          var renderReg = function () {
            var type = rg.querySelector("[name='utype']").value;
            var items = [
              ["iec", type === "ie" ? "IEC" : "IEC or licence", "Get or update the IEC with DGFT first."],
              ["dsc", "Class 3 DSC", "Arrange a Class 3 DSC for the authorised signatory."],
              ["contact", "Contact details", "Update the email and mobile with DGFT so OTPs reach you."],
              ["pan", "PAN and GSTIN", "Keep PAN and GSTIN details ready; names must match PAN records."],
            ];
            var rows = [], missing = [];
            items.forEach(function (it) {
              var ok = rg.querySelector("[name='" + it[0] + "']").checked;
              if (!ok) missing.push(it[2]);
              rows.push(row(it[1], ok ? "Ready" : "Pending"));
            });
            rows.push(row("Ready to apply", missing.length ? "Not yet" : "Yes", true));
            var v = document.getElementById("rg-verdict");
            if (missing.length) {
              v.textContent = missing.length + (missing.length === 1 ? " item" : " items") + " to sort before applying.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Ready to register on ICEGATE.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("rg-out").innerHTML = rows.join("");
            document.getElementById("rg-note").textContent = missing.length
              ? missing[0]
              : type === "ie"
                ? "After approval, register your bank account and AD code so refunds can be credited."
                : "Your user type may need extra licence details during registration; we’ll confirm them with you.";
          };
          rg.addEventListener("change", function () {
            trackUse("icegate_ready");
            renderReg();
          });
          renderReg();
        }

        /* ---- IGST refund readiness checker ---- */
        var rf = document.getElementById("refund-check");
        if (rf) {
          var renderRef = function () {
            var steps = [
              ["sb", "Shipping bill", "File the shipping bill showing IGST paid."],
              ["egm", "Export manifest", "Ask the shipping line or airline to file the EGM."],
              ["g1", "GSTR-1 Table 6A", "Report the export invoice in GSTR-1, matching the shipping bill."],
              ["g3b", "GSTR-3B", "File GSTR-3B for the export month."],
              ["bank", "Bank and PFMS", "Register the bank account on ICEGATE and get it validated by PFMS."],
            ];
            var rows = [], first = null, done = 0;
            steps.forEach(function (s) {
              var ok = rf.querySelector("[name='" + s[0] + "']").checked;
              if (ok) done++;
              else if (!first) first = s;
              rows.push(row(s[1], ok ? "Done" : "Pending"));
            });
            rows.push(row("Steps complete", done + " of " + steps.length, true));
            var v = document.getElementById("rf-verdict");
            if (first) {
              v.textContent = "Refund on hold: " + first[1] + " pending.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "All set for the refund to be processed.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("rf-out").innerHTML = rows.join("");
            document.getElementById("rf-note").textContent = first
              ? first[2]
              : "Track the refund status on ICEGATE. If it’s still stuck, check for an invoice mismatch between GSTR-1 and the shipping bill.";
          };
          rf.addEventListener("change", function () {
            trackUse("igst_refund_ready");
            renderRef();
          });
          renderRef();
        }
      })();
    </script>
