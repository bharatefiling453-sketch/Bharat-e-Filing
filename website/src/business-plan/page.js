    <script>
      /* Business plan: live planning snapshot, loan EMI and DSCR calculator, break-even calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Financial year runs 1 April to 31 March. EMI = P·r·(1+r)^n / ((1+r)^n − 1) with monthly rate r and n months.
           DSCR = cash available for debt service (profit after tax + depreciation + interest) / (principal + interest) for the year.
           Break-even units = fixed costs / (price − variable cost per unit). Bank norms for DSCR vary; 1.25 is a common benchmark. */
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function lakh(n) {
          return "₹" + (Math.round(n * 100) / 100).toLocaleString("en-IN") + " lakh";
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
          window.dataLayer.push({ event: "calculator_use", service: "business-plan", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live planning snapshot ---- */
        function tick() {
          var now = new Date();
          var y = now.getMonth() >= 3 ? now.getFullYear() + 1 : now.getFullYear();
          var start = new Date(y, 3, 1);
          setText("[data-fy-start]", dmy(start));
          setText("[data-fy-next]", "FY " + y + "-" + String(y + 1).slice(2));
          setText("[data-fy-label]", "Year one of your projections, FY " + y + "-" + String(y + 1).slice(2) + ", starts in");
          var ms = Math.max(0, start - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='fy']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next financial year starts");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Loan EMI and DSCR calculator ---- */
        var dc = document.getElementById("dscr-calc");
        if (dc) {
          var num = function (n) {
            return Math.max(0, Number(dc.querySelector("[name='" + n + "']").value) || 0);
          };
          var renderDscr = function () {
            var p = num("loan"), rate = num("rate"), yrs = Math.max(1, Math.round(num("years"))), cash = num("cash");
            var n = yrs * 12, r = rate / 1200;
            var emi = p <= 0 ? 0 : r === 0 ? p / n : (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
            var yearly = emi * 12, totalInt = emi * n - p;
            var dscr = yearly > 0 ? cash / yearly : 0;
            var v = document.getElementById("dc-verdict");
            if (p <= 0) {
              v.textContent = "Enter a loan amount.";
              v.className = "result__verdict is-no";
            } else if (dscr >= 1.25) {
              v.textContent = "DSCR of " + dscr.toFixed(2) + ": comfortable for most banks.";
              v.className = "result__verdict is-no";
            } else if (dscr >= 1) {
              v.textContent = "DSCR of " + dscr.toFixed(2) + ": covered, but tight.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "DSCR of " + dscr.toFixed(2) + ": repayments not covered.";
              v.className = "result__verdict is-yes";
            }
            document.getElementById("dc-out").innerHTML = [
              row("Monthly EMI", rupees(emi * 100000)),
              row("Yearly repayment", lakh(yearly)),
              row("Total interest", lakh(totalInt)),
              row("DSCR", p > 0 ? dscr.toFixed(2) : "—", true),
            ].join("");
            document.getElementById("dc-note").textContent =
              dscr < 1.25 && p > 0
                ? "Try a longer tenure, a smaller loan or more own money, or review your costs. Banks also look at security and credit history."
                : "This uses the first year’s figures; a plan shows DSCR for every year of the loan. Bank norms vary.";
          };
          dc.addEventListener("input", function () {
            trackUse("bp_dscr");
            renderDscr();
          });
          dc.addEventListener("change", renderDscr);
          renderDscr();
        }

        /* ---- Break-even calculator ---- */
        var be = document.getElementById("bep-calc");
        if (be) {
          var bnum = function (n) {
            return Math.max(0, Number(be.querySelector("[name='" + n + "']").value) || 0);
          };
          var renderBe = function () {
            var fixed = bnum("fixed"), price = bnum("price"), vc = bnum("varcost"), units = bnum("units");
            var margin = price - vc;
            var v = document.getElementById("be-verdict");
            if (margin <= 0) {
              v.textContent = "Price must be above the variable cost.";
              v.className = "result__verdict is-yes";
              document.getElementById("be-out").innerHTML = row("Margin per unit", rupees(margin), true);
              document.getElementById("be-note").textContent = "Each sale loses money, so there is no break-even point. Revisit the price or costs.";
              return;
            }
            var bepUnits = Math.ceil(fixed / margin), profit = units * margin - fixed;
            if (units >= bepUnits) {
              v.textContent = "You cross break-even at these sales.";
              v.className = "result__verdict is-no";
            } else {
              v.textContent = "Below break-even by " + (bepUnits - units).toLocaleString("en-IN") + " units.";
              v.className = "result__verdict is-yes";
            }
            document.getElementById("be-out").innerHTML = [
              row("Margin per unit", rupees(margin)),
              row("Break-even units", bepUnits.toLocaleString("en-IN")),
              row("Break-even sales", rupees(bepUnits * price)),
              row(profit >= 0 ? "Monthly profit" : "Monthly loss", rupees(Math.abs(profit)), true),
            ].join("");
            document.getElementById("be-note").textContent =
              (units >= bepUnits && units > 0
                ? "Margin of safety: " + Math.round(((units - bepUnits) / units) * 100) + "% of expected sales. "
                : "Raise sales, lift the price or cut fixed costs to reach break-even. ") + "Profit here is before tax.";
          };
          be.addEventListener("input", function () {
            trackUse("bp_breakeven");
            renderBe();
          });
          be.addEventListener("change", renderBe);
          renderBe();
        }
      })();
    </script>
