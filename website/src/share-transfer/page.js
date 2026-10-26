    <script>
      /* Share transfer: live transfer clock, capital gains estimator, share transfer planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* SH-4 lodged within 60 days of execution (Section 56(1)); certificate within one month of receipt (Section 56(4)); refusal notice within 30 days
           (Section 58); BEN-2 within 30 days of the declaration (Section 90); FC-TRS within 60 days of the consideration (FEMA).
           Unlisted shares: long-term if held more than 24 months, 12.5% without indexation; short-term at slab; deemed fair value rules for the
           seller, and the buyer taxed on a shortfall over ₹50,000 (rules carried into the Income-tax Act, 2025). Cess and surcharge excluded. */
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function addMonths(from, n) {
          return new Date(from.getFullYear(), from.getMonth() + n, from.getDate());
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
          window.dataLayer.push({ event: "calculator_use", service: "share-transfer", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live share transfer clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 60);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-lodge-by]", dmy(due));
          setText("[data-cert-by]", dmy(addMonths(today, 1)));
          setText("[data-refuse-by]", dmy(addDays(today, 30)));
          setText("[data-fctrs-by]", dmy(addDays(today, 60)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='lodge']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to lodge an SH-4 signed today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Capital gains estimator ---- */
        var cg = document.getElementById("cg-calc");
        if (cg) {
          var soldIn = cg.querySelector("[name='soldon']");
          soldIn.value = isoDate(new Date());
          var renderCg = function () {
            var bought = parse(cg.querySelector("[name='boughton']").value), sold = parse(soldIn.value);
            if (!bought || !sold) return;
            var cost = Math.max(0, Number(cg.querySelector("[name='cost']").value) || 0);
            var price = Math.max(0, Number(cg.querySelector("[name='price']").value) || 0);
            var fmv = Math.max(0, Number(cg.querySelector("[name='fmv']").value) || 0);
            var slab = Number(cg.querySelector("[name='slab']").value) || 0.3;
            var longTerm = sold > addMonths(bought, 24);
            var value = Math.max(price, fmv);
            var gain = value - cost;
            var rate = longTerm ? 0.125 : slab;
            var tax = Math.max(0, gain) * rate;
            var shortfall = fmv - price;
            var v = document.getElementById("cg-verdict");
            v.textContent = gain > 0 ? (longTerm ? "Long-term gain" : "Short-term gain") + ": about " + inr(tax) + " tax." : "No gain. A loss may be carried forward.";
            v.className = "result__verdict " + (gain > 0 ? "is-yes" : "is-no");
            document.getElementById("cg-out").innerHTML = [
              row("Holding", longTerm ? "Over 24 months" : "24 months or less"),
              row("Sale value taken", inr(value)),
              row("Capital gain", inr(gain)),
              row("Seller’s tax (before cess)", inr(tax), true),
            ].join("");
            document.getElementById("cg-note").textContent =
              shortfall > 50000
                ? "Price is " + inr(shortfall) + " below fair value: the buyer may be taxed on this, unless a relative received it as a gift."
                : "Estimate only, before surcharge and 4% cess. Your CA confirms the final figure.";
          };
          cg.addEventListener("input", function () {
            trackUse("share_capital_gains");
            renderCg();
          });
          cg.addEventListener("change", renderCg);
          renderCg();
        }

        /* ---- Share transfer planner ---- */
        var tp = document.getElementById("transfer-plan");
        if (tp) {
          var dateIn = tp.querySelector("[name='signedon']");
          dateIn.value = isoDate(new Date());
          var renderPlan = function () {
            var d = parse(dateIn.value);
            if (!d) return;
            var on = function (n) {
              return tp.querySelector("[name='" + n + "']").checked;
            };
            var rows = [];
            var v = document.getElementById("tp-verdict");
            if (on("demat")) {
              rows.push(row("Transfer through", "Depository participant"));
              v.textContent = "Demat shares move through your DP, not SH-4.";
            } else {
              rows.push(row("Lodge SH-4 by", dmy(addDays(d, 60))));
              rows.push(row("Refusal notice by", dmy(addDays(d, 30))));
              v.textContent = "Lodge the SH-4 within 60 days of signing.";
            }
            if (on("sbo")) rows.push(row("BEN-2 (after declaration)", "Within 30 days"));
            if (on("nonres")) rows.push(row("FC-TRS by", dmy(addDays(d, 60))));
            rows.push(row(on("demat") ? "Records updated" : "Certificate by", on("demat") ? "On DP credit" : dmy(addMonths(d, 1)), true));
            v.className = "result__verdict is-no";
            document.getElementById("tp-out").innerHTML = rows.join("");
          };
          tp.addEventListener("input", function () {
            trackUse("share_transfer_planner");
            renderPlan();
          });
          tp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
