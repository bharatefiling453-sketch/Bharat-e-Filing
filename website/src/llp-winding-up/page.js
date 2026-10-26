    <script>
      /* LLP winding up: live closure clock, closure route finder, pending filings calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Form 24 strike off for an LLP without business for at least a year, nil assets and liabilities (Section 75, Rule 37); Form 11 by 30 May and
           Form 8 by 30 October, ₹100 a day each when late (Sections 34 and 35, Rule 24); restoration through the Tribunal within three years;
           voluntary liquidation of solvent LLPs under IBC Section 59; winding up by the Tribunal under Section 64. */
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
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
        }
        function daysLate(due, on) {
          return Math.max(0, Math.round((on - due) / 86400000));
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
          window.dataLayer.push({ event: "calculator_use", service: "llp-winding-up", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live closure clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var eligible = new Date(today.getFullYear() + 1, today.getMonth(), today.getDate());
          var end = new Date(eligible.getFullYear(), eligible.getMonth(), eligible.getDate(), 0, 0, 0);
          setText("[data-f24-from]", dmy(eligible));
          var lastF11 = new Date(today.getFullYear(), 4, 30);
          if (lastF11 > today) lastF11 = new Date(today.getFullYear() - 1, 4, 30);
          setText("[data-f11-label]", "Form 11 for FY " + (lastF11.getFullYear() - 1) + "-" + String(lastF11.getFullYear()).slice(2) + " was due on " + dmy(lastF11) + ". Late fee so far");
          setText("[data-f11-fee]", inr(daysLate(lastF11, today) * 100));
          var f8 = new Date(today.getFullYear(), 9, 30), f11 = new Date(today.getFullYear(), 4, 30);
          if (f8 < today) f8 = new Date(today.getFullYear() + 1, 9, 30);
          if (f11 < today) f11 = new Date(today.getFullYear() + 1, 4, 30);
          var next = f8 < f11 ? f8 : f11;
          setText("[data-next-due]", dmy(next));
          setText("[data-next-form]", (f8 < f11 ? "Form 8" : "Form 11") + " is next, and both repeat every year until closure.");
          setText("[data-restore-by]", dmy(new Date(today.getFullYear() + 3, today.getMonth(), today.getDate())));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='form24']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until an LLP that stops today can apply in Form 24");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- LLP closure route finder ---- */
        var rf = document.getElementById("route-find");
        if (rf) {
          var renderRoute = function () {
            var status = rf.querySelector("[name='status']").value;
            var assets = rf.querySelector("[name='assets']").checked, debts = rf.querySelector("[name='debts']").checked;
            var dispute = rf.querySelector("[name='dispute']").checked;
            var route, form, time, note, warn = false;
            if (dispute) {
              route = "Winding up by the Tribunal"; form = "Petition (Section 64)"; time = "6–18 months"; warn = true;
              note = "Strike off needs every partner’s consent. Disputes or pending cases usually go to the Tribunal.";
            } else if (debts && !assets) {
              route = "Insolvency route"; form = "IBC process"; time = "6–12 months"; warn = true;
              note = "An LLP that can’t pay its debts can’t use Form 24. Talk to us about the insolvency options.";
            } else if (assets || debts) {
              route = "Voluntary liquidation"; form = "IBC Section 59"; time = "6–12 months";
              note = "Or settle the assets and creditors first to reach nil, then use Form 24.";
            } else if (status === "running" || status === "recent") {
              route = "Strike off, after a year"; form = "Form 24 later"; time = "From one year of no business"; warn = true;
              note = "Stop business, keep filing on time, and apply once a full year has passed without business.";
            } else {
              route = "Strike off"; form = "Form 24"; time = "3–6 months";
              note = "File pending Form 8 and Form 11 up to the year business stopped, and close GST and the bank account first.";
            }
            var v = document.getElementById("rf-verdict");
            v.textContent = "Best route: " + route + ".";
            v.className = "result__verdict " + (warn ? "is-yes" : "is-no");
            document.getElementById("rf-out").innerHTML = [
              row("Route", route),
              row("Form", form),
              row("Partners’ consent", dispute ? "Not available" : "Needed"),
              row("Typical time", time, true),
            ].join("");
            document.getElementById("rf-note").textContent = note;
          };
          rf.addEventListener("change", function () {
            trackUse("llp_closure_route");
            renderRoute();
          });
          renderRoute();
        }

        /* ---- Pending filings calculator ---- */
        var fc = document.getElementById("fee-calc");
        if (fc) {
          var dateIn = fc.querySelector("[name='filedate']");
          dateIn.value = isoDate(new Date());
          var renderFee = function () {
            var last = Number(fc.querySelector("[name='lastfiled']").value);
            var stop = Number(fc.querySelector("[name='stopped']").value);
            var d = parse(dateIn.value);
            if (!d) return;
            var forms = 0, fee = 0;
            for (var fy = last + 1; fy <= stop; fy++) {
              forms += 2;
              fee += daysLate(new Date(fy + 1, 4, 30), d) * 100;
              fee += daysLate(new Date(fy + 1, 9, 30), d) * 100;
            }
            var years = Math.max(0, stop - last);
            var v = document.getElementById("fc-verdict");
            if (!years) {
              v.textContent = "No pending years. You can move straight to closure.";
              v.className = "result__verdict is-no";
            } else {
              v.textContent = forms + " forms pending, about " + inr(fee) + " in late fees.";
              v.className = "result__verdict " + (fee ? "is-yes" : "is-no");
            }
            document.getElementById("fc-out").innerHTML = [
              row("Pending years", String(years)),
              row("Forms to file", forms + " (Form 8 and 11)"),
              row("Late fees so far", inr(fee), true),
            ].join("");
          };
          fc.addEventListener("input", function () {
            trackUse("llp_pending_fees");
            renderFee();
          });
          fc.addEventListener("change", renderFee);
          renderFee();
        }
      })();
    </script>
