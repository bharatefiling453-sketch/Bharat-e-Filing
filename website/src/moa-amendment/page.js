    <script>
      /* MOA amendment: live MOA clock, MOA change route finder, authorised capital calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* MGT-14 within 30 days of a special resolution (Section 117); SH-7 within 30 days of a capital alteration (Section 64);
           general meeting on 21 clear days' notice (Section 101); Registrar registers within 30 days of filing (Section 13(9)) */
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
          window.dataLayer.push({ event: "calculator_use", service: "moa-amendment", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live MOA amendment clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-file-by]", dmy(due));
          setText("[data-sh7-by]", dmy(due));
          setText("[data-egm-from]", dmy(addDays(today, 22)));
          setText("[data-roc-by]", dmy(due));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='mgt14']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file MGT-14 for a resolution passed today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- MOA change route finder ---- */
        var rf = document.getElementById("route-find");
        if (rf) {
          var ROUTE = {
            objects: ["Special resolution", "MGT-14", "Registrar registers", "2–3 weeks"],
            capital: ["Ordinary resolution", "SH-7", "Registrar records", "1–2 weeks"],
            name: ["Special resolution", "RUN, MGT-14, INC-24", "Registrar approval", "3–5 weeks"],
            state: ["Special resolution", "MGT-14, INC-23, INC-28", "Regional Director", "2–3 months"],
            liability: ["Special resolution", "MGT-14", "Registrar registers", "2–3 weeks"],
          };
          var renderRoute = function () {
            var clause = rf.querySelector("[name='clause']").value;
            var aoa = rf.querySelector("[name='aoapower']").checked, unused = rf.querySelector("[name='unused']").checked;
            var r = ROUTE[clause].slice();
            var extra = "";
            if (clause === "capital" && !aoa) {
              r[0] = "Special (AOA) + ordinary";
              r[1] = "MGT-14, SH-7";
              extra = "Alter the articles first by special resolution to give the power, in the same meeting.";
            }
            if (clause === "objects" && unused) {
              r[0] = "Special resolution by postal ballot";
              extra = "With unused public-issue money: newspaper notice and an exit offer to dissenting shareholders.";
            }
            var v = document.getElementById("rf-verdict");
            v.textContent = clause === "state" ? "Needs Regional Director approval." : clause === "name" ? "Needs Registrar approval of the name." : "File within 30 days of the resolution.";
            v.className = "result__verdict " + (clause === "state" || extra ? "is-yes" : "is-no");
            document.getElementById("rf-out").innerHTML = [
              row("Resolution", r[0]),
              row("Forms", r[1]),
              row("Approval", r[2]),
              row("Typical time", r[3], true),
            ].join("");
            document.getElementById("rf-note").textContent =
              extra ||
              (clause === "objects"
                ? "Attach the altered MOA to MGT-14. The change takes effect once registered."
                : clause === "capital"
                ? "Attach the altered capital clause to SH-7, then allot shares within the new limit."
                : "We handle this as a separate service with its own steps.");
          };
          rf.addEventListener("change", function () {
            trackUse("moa_route_finder");
            renderRoute();
          });
          renderRoute();
        }

        /* ---- Authorised capital calculator ---- */
        var cc = document.getElementById("capital-calc");
        if (cc) {
          var renderCap = function () {
            var auth = Math.max(0, Number(cc.querySelector("[name='authorised']").value) || 0);
            var paid = Math.max(0, Number(cc.querySelector("[name='paidup']").value) || 0);
            var add = Math.max(0, Number(cc.querySelector("[name='newshares']").value) || 0);
            var needed = paid + add;
            var room = auth - paid;
            var v = document.getElementById("cc-verdict");
            if (needed <= auth) {
              v.textContent = "No increase needed. You have room for this issue.";
              v.className = "result__verdict is-no";
              document.getElementById("cc-out").innerHTML = [
                row("Headroom now", inr(room)),
                row("After this issue", inr(auth - needed)),
                row("Action", "Allot within limit", true),
              ].join("");
              return;
            }
            var target = Math.ceil(needed / 100000) * 100000;
            v.textContent = "Increase authorised capital to at least " + inr(target) + ".";
            v.className = "result__verdict is-yes";
            document.getElementById("cc-out").innerHTML = [
              row("Paid-up after issue", inr(needed)),
              row("Increase by", inr(target - auth)),
              row("New authorised capital", inr(target), true),
            ].join("");
          };
          cc.addEventListener("input", function () {
            trackUse("authorised_capital_calc");
            renderCap();
          });
          cc.addEventListener("change", renderCap);
          renderCap();
        }
      })();
    </script>
