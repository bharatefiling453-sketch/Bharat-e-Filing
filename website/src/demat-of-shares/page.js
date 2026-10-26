    <script>
      /* Demat of shares: live demat clock, Rule 9B applicability checker, demat journey planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Rule 9B: private companies other than small and Government companies; compliance date 30 June 2025 for companies not small on
           31 March 2023 (extended February 2025); 18 months from the end of the year in which a company ceases to be small; producer companies by
           31 March 2028. Small company from 1 December 2025: paid-up ≤ ₹10 crore and turnover ≤ ₹100 crore, not a holding or subsidiary.
           Rule 9A: unlisted public companies since 2 October 2018. PAS-6 within 60 days of each half-year (30 Sep → 29 Nov, 31 Mar → 30 May). */
        var RULE9B = new Date(2025, 5, 30);
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
        function nextPas6(from) {
          var y = from.getFullYear();
          var c = [new Date(y, 4, 30), new Date(y, 10, 29), new Date(y + 1, 4, 30)].filter(function (d) {
            return d >= from;
          });
          return c[0];
        }
        function firstPas6(isin) {
          var m = isin.getMonth(), y = isin.getFullYear();
          if (m >= 3 && m <= 8) return new Date(y, 10, 29);
          return new Date(m >= 9 ? y + 1 : y, 4, 30);
        }
        function lastFyEnd(from) {
          var y = from.getMonth() >= 3 ? from.getFullYear() : from.getFullYear() - 1;
          return new Date(y, 2, 31);
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
          window.dataLayer.push({ event: "calculator_use", service: "demat-of-shares", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live demat clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = nextPas6(today);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-pas6-by]", dmy(due));
          setText("[data-pas6-label]", "PAS-6 for the half-year to " + (due.getMonth() === 10 ? "30 Sep " + due.getFullYear() : "31 Mar " + due.getFullYear()));
          var fyEnd = lastFyEnd(today);
          setText("[data-ceased-label]", "Stopped being small in FY " + (fyEnd.getFullYear() - 1) + "-" + String(fyEnd.getFullYear()).slice(2) + "?");
          setText("[data-ceased-by]", dmy(new Date(fyEnd.getFullYear() + 1, 8, 30)));
          setText("[data-since-days]", String(Math.max(0, Math.round((today - RULE9B) / 86400000))).replace(/\B(?=(\d{3})+(?!\d))/g, ","));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='pas6']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next PAS-6 due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Rule 9B applicability checker ---- */
        var r9 = document.getElementById("rule9b");
        if (r9) {
          var renderR9 = function () {
            var type = r9.querySelector("[name='ctype']").value;
            var cap = Math.max(0, Number(r9.querySelector("[name='capital']").value) || 0);
            var turn = Math.max(0, Number(r9.querySelector("[name='turnover']").value) || 0);
            var since = Number(r9.querySelector("[name='since']").value);
            var group = r9.querySelector("[name='group']").checked;
            var today = day(new Date());
            var v = document.getElementById("r9-verdict"), rows = [], note = "";
            var small = cap <= 10 && turn <= 100 && !group;
            var applies, due, rule;
            if (type === "pub") {
              applies = true; rule = "Rule 9A"; due = new Date(2018, 9, 2);
              note = "Unlisted public companies have issued only demat securities since 2 October 2018.";
            } else if (type === "govt") {
              applies = false; rule = "Exempt";
              note = "Government companies are outside Rule 9B.";
            } else if (type === "producer") {
              applies = true; rule = "Rule 9B"; due = new Date(2028, 2, 31);
              note = "Producer companies have until 31 March 2028.";
            } else if (small) {
              applies = false; rule = "Small company";
              note = "Small companies are exempt. Recheck each year end against ₹10 crore capital and ₹100 crore turnover.";
            } else {
              applies = true; rule = "Rule 9B";
              due = since <= 2023 ? RULE9B : new Date(since + 1, 8, 30);
              note = since <= 2023 ? "The extended date for companies that were not small on 31 March 2023." : "Counted 18 months from the end of the year in which the company ceased to be small.";
            }
            if (applies) {
              var late = due < today;
              v.textContent = late ? "Demat applies, and the date has passed. Act now." : "Demat applies. Comply by " + dmy(due) + ".";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Demat isn’t mandatory for your company now.";
              v.className = "result__verdict is-no";
            }
            rows.push(row("Small company", type === "pvt" ? (small ? "Yes" : "No") : "Not applicable"));
            rows.push(row("Rule", rule));
            rows.push(row("PAS-6", applies ? "Every half-year" : "Not needed"));
            rows.push(row("Comply by", applies ? dmy(due) : "Not required", true));
            document.getElementById("r9-out").innerHTML = rows.join("");
            document.getElementById("r9-note").textContent = note;
          };
          r9.addEventListener("input", function () {
            trackUse("rule9b_checker");
            renderR9();
          });
          r9.addEventListener("change", renderR9);
          renderR9();
        }

        /* ---- Demat journey planner ---- */
        var dp = document.getElementById("demat-plan");
        if (dp) {
          var startIn = dp.querySelector("[name='startdate']");
          startIn.value = isoDate(new Date());
          var renderPlan = function () {
            var d = parse(startIn.value);
            if (!d) return;
            var accounts = dp.querySelector("[name='accounts']").checked;
            var isin = addDays(d, 30);
            var credits = addDays(isin, accounts ? 14 : 28);
            var v = document.getElementById("dp-verdict");
            v.textContent = "Shares credited by about " + dmy(credits) + ".";
            v.className = "result__verdict is-no";
            document.getElementById("dp-out").innerHTML = [
              row("Agreements signed (target)", dmy(addDays(d, 14))),
              row("ISIN active (target)", dmy(isin)),
              row("First PAS-6 by", dmy(firstPas6(isin))),
              row("Holders credited (target)", dmy(credits), true),
            ].join("");
          };
          dp.addEventListener("input", function () {
            trackUse("demat_planner");
            renderPlan();
          });
          dp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
