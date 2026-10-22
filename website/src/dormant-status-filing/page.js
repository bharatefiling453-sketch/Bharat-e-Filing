    <script>
      /* Dormant status: live dormant clock, eligibility checker, dormant company calendar (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Inactive: no business or significant accounting transaction in the last two financial years (Section 455 Explanation); MSC-1 after a special
           resolution or three-fourths consent (Rule 3); MSC-3 within 30 days of each year end; MSC-4 within 7 days of an act ending dormancy (Rule 8);
           strike-off after five consecutive dormant years (Section 455(6)); board meetings one per half calendar year, 90 days apart (Section 173(5)) */
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
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
        }
        function fyStart(d) {
          return d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1;
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
          window.dataLayer.push({ event: "calculator_use", service: "dormant-status-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live dormant status clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = new Date(today.getFullYear(), 3, 30);
          if (due < today) due = new Date(today.getFullYear() + 1, 3, 30);
          var end = new Date(due.getFullYear(), 3, 30, 23, 59, 59);
          var fy = fyStart(today);
          setText("[data-msc3-by]", dmy(due));
          setText("[data-inactive-since]", dmy(new Date(fy - 2, 3, 1)));
          setText("[data-msc4-by]", dmy(addDays(today, 7)));
          setText("[data-limit-by]", dmy(new Date(fy + 5, 2, 31)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='msc3']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next MSC-3 due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Dormant eligibility checker ---- */
        var el = document.getElementById("eligibility");
        if (el) {
          var renderElig = function () {
            var reason = el.querySelector("[name='reason']").value;
            var years = Math.max(0, Math.floor(Number(el.querySelector("[name='idleyears']").value) || 0));
            var on = function (n) {
              return el.querySelector("[name='" + n + "']").checked;
            };
            var blockers = [];
            if (on("probe")) blockers.push("pending inquiry or prosecution");
            if (on("deposits")) blockers.push("public deposits");
            if (on("dues")) blockers.push("unpaid dues");
            if (on("dispute")) blockers.push("management dispute");
            var shortIdle = reason === "inactive" && years < 2;
            var ok = !blockers.length && !shortIdle;
            var v = document.getElementById("el-verdict");
            v.textContent = ok ? "Looks eligible for dormant status." : shortIdle && !blockers.length ? "Not yet: two inactive years are needed." : "Not eligible until the blockers are cleared.";
            v.className = "result__verdict " + (ok ? "is-no" : "is-yes");
            document.getElementById("el-out").innerHTML = [
              row("Ground", reason === "inactive" ? "Inactive company" : reason === "project" ? "Future project" : "Holding asset or IP"),
              row("Approval", "Special resolution"),
              row("Lender concurrence", on("unsecured") ? "Needed" : "Not needed"),
              row("Form", ok ? "MSC-1" : "Clear blockers first", true),
            ].join("");
            document.getElementById("el-note").textContent = blockers.length
              ? "Clear these first: " + blockers.join(", ") + "."
              : shortIdle
              ? "Eligible as inactive after " + (2 - years) + " more year" + (2 - years === 1 ? "" : "s") + " with no significant transactions."
              : on("unsecured")
              ? "An unsecured loan is fine with the lender’s written concurrence attached to MSC-1."
              : "We confirm from your accounts that only allowed payments were made.";
          };
          el.addEventListener("input", function () {
            trackUse("dormant_eligibility");
            renderElig();
          });
          el.addEventListener("change", renderElig);
          renderElig();
        }

        /* ---- Dormant company calendar ---- */
        var cl = document.getElementById("calendar");
        if (cl) {
          var renderCal = function () {
            var d = parse(cl.querySelector("[name='granted']").value);
            if (!d) return;
            var today = day(new Date());
            var fy = fyStart(d);
            var first = new Date(fy + 1, 3, 30);
            var next = new Date(today.getFullYear(), 3, 30);
            if (next < today) next = new Date(today.getFullYear() + 1, 3, 30);
            if (next < first) next = first;
            var limit = new Date(fy + 5, 2, 31);
            var v = document.getElementById("cl-verdict");
            v.textContent = limit < today ? "Five-year limit passed. Act now." : "Next MSC-3 due by " + dmy(next) + ".";
            v.className = "result__verdict " + (limit < today ? "is-yes" : "is-no");
            document.getElementById("cl-out").innerHTML = [
              row("First MSC-3", dmy(first)),
              row("Board meetings", "2 a year"),
              row("Reactivate or close by", dmy(limit), true),
            ].join("");
          };
          cl.addEventListener("input", function () {
            trackUse("dormant_calendar");
            renderCal();
          });
          cl.addEventListener("change", renderCal);
          renderCal();
        }
      })();
    </script>
