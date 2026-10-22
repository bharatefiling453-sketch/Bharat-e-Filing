    <script>
      /* Registered office change: live office move clock, route finder, deadline planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* INC-22: 30 days (Section 12(4)); MGT-14: 30 days (Section 117); GST core amendment: 15 days (Rule 19); INC-26 advert within 30 days before INC-23 (Rule 30);
           RD to decide within 60 days (Section 13(4)); INC-28: 30 days from the order (Section 13(5)) */
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
          window.dataLayer.push({ event: "calculator_use", service: "registered-office-change", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live office move clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-inc22-by]", dmy(due));
          setText("[data-mgt14-by]", dmy(addDays(today, 30)));
          setText("[data-gst-by]", dmy(addDays(today, 15)));
          setText("[data-inc23-by]", dmy(addDays(today, 30)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='inc22']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file INC-22 for a move made today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Office move route finder ---- */
        var rf = document.getElementById("route-find");
        if (rf) {
          var ROUTES = {
            company: {
              city: ["Board resolution is enough.", "Board", "INC-22", "About 1 week"],
              state: ["Special resolution needed.", "Board + special", "MGT-14, INC-22", "2–3 weeks"],
              roc: ["Regional Director must confirm.", "Board + special", "MGT-14, INC-23, INC-28, INC-22", "4–6 weeks"],
              interstate: ["Regional Director approval needed.", "Board + special", "MGT-14, INC-26, INC-23, INC-28, INC-22", "2–3 months"],
            },
            llp: {
              city: ["Partners’ consent is enough.", "Partners", "Form 15", "About 1 week"],
              state: ["Partners’ consent is enough.", "Partners", "Form 15", "1–2 weeks"],
              roc: ["Partners’ consent, new ROC informed.", "Partners", "Form 15", "1–2 weeks"],
              interstate: ["Notice and creditor consent first.", "Partners + creditors", "Notice, Form 15", "4–6 weeks"],
            },
          };
          var renderRoute = function () {
            var entity = rf.querySelector("[name='entity']").value, move = rf.querySelector("[name='move']").value;
            var gst = rf.querySelector("[name='gstin']").checked, pending = rf.querySelector("[name='pending']").checked;
            var r = ROUTES[entity][move];
            var blocked = pending && entity === "company" && move === "interstate";
            var v = document.getElementById("rf-verdict");
            v.textContent = blocked ? "A state shift isn’t allowed while this is pending." : r[0];
            v.className = "result__verdict " + (blocked || move === "interstate" || move === "roc" ? "is-yes" : "is-no");
            var gstText = !gst ? "Not registered" : move === "interstate" ? "New registration" : "Amend in 15 days";
            document.getElementById("rf-out").innerHTML = [
              row("Approval", r[1]),
              row("Forms", r[2]),
              row("GST", gstText),
              row("Typical time", r[3], true),
            ].join("");
            document.getElementById("rf-note").textContent = blocked
              ? "Rule 30 bars the shift while an inquiry, inspection, investigation or prosecution is pending. Talk to us about the options."
              : entity === "company"
              ? "INC-22 is filed within 30 days of every change of registered office, whatever the route."
              : "Form 15 is filed within 30 days; Form 3 too if the LLP agreement changes.";
          };
          rf.addEventListener("change", function () {
            trackUse("office_route_finder");
            renderRoute();
          });
          renderRoute();
        }

        /* ---- Office move deadline planner ---- */
        var dp = document.getElementById("deadline-plan");
        if (dp) {
          var dateIn = dp.querySelector("[name='effective']");
          dateIn.value = isoDate(new Date());
          var renderPlan = function () {
            var route = dp.querySelector("[name='droute']").value;
            var d = parse(dateIn.value);
            if (!d) return;
            var rows = [], v = document.getElementById("dp-verdict");
            if (route === "interstate") {
              var ad = addDays(d, 7), inc23 = addDays(ad, 7), order = addDays(inc23, 60);
              rows.push(row("MGT-14 by", dmy(addDays(d, 30))));
              rows.push(row("INC-26 notice (target)", dmy(ad)));
              rows.push(row("INC-23 by", dmy(addDays(ad, 30))));
              rows.push(row("RD order (expected by)", dmy(order)));
              rows.push(row("INC-28 by", dmy(addDays(order, 30)), true));
              v.textContent = "State shift: file INC-23 within 30 days of the notice.";
            } else {
              if (route === "state") rows.push(row("MGT-14 by", dmy(addDays(d, 30))));
              rows.push(row("GST amendment by", dmy(addDays(d, 15))));
              rows.push(row("INC-22 by", dmy(addDays(d, 30)), true));
              v.textContent = route === "city" ? "Same city: board resolution and INC-22." : "Same state: MGT-14 and INC-22 within 30 days.";
            }
            v.className = "result__verdict is-no";
            document.getElementById("dp-out").innerHTML = rows.join("");
          };
          dp.addEventListener("input", function () {
            trackUse("office_deadline_planner");
            renderPlan();
          });
          dp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
