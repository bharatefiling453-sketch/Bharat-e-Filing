    <script>
      /* Section 8 company: live calendar, eligibility checker, first-year compliance calendar (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Companies Act, 2013: section 8 licence for charitable objects; income applied to the objects, no dividends (section 8(1)).
           Private: 2 to 200 members, at least 2 directors; public: at least 7 members and 3 directors (sections 3(1), 2(68), 149(1)).
           One director resident 182 days in the financial year (section 149(3)). First auditor within 30 days (section 139(6));
           share certificates within two months (section 56(4)(a)); INC-20A within 180 days for a company with share capital (section 10A).
           First financial year of a company incorporated on or after 1 January ends on 31 March of the following year (section 2(41));
           first AGM within nine months of that year end (section 96(1)); AOC-4 within 30 days and MGT-7 within 60 days of the AGM
           (sections 137 and 92(4)). A Section 8 company is not a small company (section 2(85)), so MGT-7A does not apply. Board meetings:
           at least one in every six calendar months (exemption notification G.S.R. 466(E), 5 June 2015). */
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
          window.dataLayer.push({ event: "calculator_use", service: "section-8-company-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live Section 8 calendar ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var aud = addDays(today, 30);
          var end = new Date(aud.getFullYear(), aud.getMonth(), aud.getDate(), 23, 59, 59);
          setText("[data-aud-by]", dmy(aud));
          setText("[data-inc20a]", dmy(addDays(today, 180)));
          setText("[data-agm-by]", dmy(new Date(firstYearEnd(today).getFullYear(), 11, 31)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='aud']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours to appoint the first auditor for a company incorporated today");
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
            var pub = ec.querySelector("[name='ctype']").value === "public";
            var d = Math.max(0, Math.round(Number(ec.querySelector("[name='directors']").value) || 0));
            var m = Math.max(0, Math.round(Number(ec.querySelector("[name='members']").value) || 0));
            var objects = ec.querySelector("[name='objects']").checked, res = ec.querySelector("[name='resident']").checked;
            var dividend = ec.querySelector("[name='dividend']").checked;
            var minD = pub ? 3 : 2, minM = pub ? 7 : 2;
            var issues = [];
            if (!objects) issues.push("Section 8 needs objects such as education, charity, health, sports, art, science, social welfare or the environment.");
            if (dividend) issues.push("A Section 8 company cannot pay dividends. If members expect profits, a private limited company fits better.");
            if (d < minD) issues.push("A " + (pub ? "public" : "private") + " Section 8 company needs at least " + minD + " directors.");
            if (m < minM) issues.push("A " + (pub ? "public" : "private") + " Section 8 company needs at least " + minM + " members.");
            if (!pub && m > 200) issues.push("A private company can have at most 200 members. Form it as a public company instead.");
            if (!res) issues.push("At least one director must stay in India for 182 days or more in the financial year.");
            var v = document.getElementById("el-verdict");
            if (issues.length) {
              v.textContent = issues.length + (issues.length === 1 ? " thing" : " things") + " to fix before filing.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Your plan fits a Section 8 company.";
              v.className = "result__verdict is-no";
            }
            var mOk = m >= minM && (pub || m <= 200);
            document.getElementById("el-out").innerHTML = [
              row("Objects", objects ? "Charitable ✓" : "Not eligible"),
              row("Directors", d + (d >= minD ? " ✓" : " (min " + minD + ")")),
              row("Members", m + (mOk ? " ✓" : m < minM ? " (min " + minM + ")" : " (max 200)")),
              row("Dividends", dividend ? "Not allowed" : "None ✓"),
              row("Ready for SPICe+", issues.length ? "Not yet" : "Yes", true),
            ].join("");
            document.getElementById("el-note").textContent = issues.length
              ? issues[0]
              : "Directors can be paid reasonable remuneration for services actually rendered. Each director needs a DIN, which can be allotted through SPICe+.";
          };
          ec.addEventListener("input", function () {
            trackUse("s8_eligibility");
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
            var capital = cc.querySelector("[name='capital']").checked;
            var fyEnd = firstYearEnd(inc);
            var agm = new Date(fyEnd.getFullYear(), 11, 31);
            var v = document.getElementById("cc-verdict");
            v.textContent = "First financial year ends on " + dmy(fyEnd) + ".";
            v.className = "result__verdict is-no";
            var rows = [row("First auditor by", dmy(addDays(inc, 30)))];
            if (capital) {
              rows.push(row("Share certificate by", dmy(new Date(inc.getFullYear(), inc.getMonth() + 2, inc.getDate()))));
              rows.push(row("INC-20A by", dmy(addDays(inc, 180))));
            }
            rows.push(row("First AGM by", dmy(agm)), row("AOC-4 by", dmy(addDays(agm, 30))), row("MGT-7 by", dmy(addDays(agm, 60)), true));
            document.getElementById("cc-out").innerHTML = rows.join("");
            document.getElementById("cc-note").textContent =
              (inc.getMonth() <= 2 ? "Incorporated between January and March, so the first financial year runs to 31 March of the following year. " : "") +
              (capital ? "" : "Without share capital, INC-20A and share certificates don’t apply. ") +
              "Hold at least one board meeting in every six calendar months.";
          };
          cc.addEventListener("input", function () {
            trackUse("s8_calendar");
            renderCal();
          });
          cc.addEventListener("change", renderCal);
          renderCal();
        }
      })();
    </script>
