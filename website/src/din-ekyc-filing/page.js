    <script>
      /* DIN eKYC: live DIN KYC clock, KYC status checker, change update deadline (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Rule 12A as amended by G.S.R. 943(E), from 31 Mar 2026: DIR-3 KYC Web once every three financial years by 30 June; changes in mobile,
           email or address within 30 days; ₹5,000 late fee. Next routine date for 2025 filers taken on the earlier reading (30 Jun 2028). */
        var NEXT_2025 = new Date(2028, 5, 30);
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
        function daysBetween(a, b) {
          return Math.round((b - a) / 86400000);
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
          window.dataLayer.push({ event: "calculator_use", service: "din-ekyc-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live DIN KYC clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-upd-by]", dmy(due));
          setText("[data-next-days]", String(Math.max(0, daysBetween(today, NEXT_2025))));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='upd']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to update KYC for a change made today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- DIN KYC status checker ---- */
        var ks = document.getElementById("kyc-status");
        if (ks) {
          var renderStatus = function () {
            var last = ks.querySelector("[name='last']").value;
            var deact = ks.querySelector("[name='deactivated']").checked || last === "missed";
            var changed = ks.querySelector("[name='changed']").checked;
            var v = document.getElementById("ks-verdict");
            var next = last === "2025" ? dmy(NEXT_2025) : last === "2026" ? "Three years after your filing" : last === "new" ? "Per your DIN date" : "After you refile";
            var action, fee;
            if (deact) {
              action = "File now to reactivate";
              fee = "₹5,000";
              v.textContent = "Your DIN needs KYC now to be reactivated.";
              v.className = "result__verdict is-yes";
            } else if (changed) {
              action = "Update within 30 days";
              fee = "None if on time";
              v.textContent = "Update your KYC within 30 days of the change.";
              v.className = "result__verdict is-yes";
            } else {
              action = "Nothing due now";
              fee = "None";
              v.textContent = "You’re up to date. No KYC due right now.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("ks-out").innerHTML = [
              row("Action", action),
              row("Form", "DIR-3 KYC Web"),
              row("Late fee", fee),
              row("Next routine KYC", next, true),
            ].join("");
            document.getElementById("ks-note").textContent =
              last === "2025"
                ? "30 June 2028 is the earlier reading of the rule; some read it as 30 June 2029. We confirm yours from the DIN record."
                : "Your exact window depends on your DIN record. We confirm it in the free status check.";
          };
          ks.addEventListener("change", function () {
            trackUse("din_kyc_status");
            renderStatus();
          });
          renderStatus();
        }

        /* ---- Change update deadline (30 days for mobile, email or address) ---- */
        var up = document.getElementById("update-plan");
        if (up) {
          var dateIn = up.querySelector("[name='changedon']");
          dateIn.value = isoDate(new Date());
          var renderUpdate = function () {
            var what = up.querySelector("[name='what']").value;
            var d = parse(dateIn.value);
            if (!d) return;
            var v = document.getElementById("up-verdict");
            if (what === "name") {
              v.textContent = "Name and other particulars change through DIR-6.";
              v.className = "result__verdict is-no";
              document.getElementById("up-out").innerHTML = [row("Form", "DIR-6 with proof"), row("Then", "Update PAN first if needed", true)].join("");
              return;
            }
            var by = addDays(d, 30), left = daysBetween(day(new Date()), by);
            v.textContent = left >= 0 ? "Update by " + dmy(by) + "." : "Overdue by " + -left + " days. File now.";
            v.className = "result__verdict " + (left >= 0 ? "is-no" : "is-yes");
            document.getElementById("up-out").innerHTML = [
              row("Form", "DIR-3 KYC Web"),
              row("Days left", left >= 0 ? String(left) : "0"),
              row("Update by", dmy(by), true),
            ].join("");
          };
          up.addEventListener("input", function () {
            trackUse("din_update_deadline");
            renderUpdate();
          });
          up.addEventListener("change", renderUpdate);
          renderUpdate();
        }
      })();
    </script>
