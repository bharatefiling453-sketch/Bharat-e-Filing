    <script>
      /* OPC compliance: live OPC compliance clock, OPC compliance planner, OPC late fee calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* OPC, FY ending 31 March of year Y+1: AOC-4 within 180 days (27 Sep, Section 137 proviso); MGT-7A within 60 days of 30 Sep (29 Nov, Section 92); ITR-6 21 Nov 2026 (CBDT Circular 7/2026) */
        var ITR6 = new Date(2026, 10, 21);
        function aocDue(fy) {
          return new Date(fy + 1, 8, 27);
        }
        function mgtDue(fy) {
          return new Date(fy + 1, 10, 29);
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
        function daysLate(due, on) {
          return Math.max(0, Math.round((on - due) / 86400000));
        }
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
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
          window.dataLayer.push({ event: "calculator_use", service: "opc-compliance", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live OPC compliance clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var list = [
            [aocDue(2025), "AOC-4 (financial statements) is due in"],
            [new Date(2026, 9, 31), "MSME-1 (Apr–Sep) is due in"],
            [ITR6, "ITR-6 is due in"],
            [mgtDue(2025), "MGT-7A (annual return) is due in"],
            [new Date(2027, 3, 30), "MSME-1 (Oct–Mar) is due in"],
            [new Date(2027, 5, 30), "DPT-3 is due in"],
            [aocDue(2026), "AOC-4 for FY 2026-27 is due in"],
          ];
          var next = list.filter(function (d) {
            return d[0] >= today;
          })[0] || list[list.length - 1];
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-next-label]", next[1]);
          setText("[data-next-date]", dmy(next[0]));
          var hero = today <= aocDue(2025) ? [aocDue(2025), "OPC AOC-4 is due by"] : [mgtDue(2025), "OPC annual return (MGT-7A) is due by"];
          setText("[data-hero-label]", hero[1]);
          setText("[data-hero-date]", dmy(hero[0]));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='next']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left: " + next[1].replace(/ in$/, ""));
          }
          setText("[data-aoc-label]", "AOC-4 was due on " + dmy(aocDue(2025)) + ". Additional fee so far");
          setText("[data-aoc-fee]", inr(daysLate(aocDue(2025), today) * 100));
          setText("[data-mgt-by]", dmy(mgtDue(2025)));
          setText("[data-itr-by]", dmy(ITR6));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- OPC compliance planner (Section 173(5): one meeting in each half-year, none with a sole director) ---- */
        var op = document.getElementById("opc-plan");
        if (op) {
          var renderPlan = function () {
            var sole = op.querySelector("[name='directors']:checked").value === "1";
            var on = function (n) {
              return op.querySelector("[name='" + n + "']").checked;
            };
            var v = document.getElementById("op-verdict");
            v.textContent = sole ? "Sole director: no board meetings needed." : "Hold two board meetings, at least 90 days apart.";
            v.className = "result__verdict is-no";
            var rows = [row("AGM", "Not required"), row("AOC-4", dmy(aocDue(2025))), row("ITR-6", dmy(ITR6)), row("MGT-7A", dmy(mgtDue(2025)))];
            if (on("msme")) rows.push(row("MSME-1", "31 Oct 2026 · 30 Apr 2027"));
            if (on("loans")) rows.push(row("DPT-3", "30 Jun 2027"));
            if (on("nominee")) rows.push(row("INC-4 (nominee)", "Within 30 days of change"));
            rows.push(row("Audit", "Required every year", true));
            document.getElementById("op-out").innerHTML = rows.join("");
            document.getElementById("op-note").textContent = sole
              ? "Decisions are recorded in the minute book and signed by the director (Section 122)."
              : "With two directors, minutes of both meetings are kept, and the director’s report is approved at one.";
          };
          op.addEventListener("change", function () {
            trackUse("opc_planner");
            renderPlan();
          });
          renderPlan();
        }

        /* ---- OPC late fee calculator (₹100 a day for each late AOC-4 and MGT-7A) ---- */
        var of = document.getElementById("opc-fee");
        if (of) {
          var aocIn = of.querySelector("[name='aoc']"), mgtIn = of.querySelector("[name='mgt']");
          aocIn.value = "2026-09-20";
          mgtIn.value = isoDate(new Date());
          var renderFee = function () {
            var fy = Number(of.querySelector("[name='fy']").value);
            var aoc = parse(aocIn.value), mgt = parse(mgtIn.value);
            if (!aoc || !mgt) return;
            var a = daysLate(aocDue(fy), aoc), m = daysLate(mgtDue(fy), mgt);
            var v = document.getElementById("of-verdict");
            v.textContent = a || m ? "Late fees: " + inr((a + m) * 100) + "." : "On time. No late fees.";
            v.className = "result__verdict " + (a || m ? "is-yes" : "is-no");
            document.getElementById("of-out").innerHTML = [
              row("AOC-4 · days late", dmy(aocDue(fy)) + " · " + a),
              row("MGT-7A · days late", dmy(mgtDue(fy)) + " · " + m),
              row("Total additional fees", inr((a + m) * 100), true),
            ].join("");
          };
          of.addEventListener("input", function () {
            trackUse("opc_late_fee");
            renderFee();
          });
          of.addEventListener("change", renderFee);
          renderFee();
        }
      })();
    </script>
