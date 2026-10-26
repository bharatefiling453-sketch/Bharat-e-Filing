    <script>
      /* Authorised capital increase: live clock, authorised capital calculator, share capital route finder (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Increase by ordinary resolution if the articles authorise it (Section 61(1)); SH-7 within 30 days (Section 64); PAS-3 within 15 days of
           allotment (Section 39(4), Rule 12); private placement allotment within 60 days of receiving money (Section 42(6)); EGM on 21 clear days' notice */
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
          window.dataLayer.push({ event: "calculator_use", service: "authorised-capital-increase", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live capital increase clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-sh7-by]", dmy(due));
          setText("[data-pas3-by]", dmy(addDays(today, 15)));
          setText("[data-egm-from]", dmy(addDays(today, 22)));
          setText("[data-pp-by]", dmy(addDays(today, 60)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='sh7']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file SH-7 for a resolution passed today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Authorised capital calculator ---- */
        var cc = document.getElementById("capital-calc");
        if (cc) {
          var renderCap = function () {
            var auth = Math.max(0, Number(cc.querySelector("[name='authorised']").value) || 0);
            var paid = Math.max(0, Number(cc.querySelector("[name='paidup']").value) || 0);
            var add = Math.max(0, Number(cc.querySelector("[name='newshares']").value) || 0);
            var head = Number(cc.querySelector("[name='headroom']").value) || 0;
            var fv = Number(cc.querySelector("[name='facevalue']").value) || 10;
            var needed = paid + add;
            var target = Math.ceil((needed * (1 + head)) / 100000) * 100000;
            var v = document.getElementById("cc-verdict");
            if (target <= auth) {
              v.textContent = "No increase needed. Your limit covers this.";
              v.className = "result__verdict is-no";
              document.getElementById("cc-out").innerHTML = [
                row("Paid-up after issue", inr(needed)),
                row("Room left after issue", inr(auth - needed)),
                row("Action", "Allot within limit", true),
              ].join("");
              return;
            }
            v.textContent = "Increase authorised capital to " + inr(target) + ".";
            v.className = "result__verdict is-yes";
            document.getElementById("cc-out").innerHTML = [
              row("Paid-up after issue", inr(needed)),
              row("Increase by", inr(target - auth)),
              row("Shares in new limit", Math.floor(target / fv).toLocaleString("en-IN") + " of " + inr(fv)),
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

        /* ---- Share capital change route finder ---- */
        var rf = document.getElementById("route-find");
        if (rf) {
          var NOTES = {
            increase: "Attach the altered MOA to SH-7, then allot within the new limit.",
            split: "Replace share certificates, or update the depository for demat shares.",
            consolidate: "Replace share certificates; fractional entitlements need a plan.",
            cancel: "Only shares no one has taken or agreed to take can be cancelled.",
          };
          var renderRoute = function () {
            var change = rf.querySelector("[name='change']").value;
            var aoa = rf.querySelector("[name='aoapower']").checked, opc = rf.querySelector("[name='opc']").checked;
            var res = opc ? "Sole member’s resolution" : aoa ? "Ordinary resolution" : "Special (AOA) + ordinary";
            var forms = aoa ? "SH-7" : "MGT-14, SH-7";
            var v = document.getElementById("rf-verdict");
            v.textContent = aoa ? "File SH-7 within 30 days." : "Alter the articles first, in the same meeting.";
            v.className = "result__verdict " + (aoa ? "is-no" : "is-yes");
            document.getElementById("rf-out").innerHTML = [
              row("Resolution", res),
              row("Forms", forms),
              row("Section", "61(1) and 64"),
              row("Typical time", "1–2 weeks", true),
            ].join("");
            document.getElementById("rf-note").textContent = NOTES[change];
          };
          rf.addEventListener("change", function () {
            trackUse("share_capital_route");
            renderRoute();
          });
          renderRoute();
        }
      })();
    </script>
