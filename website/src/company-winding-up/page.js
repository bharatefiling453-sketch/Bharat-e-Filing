    <script>
      /* Company winding up: live closure clock, closure route finder, pending filings calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* STK-2 strike off for a company that has not carried on business for the two immediately preceding financial years, or never commenced
           within a year, after extinguishing liabilities, with a special resolution or 75% members' consent (Section 248(2)); STK-8 statement of
           accounts not more than 30 days old; AOC-4 within 30 days and MGT-7 within 60 days of the AGM (taken as 30 September), ₹100 a day each when
           late; voluntary liquidation of solvent companies under IBC Section 59; winding up by the Tribunal under Section 271. */
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
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
          window.dataLayer.push({ event: "calculator_use", service: "company-winding-up", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live closure clock ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear();
          var aoc = new Date(y, 9, 30), mgt = new Date(y, 10, 29);
          if (aoc < today) aoc = new Date(y + 1, 9, 30);
          if (mgt < today) mgt = new Date(y + 1, 10, 29);
          var next = aoc < mgt ? aoc : mgt;
          var end = new Date(next.getFullYear(), next.getMonth(), next.getDate(), 23, 59, 59);
          setText("[data-next-due]", dmy(next));
          setText("[data-next-form]", "Your company’s next ROC filing, " + (aoc < mgt ? "AOC-4" : "MGT-7") + " for " + fyLabel(next.getFullYear() - 1) + ", is due in");
          var lastAoc = new Date(y, 9, 30);
          if (lastAoc >= today) lastAoc = new Date(y - 1, 9, 30);
          setText("[data-aoc-label]", "AOC-4 for " + fyLabel(lastAoc.getFullYear() - 1) + " was due on " + dmy(lastAoc) + ". Additional fee so far");
          setText("[data-aoc-fee]", inr(daysLate(lastAoc, today) * 100));
          setText("[data-stk8-by]", dmy(addDays(today, 30)));
          var fyStart = today.getMonth() >= 3 ? y : y - 1;
          setText("[data-two-fy]", "31 Mar " + (fyStart + 3));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='roc']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next ROC filing due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Company closure route finder ---- */
        var rf = document.getElementById("route-find");
        if (rf) {
          var renderRoute = function () {
            var status = rf.querySelector("[name='status']").value;
            var assets = rf.querySelector("[name='assets']").checked, debts = rf.querySelector("[name='debts']").checked;
            var barred = rf.querySelector("[name='barred']").checked, dispute = rf.querySelector("[name='dispute']").checked;
            var route, form, time, note, warn = false;
            if (dispute) {
              route = "Winding up by the Tribunal"; form = "Petition (Section 271)"; time = "1–2 years"; warn = true;
              note = "STK-2 needs a special resolution or 75% consent. Disputes or pending cases usually go to the Tribunal.";
            } else if (debts && !assets) {
              route = "Insolvency route"; form = "IBC process"; time = "6–12 months"; warn = true;
              note = "A company that can’t pay its debts can’t use STK-2. Talk to us about the insolvency options.";
            } else if (assets || debts || barred) {
              route = "Voluntary liquidation"; form = "IBC Section 59"; time = "6–12 months";
              note = barred
                ? "Section 249 bars Section 8 companies, deposit holders and companies under inspection or prosecution from STK-2."
                : "Or settle the assets and creditors first to reach nil, then use STK-2.";
            } else if (status === "running" || status === "recent") {
              route = "Strike off, after two years"; form = "STK-2 later"; time = "After two idle financial years"; warn = true;
              note = "Stop business, keep filing on time, and apply once two full financial years have passed without business. Or consider dormant status.";
            } else {
              route = "Strike off"; form = "STK-2"; time = "4–8 months";
              note = "File pending AOC-4 and MGT-7 up to the year business stopped, and close GST and the bank account first.";
            }
            var v = document.getElementById("rf-verdict");
            v.textContent = "Best route: " + route + ".";
            v.className = "result__verdict " + (warn ? "is-yes" : "is-no");
            document.getElementById("rf-out").innerHTML = [
              row("Route", route),
              row("Form", form),
              row("Members’ approval", dispute ? "Not available" : "Special resolution"),
              row("Typical time", time, true),
            ].join("");
            document.getElementById("rf-note").textContent = note;
          };
          rf.addEventListener("change", function () {
            trackUse("company_closure_route");
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
              fee += daysLate(new Date(fy + 1, 9, 30), d) * 100;
              fee += daysLate(new Date(fy + 1, 10, 29), d) * 100;
            }
            var years = Math.max(0, stop - last);
            var v = document.getElementById("fc-verdict");
            if (!years) {
              v.textContent = "No pending years. You can move straight to closure.";
              v.className = "result__verdict is-no";
            } else {
              v.textContent = forms + " forms pending, about " + inr(fee) + " in additional fees.";
              v.className = "result__verdict " + (fee ? "is-yes" : "is-no");
            }
            document.getElementById("fc-out").innerHTML = [
              row("Pending years", String(years)),
              row("Forms to file", forms + " (AOC-4 and MGT-7)"),
              row("Additional fees so far", inr(fee), true),
            ].join("");
          };
          fc.addEventListener("input", function () {
            trackUse("company_pending_fees");
            renderFee();
          });
          fc.addEventListener("change", renderFee);
          renderFee();
        }
      })();
    </script>
