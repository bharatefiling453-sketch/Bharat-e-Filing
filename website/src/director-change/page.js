    <script>
      /* Director change: live director change clock, director change checker, deadline planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* DIR-12: 30 days (Section 170(2), Rule 18); DIR-11: 30 days (Section 168(1)); special notice: at least 14 days before the meeting (Section 115);
           additional director holds office until the next AGM, latest 30 Sep (Section 161(1), Section 96); minimum directors: Section 149(1) */
        var MIN = { pvt: 2, pub: 3, opc: 1 };
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
        function nextAgm(from) {
          var x = new Date(from.getFullYear(), 8, 30);
          return x < from ? new Date(from.getFullYear() + 1, 8, 30) : x;
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
          window.dataLayer.push({ event: "calculator_use", service: "director-change", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live director change clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-dir12-by]", dmy(due));
          setText("[data-dir11-by]", dmy(due));
          setText("[data-meeting-from]", dmy(addDays(today, 14)));
          setText("[data-agm-by]", dmy(nextAgm(today)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='dir12']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file DIR-12 for a change made today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Director change checker ---- */
        var bc = document.getElementById("board-check");
        if (bc) {
          var STEPS = {
            additional: ["Board resolution", "DIR-2, DIR-8, DIR-12", "Holds office until the next AGM; regularise it there."],
            general: ["Shareholders’ resolution", "DIR-2, DIR-8, DIR-12", "Appointed at the general meeting; no regularisation needed."],
            resign: ["Notice to the company", "DIR-12 (+ DIR-11 optional)", "Effective from receipt of the notice or the date in it, whichever is later."],
            remove: ["Ordinary resolution", "Special notice, DIR-12", "Special notice at least 14 days before the meeting; the director can be heard."],
          };
          var renderBoard = function () {
            var type = bc.querySelector("[name='ctype']").value, change = bc.querySelector("[name='change']").value;
            var after = Math.max(0, Math.floor(Number(bc.querySelector("[name='after']").value) || 0));
            var resident = bc.querySelector("[name='resident']").checked;
            var s = STEPS[change];
            var low = after < MIN[type], high = after > 15, issue = low || !resident;
            var v = document.getElementById("bc-verdict");
            if (low) v.textContent = "Board falls below the minimum of " + MIN[type] + ". Appoint first.";
            else if (!resident) v.textContent = "Keep at least one resident director.";
            else v.textContent = high ? "Over 15 directors needs a special resolution." : "This change keeps your board valid.";
            v.className = "result__verdict " + (issue || high ? "is-yes" : "is-no");
            document.getElementById("bc-out").innerHTML = [
              row("Approval", s[0]),
              row("Forms", s[1]),
              row("Minimum board", MIN[type] + " · you’d have " + after),
              row("File DIR-12 within", "30 days", true),
            ].join("");
            document.getElementById("bc-note").textContent = s[2];
          };
          bc.addEventListener("input", function () {
            trackUse("director_change_checker");
            renderBoard();
          });
          bc.addEventListener("change", renderBoard);
          renderBoard();
        }

        /* ---- Director change deadline planner ---- */
        var cp = document.getElementById("change-plan");
        if (cp) {
          var dateIn = cp.querySelector("[name='eventdate']");
          var lbl = document.getElementById("cp-date-label");
          dateIn.value = isoDate(new Date());
          var LABEL = { appoint: "Appointed on", resign: "Resignation received on", remove: "Special notice received on" };
          var renderPlan = function () {
            var change = cp.querySelector("[name='pchange']").value;
            lbl.textContent = LABEL[change];
            var d = parse(dateIn.value);
            if (!d) return;
            var rows = [], v = document.getElementById("cp-verdict");
            if (change === "appoint") {
              rows.push(row("GST amendment by", dmy(addDays(d, 15))));
              rows.push(row("Regularise by (latest)", dmy(nextAgm(d))));
              rows.push(row("DIR-12 by", dmy(addDays(d, 30)), true));
              v.textContent = "File DIR-12 within 30 days of the appointment.";
            } else if (change === "resign") {
              rows.push(row("DIR-11 by (optional)", dmy(addDays(d, 30))));
              rows.push(row("GST amendment by", dmy(addDays(d, 15))));
              rows.push(row("DIR-12 by", dmy(addDays(d, 30)), true));
              v.textContent = "The company files DIR-12 within 30 days.";
            } else {
              var meet = addDays(d, 14);
              rows.push(row("Meeting no earlier than", dmy(meet)));
              rows.push(row("DIR-12 by (if held then)", dmy(addDays(meet, 30)), true));
              v.textContent = "Hold the meeting at least 14 days after the special notice.";
            }
            v.className = "result__verdict is-no";
            document.getElementById("cp-out").innerHTML = rows.join("");
          };
          cp.addEventListener("input", function () {
            trackUse("director_change_deadlines");
            renderPlan();
          });
          cp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
