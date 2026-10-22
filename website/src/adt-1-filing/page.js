    <script>
      /* ADT-1: live ADT-1 clock, due date and term planner, auditor rotation checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* ADT-1 within 15 days of the meeting (Section 139(1), Rule 4(2)); first auditor by the board within 30 days of incorporation, else members within
           90 days (Section 139(6)); casual vacancy filled by the board within 30 days, members' approval within 3 months after a resignation (Section 139(8));
           rotation for listed, unlisted public ≥ ₹10 cr paid-up, private ≥ ₹50 cr paid-up, or public borrowings ≥ ₹50 cr (Rule 5): individual 5 years, firm 10 */
        var AGM_DUE = new Date(2026, 9, 15);
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
          window.dataLayer.push({ event: "calculator_use", service: "adt-1-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live ADT-1 clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 15);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-adt1-by]", dmy(due));
          var late = Math.round((today - AGM_DUE) / 86400000);
          setText("[data-late-text]", late > 0 ? late + " days ago. File now to limit additional fees." : "Due in " + -late + " days.");
          setText("[data-first-by]", dmy(addDays(today, 30)));
          setText("[data-first-egm]", dmy(addDays(today, 90)));
          var agmYear = today.getMonth() > 8 ? today.getFullYear() : today.getFullYear() - 1;
          setText("[data-term-end]", String(agmYear + 5));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='adt1']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file ADT-1 for an appointment today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- ADT-1 due date and term planner ---- */
        var ap = document.getElementById("adt-plan");
        if (ap) {
          var renderPlan = function () {
            var type = ap.querySelector("[name='atype']").value;
            var d = parse(ap.querySelector("[name='meetdate']").value);
            if (!d) return;
            var due = addDays(d, 15), today = day(new Date());
            var left = Math.round((due - today) / 86400000);
            var v = document.getElementById("ap-verdict");
            v.textContent = left >= 0 ? "File ADT-1 by " + dmy(due) + "." : "ADT-1 was due on " + dmy(due) + ". File now.";
            v.className = "result__verdict " + (left >= 0 ? "is-no" : "is-yes");
            var rows = [row("Appointed by", type === "agm" ? "Members (AGM)" : type === "resigned" ? "Board + members" : "Board")];
            if (type === "agm") rows.push(row("Term ends", (d.getFullYear() + 5) + " AGM"));
            else if (type === "first") rows.push(row("Term ends", "First AGM"));
            else rows.push(row("Term ends", "Next AGM"));
            if (type === "resigned") rows.push(row("Members approve by", dmy(addMonths(d, 3))));
            rows.push(row(left >= 0 ? "ADT-1 due" : "Days late", left >= 0 ? dmy(due) : String(-left), true));
            document.getElementById("ap-out").innerHTML = rows.join("");
            document.getElementById("ap-note").textContent =
              type === "first"
                ? "The board must appoint the first auditor within 30 days of incorporation; otherwise members do so at an EGM within 90 days."
                : type === "agm"
                ? "Five years from this AGM to the end of the sixth AGM. No yearly ratification is needed."
                : type === "resigned"
                ? "After a resignation, the outgoing auditor files ADT-3 within 30 days."
                : "The board fills a casual vacancy within 30 days of it arising.";
          };
          ap.addEventListener("input", function () {
            trackUse("adt1_planner");
            renderPlan();
          });
          ap.addEventListener("change", renderPlan);
          renderPlan();
        }

        /* ---- Auditor rotation checker ---- */
        var rc = document.getElementById("rotation-check");
        if (rc) {
          var renderRot = function () {
            var type = rc.querySelector("[name='ctype']").value, firm = rc.querySelector("[name='auditor']").value === "firm";
            var cap = Math.max(0, Number(rc.querySelector("[name='capital']").value) || 0);
            var bor = Math.max(0, Number(rc.querySelector("[name='borrowings']").value) || 0);
            var served = Math.max(0, Math.floor(Number(rc.querySelector("[name='served']").value) || 0));
            var applies = type === "listed" || (type === "pub" && cap >= 10) || (type === "pvt" && cap >= 50) || bor >= 50;
            var max = firm ? 10 : 5, left = Math.max(0, max - served);
            var v = document.getElementById("rc-verdict");
            if (!applies) {
              v.textContent = "Rotation doesn’t apply. Reappoint every five years.";
              v.className = "result__verdict is-no";
            } else {
              v.textContent = left > 0 ? "Rotation applies. " + left + " more years allowed." : "Rotation applies. Appoint a new auditor.";
              v.className = "result__verdict " + (left > 0 ? "is-no" : "is-yes");
            }
            document.getElementById("rc-out").innerHTML = [
              row("Rotation", applies ? "Applies" : "Not applicable"),
              row("Maximum tenure", applies ? max + " years (" + (firm ? "two terms" : "one term") + ")" : "No limit"),
              row("Cooling-off", applies ? "5 years" : "Not applicable"),
              row("Years remaining", applies ? String(left) : "—", true),
            ].join("");
            document.getElementById("rc-note").textContent = applies
              ? "Count the years before 1 April 2014 too. After the cooling-off period, the auditor can be appointed again."
              : "Thresholds: unlisted public ₹10 crore and private ₹50 crore paid-up, or ₹50 crore of public borrowings.";
          };
          rc.addEventListener("input", function () {
            trackUse("auditor_rotation");
            renderRot();
          });
          rc.addEventListener("change", renderRot);
          renderRot();
        }
      })();
    </script>
