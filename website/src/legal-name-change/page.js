    <script>
      /* Legal name change: live plan (service targets), route finder, records update planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Target dates are Bharat e-Filing's own service timeline (ads within 3 days, Gazette application ready within 7 days), not legal
           deadlines. Gazette publication time depends on the publishing office. UIDAI allows two name updates in Aadhaar in a lifetime;
           Passport Seva accepts a central or state Gazette notification as proof of a change of name. */
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
          window.dataLayer.push({ event: "calculator_use", service: "legal-name-change", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live plan ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var ready = addDays(today, 7);
          var end = new Date(ready.getFullYear(), ready.getMonth(), ready.getDate(), 18, 0, 0);
          setText("[data-gz-ready]", dmy(ready));
          setText("[data-ads-by]", dmy(addDays(today, 3)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='gazette']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours to our target for a Gazette application started today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Route finder ---- */
        var ROUTES = {
          marriage: ["Marriage certificate", "Optional", "A marriage certificate is commonly accepted to change a surname in PAN and the passport. A Gazette notification helps if any record asks for it."],
          divorce: ["Affidavit, ads and Gazette", "Recommended", "Keep the divorce decree with your papers; some offices ask for it along with the Gazette notification."],
          spelling: ["Affidavit, ads and Gazette", "Recommended", "Use the Gazette to align every record to one spelling. Update Aadhaar only once, with the final spelling."],
          full: ["Affidavit, ads and Gazette", "Recommended", "A complete change of name is best supported by a Gazette notification, which most offices accept."],
          minor: ["Parent applies: affidavit, ads, Gazette", "Recommended", "The parent or guardian signs on the child’s behalf, with the child’s birth certificate."],
        };
        var rc = document.getElementById("route-check");
        if (rc) {
          var renderRoute = function () {
            var reason = rc.querySelector("[name='reason']").value, abroad = rc.querySelector("[name='abroad']").checked;
            var r = ROUTES[reason];
            var v = document.getElementById("rc-verdict");
            v.textContent = "Usual route: " + r[0] + ".";
            v.className = "result__verdict is-no";
            document.getElementById("rc-out").innerHTML = [
              row("Affidavit", reason === "marriage" ? "Helpful" : "Yes"),
              row("Newspaper ads", reason === "marriage" ? "For Gazette" : "Two"),
              row("Gazette", r[1], true),
            ].join("");
            document.getElementById("rc-note").textContent =
              r[2] + (abroad ? " For the passport, Passport Seva accepts a central or state Gazette notification as proof of change of name." : "");
          };
          rc.addEventListener("change", function () {
            trackUse("name_route");
            renderRoute();
          });
          renderRoute();
        }

        /* ---- Records update planner ---- */
        var ORDER = [
          ["aadhaar", "Aadhaar", "first, with final proof"],
          ["pan", "PAN", "with proof of new name"],
          ["bank", "Bank accounts", "with updated PAN and Aadhaar"],
          ["passport", "Passport", "Gazette or accepted proof"],
          ["voter", "Voter ID or licence", "each with its own form"],
          ["invest", "Insurance, demat or property", "last, with all the above"],
        ];
        var rp = document.getElementById("records-check");
        if (rp) {
          var renderPlan = function () {
            var picked = ORDER.filter(function (o) {
              return rp.querySelector("[name='" + o[0] + "']").checked;
            });
            var v = document.getElementById("rp-verdict");
            if (!picked.length) {
              v.textContent = "Tick the records you hold to see the order.";
              v.className = "result__verdict is-yes";
              document.getElementById("rp-out").innerHTML = "";
              document.getElementById("rp-note").textContent = "";
              return;
            }
            v.textContent = picked.length + (picked.length === 1 ? " record" : " records") + " to update, starting with " + picked[0][1] + ".";
            v.className = "result__verdict is-no";
            document.getElementById("rp-out").innerHTML = picked
              .map(function (o, i) {
                return row(i + 1 + ". " + o[1], o[2], i === picked.length - 1);
              })
              .join("");
            document.getElementById("rp-note").textContent =
              "Aadhaar allows two name updates in a lifetime, so update it once your proof is final. Keep the PAN and Aadhaar names identical.";
          };
          rp.addEventListener("change", function () {
            trackUse("name_records");
            renderPlan();
          });
          renderPlan();
        }
      })();
    </script>
