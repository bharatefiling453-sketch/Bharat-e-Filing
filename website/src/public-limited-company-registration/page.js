    <script>
      /* Public limited company: live company calendar, board requirements checker, first-year compliance calendar (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Companies Act, 2013: a public company has at least 7 members (section 3(1)(a)) and 3 directors, up to 15 without a special
           resolution (section 149(1)); one director resident 182 days in the financial year (section 149(3)). Unlisted public companies with
           paid-up capital >= ₹10 crore, turnover >= ₹100 crore or outstanding loans, debentures and deposits > ₹50 crore need two independent
           directors (rule 4, Appointment and Qualification of Directors Rules) and audit and nomination committees (rule 6, Meetings of Board
           Rules); JVs, wholly owned subsidiaries and dormant companies are exempt. Woman director at paid-up capital >= ₹100 crore or turnover
           >= ₹300 crore (rule 3). Whole-time KMP at paid-up capital >= ₹10 crore (rule 8, Managerial Personnel Rules). Demat and half-yearly
           PAS-6 within 60 days of each half-year end (rule 9A, Prospectus and Allotment of Securities Rules). First board meeting and auditor
           within 30 days (sections 173(1), 139(6)); share certificates within two months (section 56(4)(a)); INC-20A within 180 days
           (section 10A); first year ends 31 March (section 2(41)); first AGM within nine months, later AGMs by 30 September (section 96);
           AOC-4 within 30 days and MGT-7 within 60 days of the AGM. */
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
        /* first half-year end (30 Sep or 31 Mar) on or after a date */
        function halfYearEnd(d) {
          var y = d.getFullYear(), m = d.getMonth();
          if (m <= 2) return new Date(y, 2, 31);
          if (m <= 8) return new Date(y, 8, 30);
          return new Date(y + 1, 2, 31);
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
          window.dataLayer.push({ event: "calculator_use", service: "public-limited-company-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live company calendar ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear(), m = today.getMonth();
          var due = addDays(today, 180);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-inc20a]", dmy(due));
          /* PAS-6: the most recent half-year end whose 60-day window is still open, else the next one */
          var prevEnd = m <= 2 ? new Date(y - 1, 8, 30) : m <= 8 ? new Date(y, 2, 31) : new Date(y, 8, 30);
          var hEnd = addDays(prevEnd, 60) >= today ? prevEnd : halfYearEnd(addDays(prevEnd, 1));
          setText("[data-pas6-by]", dmy(addDays(hEnd, 60)));
          setText("[data-pas6-label]", "PAS-6 for the half-year ending " + dmy(hEnd) + " is due by");
          var fyEnd = m >= 3 && m <= 8 ? y : m <= 2 ? y : y + 1;
          setText("[data-agm-by]", dmy(new Date(fyEnd, 8, 30)));
          setText("[data-agm-label]", "The AGM for FY " + (fyEnd - 1) + "-" + String(fyEnd).slice(2) + " is due by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='inc20a']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until INC-20A is due for a company incorporated today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Board requirements checker ---- */
        var bc = document.getElementById("board-check");
        if (bc) {
          var num = function (n) {
            return Math.max(0, Number(bc.querySelector("[name='" + n + "']").value) || 0);
          };
          var renderBoard = function () {
            var d = Math.round(num("directors")), m = Math.round(num("members"));
            var cap = num("capital"), turn = num("turnover"), loans = num("loans");
            var res = bc.querySelector("[name='resident']").checked, wos = bc.querySelector("[name='wos']").checked;
            var big = cap >= 10 || turn >= 100 || loans > 50;
            var idNeeded = big && !wos, woman = cap >= 100 || turn >= 300, kmp = cap >= 10;
            var issues = [];
            if (d < 3) issues.push("A public company needs at least three directors.");
            if (m < 7) issues.push("A public company needs at least seven members.");
            if (!res) issues.push("At least one director must stay in India for 182 days or more in the financial year.");
            var v = document.getElementById("bc-verdict");
            if (issues.length) {
              v.textContent = issues.length + (issues.length === 1 ? " thing" : " things") + " to fix before filing.";
              v.className = "result__verdict is-yes";
            } else {
              var extra = (idNeeded ? 1 : 0) + (woman ? 1 : 0) + (kmp ? 1 : 0);
              v.textContent = extra ? "Structure meets the minimum; " + extra + " board rule" + (extra === 1 ? " applies." : "s apply.") : "Structure meets the minimum.";
              v.className = "result__verdict " + (extra ? "is-yes" : "is-no");
            }
            document.getElementById("bc-out").innerHTML = [
              row("Directors / members", d + " / " + m + (d >= 3 && m >= 7 ? " ✓" : "")),
              row("Independent directors", idNeeded ? "At least 2" : "Not required"),
              row("Audit committee", idNeeded ? "Required" : "Not required"),
              row("Woman director", woman ? "Required" : "Not required"),
              row("Whole-time KMP", kmp ? "Required" : "Not required", true),
            ].join("");
            document.getElementById("bc-note").textContent = issues.length
              ? issues[0]
              : big && wos
              ? "As a wholly owned subsidiary, joint venture or dormant company, the independent director and committee rules don’t apply."
              : kmp
              ? "Whole-time KMP means a managing director, CEO, manager or whole-time director, a company secretary and a CFO."
              : "Thresholds use the figures in the latest audited financial statements. A listed company follows stricter rules.";
          };
          bc.addEventListener("input", function () {
            trackUse("pub_board");
            renderBoard();
          });
          bc.addEventListener("change", renderBoard);
          renderBoard();
        }

        /* ---- First-year compliance calendar ---- */
        var cc = document.getElementById("cal-calc");
        if (cc) {
          var dateIn = cc.querySelector("[name='incdate']");
          dateIn.value = isoDate(day(new Date()));
          var renderCal = function () {
            var inc = parse(dateIn.value);
            if (!inc) return;
            var fyEnd = new Date(inc.getFullYear() + 1, 2, 31);
            var agm = new Date(fyEnd.getFullYear(), 11, 31);
            var v = document.getElementById("cc-verdict");
            v.textContent = "First financial year ends on " + dmy(fyEnd) + ".";
            v.className = "result__verdict is-no";
            document.getElementById("cc-out").innerHTML = [
              row("Board meeting by", dmy(addDays(inc, 30))),
              row("First auditor by", dmy(addDays(inc, 30))),
              row("Share certificate by", dmy(new Date(inc.getFullYear(), inc.getMonth() + 2, inc.getDate()))),
              row("INC-20A by", dmy(addDays(inc, 180))),
              row("First PAS-6 by", dmy(addDays(halfYearEnd(inc), 60))),
              row("First AGM by", dmy(agm)),
              row("AOC-4 by", dmy(addDays(agm, 30))),
              row("MGT-7 by", dmy(addDays(agm, 60)), true),
            ].join("");
            document.getElementById("cc-note").textContent =
              (inc.getMonth() <= 2 ? "Incorporated between January and March, so the first financial year runs to 31 March of the following year. " : "") +
              "Shares are issued in demat form. After the first meeting, hold at least four board meetings a year, no more than 120 days apart.";
          };
          cc.addEventListener("input", function () {
            trackUse("pub_calendar");
            renderCal();
          });
          cc.addEventListener("change", renderCal);
          renderCal();
        }
      })();
    </script>
