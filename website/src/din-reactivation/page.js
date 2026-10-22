    <script>
      /* DIN reactivation: live reactivation clock, DIN fix finder, disqualification period calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Rule 12A as amended by G.S.R. 943(E): KYC once every three years by 30 June (earlier reading for 2025 filers: 30 Jun 2028); ₹5,000 flat late fee.
           Section 164(2): five years from the date of the company's failure. */
        var NEXT_KYC = new Date(2028, 5, 30, 23, 59, 59);
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function addYears(from, n) {
          return new Date(from.getFullYear() + n, from.getMonth(), from.getDate());
        }
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
          window.dataLayer.push({ event: "calculator_use", service: "din-reactivation", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live DIN reactivation clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          setText("[data-file-by]", dmy(addDays(today, 1)));
          setText("[data-disq-by]", dmy(addYears(today, 5)));
          var ms = Math.max(0, NEXT_KYC - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='kyc']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next routine KYC due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- DIN fix finder ---- */
        var fx = document.getElementById("fix-finder");
        if (fx) {
          var FIX = {
            kyc: ["One filing fixes this: KYC with the late fee.", "DIR-3 KYC Web", "₹5,000 flat", "1–3 days", false],
            disq: ["KYC won’t lift a 164(2) disqualification.", "Review of options", "Not applicable", "Five years, or legal route", true],
            gone: ["A surrendered DIN isn’t reactivated.", "Fresh DIN when appointed", "Not applicable", "With the appointment", true],
            unsure: ["Let’s read your DIN status first.", "Free status check", "Depends on status", "Same day", false],
          };
          var renderFix = function () {
            var st = fx.querySelector("[name='status']").value;
            var dsc = fx.querySelector("[name='dsc']").checked, link = fx.querySelector("[name='panlink']").checked;
            var f = FIX[st];
            var v = document.getElementById("fx-verdict");
            v.textContent = f[0];
            v.className = "result__verdict " + (f[4] ? "is-yes" : "is-no");
            var before = [];
            if (!dsc) before.push("new DSC");
            if (!link) before.push("PAN–Aadhaar link");
            document.getElementById("fx-out").innerHTML = [
              row("Route", f[1]),
              row("Late fee", f[2]),
              row("Do first", st === "kyc" && before.length ? before.join(", ") : "Nothing"),
              row("Typical time", f[3], true),
            ].join("");
            document.getElementById("fx-note").textContent =
              st === "kyc"
                ? before.length
                  ? "Fix these first, or the KYC will fail. Our Reactivation + DSC plan covers a new DSC."
                  : "You’re ready. Share the OTPs on a short call and we file within 24 hours."
                : st === "disq"
                ? "Options depend on the facts: pending filings, Tribunal revival under Section 252, or correcting a wrong marking."
                : st === "gone"
                ? "Under Rule 11, a surrendered or cancelled DIN stays closed. A fresh DIN is applied for with the next appointment."
                : "Send your DIN and we confirm the status and the right fix before you pay any late fee.";
          };
          fx.addEventListener("change", function () {
            trackUse("din_fix_finder");
            renderFix();
          });
          renderFix();
        }

        /* ---- Disqualification period calculator (Section 164(2): five years) ---- */
        var dq = document.getElementById("disq-calc");
        if (dq) {
          var dateIn = dq.querySelector("[name='defaultdate']");
          var renderDisq = function () {
            var d = parse(dateIn.value);
            if (!d) return;
            var cause = dq.querySelector("[name='cause']").value;
            var ends = addYears(d, 5), today = day(new Date());
            var left = Math.round((ends - today) / 86400000);
            var v = document.getElementById("dq-verdict");
            v.textContent = left > 0 ? "Disqualified until " + dmy(ends) + "." : "The five-year period ended on " + dmy(ends) + ".";
            v.className = "result__verdict " + (left > 0 ? "is-yes" : "is-no");
            document.getElementById("dq-out").innerHTML = [
              row("Cause", cause === "returns" ? "Returns not filed" : "Repayment default"),
              row("Days remaining", left > 0 ? left.toLocaleString("en-IN") : "0"),
              row("Eligible again from", dmy(addDays(ends, 1)), true),
            ].join("");
          };
          dq.addEventListener("input", function () {
            trackUse("din_disqualification_period");
            renderDisq();
          });
          dq.addEventListener("change", renderDisq);
          renderDisq();
        }
      })();
    </script>
