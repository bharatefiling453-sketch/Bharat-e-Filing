    <script>
      /* GSTR-10: live final return clock, due date and late fee calculator, closing stock tax calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var LATE_PER_DAY = 100, LATE_CAP = 5000; /* each under CGST and SGST, Section 47 */
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function addMonths(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth() + n, 1);
          var last = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
          d.setDate(Math.min(from.getDate(), last));
          return d;
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
          window.dataLayer.push({ event: "calculator_use", service: "gstr-10-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live clock (Section 45: 3 months; Section 47: cap after 50 days; Section 46: 15 days after GSTR-3A) ---- */
        function tick() {
          var now = new Date();
          var by = addMonths(now, 3);
          var end = new Date(by.getFullYear(), by.getMonth(), by.getDate(), 23, 59, 59);
          setText("[data-g10-by]", dmy(by));
          setText("[data-due-today]", dmy(addMonths(now, -3)));
          setText("[data-cap-on]", dmy(addDays(now, LATE_CAP / LATE_PER_DAY)));
          setText("[data-notice-by]", dmy(addDays(now, 15)));
          var ms = end - now;
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='g10']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file GSTR-10 for a registration cancelled today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Due date and late fee calculator ---- */
        var gf = document.getElementById("g10-fee");
        if (gf) {
          var cancelIn = gf.querySelector("[name='cancel']"), orderIn = gf.querySelector("[name='order']"), filedIn = gf.querySelector("[name='filed']");
          var today = new Date();
          cancelIn.value = isoDate(addMonths(today, -4));
          orderIn.value = isoDate(addMonths(today, -4));
          filedIn.value = isoDate(today);
          var renderFee = function () {
            var c = parse(cancelIn.value), o = parse(orderIn.value), f = parse(filedIn.value);
            if (!c || !o || !f) return;
            var due = addMonths(c > o ? c : o, 3);
            var late = Math.max(0, Math.round((f - due) / 86400000));
            var each = Math.min(late * LATE_PER_DAY, LATE_CAP);
            var v = document.getElementById("gf-verdict");
            v.textContent = late ? "Late by " + late + " day" + (late === 1 ? "" : "s") + "." : "On time. No late fee.";
            v.className = "result__verdict " + (late ? "is-yes" : "is-no");
            document.getElementById("gf-out").innerHTML = [
              row("GSTR-10 due by", dmy(due)),
              row("Late fee (CGST)", inr(each)),
              row("Late fee (SGST)", inr(each)),
              row("Total late fee", inr(each * 2), true),
            ].join("");
          };
          gf.addEventListener("input", function () {
            trackUse("gstr10_late_fee");
            renderFee();
          });
          gf.addEventListener("change", renderFee);
          renderFee();
        }

        /* ---- Closing stock tax calculator (Section 29(5); capital goods reduced 5 percentage points per quarter or part) ---- */
        var gs = document.getElementById("g10-stock");
        if (gs) {
          var num = function (n) {
            return Math.max(0, Number(gs.querySelector("[name='" + n + "']").value) || 0);
          };
          var cgDate = gs.querySelector("[name='cgdate']");
          cgDate.value = isoDate(addMonths(new Date(), -21));
          var renderStock = function () {
            var stock = Math.max(num("itc"), num("out"));
            var inv = parse(cgDate.value), now = new Date(), q = 0;
            if (inv) while (addMonths(inv, 3 * q) < now && q < 20) q++;
            var reduced = num("cg") * Math.max(0, 1 - 0.05 * q);
            var capital = Math.max(reduced, num("cgtv"));
            document.getElementById("gs-out-rows").innerHTML = [
              row("Stock: higher of credit and output tax", inr(stock)),
              row("Capital goods credit after " + q + " quarter" + (q === 1 ? "" : "s") + " (−" + Math.min(100, q * 5) + "%)", inr(reduced)),
              row("Capital goods: higher amount", inr(capital)),
              row("Tax payable in GSTR-10", inr(stock + capital), true),
            ].join("");
          };
          gs.addEventListener("input", function () {
            trackUse("gstr10_stock_tax");
            renderStock();
          });
          gs.addEventListener("change", renderStock);
          renderStock();
        }
      })();
    </script>
