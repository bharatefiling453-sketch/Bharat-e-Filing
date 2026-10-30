    <script>
      /* Private limited company: live company calendar, structure checker, first-year compliance calendar (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Companies Act, 2013: a private company has 2 to 200 members (sections 2(68) and 3(1)(b)) and at least 2 directors, up to 15
           without a special resolution (section 149(1)); one director must stay in India for at least 182 days in the financial year
           (section 149(3)). First board meeting within 30 days of incorporation (section 173(1)); first auditor within 30 days
           (section 139(6)); share certificates within two months (section 56(4)(a)); INC-20A within 180 days (section 10A). The first
           financial year of a company incorporated on or after 1 January ends on 31 March of the following year (section 2(41)); first AGM
           within nine months of that year end (section 96(1)); AOC-4 within 30 days of the AGM (section 137) and MGT-7/7A within 60 days
           (section 92(4)). */
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
        function firstYearEnd(inc) {
          return new Date(inc.getFullYear() + 1, 2, 31);
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
          window.dataLayer.push({ event: "calculator_use", service: "private-limited-company-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live company calendar ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 180);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-inc20a]", dmy(due));
          setText("[data-bm-by]", dmy(addDays(today, 30)));
          var fy = firstYearEnd(today);
          setText("[data-agm-by]", dmy(new Date(fy.getFullYear(), 11, 31)));
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

        /* ---- Structure checker ---- */
        var sc = document.getElementById("struct-check");
        if (sc) {
          var renderStruct = function () {
            var d = Math.max(0, Math.round(Number(sc.querySelector("[name='directors']").value) || 0));
            var m = Math.max(0, Math.round(Number(sc.querySelector("[name='members']").value) || 0));
            var res = sc.querySelector("[name='resident']").checked, foreign = sc.querySelector("[name='foreign']").checked;
            var issues = [];
            if (d < 2) issues.push("A private company needs at least two directors.");
            if (m < 2) issues.push("A private company needs at least two shareholders. A single founder can form a One Person Company instead.");
            if (m > 200) issues.push("A private company can have at most 200 members, not counting current and former employee shareholders.");
            if (!res) issues.push("At least one director must stay in India for 182 days or more in the financial year.");
            var v = document.getElementById("st-verdict");
            if (issues.length) {
              v.textContent = issues.length + (issues.length === 1 ? " thing" : " things") + " to fix before filing.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Your structure meets the Companies Act’s requirements.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("st-out").innerHTML = [
              row("Directors", d + (d >= 2 && d <= 15 ? " ✓" : d > 15 ? " (special resolution)" : " (min 2)")),
              row("Shareholders", m + (m >= 2 && m <= 200 ? " ✓" : m > 200 ? " (max 200)" : " (min 2)")),
              row("Resident director", res ? "Yes" : "Needed"),
              row("Ready for SPICe+", issues.length ? "Not yet" : "Yes", true),
            ].join("");
            var note = issues.length
              ? issues[0]
              : d > 15
              ? "More than 15 directors is allowed after a special resolution of the shareholders."
              : "A director and a shareholder can be the same person. Each director needs a DIN, which can be allotted through SPICe+.";
            if (!issues.length && foreign) note = "Foreign nationals can be directors and shareholders. Foreign investment must follow the FDI rules for your sector, with reporting to the RBI.";
            document.getElementById("st-note").textContent = note;
          };
          sc.addEventListener("input", function () {
            trackUse("pvt_structure");
            renderStruct();
          });
          sc.addEventListener("change", renderStruct);
          renderStruct();
        }

        /* ---- First-year compliance calendar ---- */
        var cc = document.getElementById("cal-calc");
        if (cc) {
          var dateIn = cc.querySelector("[name='incdate']");
          dateIn.value = isoDate(day(new Date()));
          var renderCal = function () {
            var inc = parse(dateIn.value);
            if (!inc) return;
            var small = cc.querySelector("[name='small']").checked;
            var fyEnd = firstYearEnd(inc);
            var agm = new Date(fyEnd.getFullYear(), 11, 31);
            var v = document.getElementById("cc-verdict");
            v.textContent = "First financial year ends on " + dmy(fyEnd) + ".";
            v.className = "result__verdict is-no";
            document.getElementById("cc-out").innerHTML = [
              row("Board meeting by", dmy(addDays(inc, 30))),
              row("First auditor by", dmy(addDays(inc, 30))),
              row("Share certificate by", dmy(new Date(inc.getFullYear(), inc.getMonth() + 2, inc.getDate()))),
              row("INC-20A by", dmy(addDays(inc, 180))),
              row("First AGM by", dmy(agm)),
              row("AOC-4 by", dmy(addDays(agm, 30))),
              row((small ? "MGT-7A" : "MGT-7") + " by", dmy(addDays(agm, 60)), true),
            ].join("");
            document.getElementById("cc-note").textContent =
              (inc.getMonth() <= 2 ? "Incorporated between January and March, so the first financial year runs to 31 March of the following year. " : "") +
              (small
                ? "As a small company, hold at least one board meeting in each half of the calendar year, at least 90 days apart."
                : "After the first meeting, hold at least four board meetings a year, with no more than 120 days between two meetings.");
          };
          cc.addEventListener("input", function () {
            trackUse("pvt_calendar");
            renderCal();
          });
          cc.addEventListener("change", renderCal);
          renderCal();
        }
      })();
    </script>
