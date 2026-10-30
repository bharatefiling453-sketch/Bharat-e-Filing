    <script>
      /* One Person Company: live OPC calendar, eligibility checker, first-year compliance calendar (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Companies Act, 2013 and Companies (Incorporation) Rules, 2014 (rule 3, as amended from 1 April 2021): only an Indian citizen, whether
           resident in India or not, can form an OPC or be its nominee; resident means 120 days in India in the preceding financial year; one OPC per
           person. INC-20A within 180 days (section 10A); first auditor within 30 days (section 139(6)); share certificates within two months
           (section 56(4)(a)); the first financial year of a company incorporated on or after 1 January ends on 31 March of the following year
           (section 2(41)); OPC files AOC-4 within 180 days of the year end (section 137); MGT-7A within 60 days of the date its AGM would be due. */
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
          window.dataLayer.push({ event: "calculator_use", service: "one-person-company-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live OPC calendar ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear();
          var due = addDays(today, 180);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-inc20a]", dmy(due));
          setText("[data-aud-by]", dmy(addDays(today, 30)));
          var aoc = addDays(new Date(y, 2, 31), 180);
          if (aoc < today) aoc = addDays(new Date(y + 1, 2, 31), 180);
          setText("[data-aoc-by]", dmy(aoc));
          setText("[data-aoc-label]", "AOC-4 for FY " + (aoc.getFullYear() - 1) + "-" + String(aoc.getFullYear()).slice(2) + " is due within 180 days of the year end, by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='inc20a']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until INC-20A is due for an OPC incorporated today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Eligibility checker ---- */
        var ec = document.getElementById("elig-check");
        if (ec) {
          var renderElig = function () {
            var citizen = ec.querySelector("[name='citizen']").value === "in";
            var days = Math.max(0, Math.round(Number(ec.querySelector("[name='days']").value) || 0));
            var other = ec.querySelector("[name='other']").checked, nominee = ec.querySelector("[name='nominee']").checked;
            var resident = days >= 120;
            var v = document.getElementById("ec-verdict"), note;
            var ok = citizen && !other && nominee;
            if (!citizen) {
              v.textContent = "Not eligible: only Indian citizens can form an OPC.";
              note = "Foreign nationals can set up a private limited company instead, subject to the FDI rules.";
            } else if (other) {
              v.textContent = "Not eligible: one person can form only one OPC.";
              note = "You can convert your existing OPC into a private company, or form a private limited company for the new business.";
            } else if (!nominee) {
              v.textContent = "Almost there: you need a nominee.";
              note = "The nominee must be an Indian citizen and give written consent, filed with SPICe+.";
            } else {
              v.textContent = "You’re eligible to form an OPC.";
              note = resident ? "You count as resident in India for the OPC rules." : "As a non-resident Indian citizen, you can still form an OPC since April 2021.";
            }
            v.className = "result__verdict " + (ok ? "is-no" : "is-yes");
            document.getElementById("ec-out").innerHTML = [
              row("Indian citizen", citizen ? "Yes" : "No"),
              row("Residency (120 days)", citizen ? (resident ? "Resident" : "Non-resident, allowed") : "Not applicable"),
              row("Nominee", nominee ? "Agreed" : "Needed"),
              row("Eligible", ok ? "Yes" : "Not yet", true),
            ].join("");
            document.getElementById("ec-note").textContent = note;
          };
          ec.addEventListener("input", function () {
            trackUse("opc_eligibility");
            renderElig();
          });
          ec.addEventListener("change", renderElig);
          renderElig();
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
            var aoc = addDays(fyEnd, 180), mgt = new Date(fyEnd.getFullYear(), 10, 29);
            var v = document.getElementById("cc-verdict");
            v.textContent = "First financial year ends on " + dmy(fyEnd) + ".";
            v.className = "result__verdict is-no";
            document.getElementById("cc-out").innerHTML = [
              row("First auditor by", dmy(addDays(inc, 30))),
              row("Share certificate by", dmy(new Date(inc.getFullYear(), inc.getMonth() + 2, inc.getDate()))),
              row("INC-20A by", dmy(addDays(inc, 180))),
              row("AOC-4 by", dmy(aoc)),
              row("MGT-7A by", dmy(mgt), true),
            ].join("");
            document.getElementById("cc-note").textContent =
              (inc.getMonth() <= 2 ? "Incorporated between January and March, so the first financial year runs to 31 March of the following year. " : "") +
              "The income tax return and audit for the first year follow the same year end.";
          };
          cc.addEventListener("input", function () {
            trackUse("opc_calendar");
            renderCal();
          });
          cc.addEventListener("change", renderCal);
          renderCal();
        }
      })();
    </script>
