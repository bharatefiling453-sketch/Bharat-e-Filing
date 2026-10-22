    <script>
      /* Company compliance: live compliance clock, compliance calendar planner, ROC late fee calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FY 2025-26: AGM by 30 Sep 2026 (Section 96); AOC-4 +30 days (Section 137); MGT-7 +60 days (Section 92); ITR-6 21 Nov 2026 (CBDT Circular 7/2026) */
        var AGM = new Date(2026, 8, 30), ITR6 = new Date(2026, 10, 21);
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
        function daysLate(due, on) {
          return Math.max(0, Math.round((on - due) / 86400000));
        }
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
        }
        /* Next occurrence of a month/day on or after today */
        function nextOn(today, m, d) {
          var x = new Date(today.getFullYear(), m, d);
          return x < today ? new Date(today.getFullYear() + 1, m, d) : x;
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
          window.dataLayer.push({ event: "calculator_use", service: "company-compliance", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live compliance clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var aoc = addDays(AGM, 30), mgt = addDays(AGM, 60);
          var msme = nextOn(today, 9, 31) < nextOn(today, 3, 30) ? nextOn(today, 9, 31) : nextOn(today, 3, 30);
          var list = [
            [aoc, "AOC-4 is due on"],
            [new Date(2026, 9, 31), "MSME-1 (Apr–Sep) is due on"],
            [ITR6, "Company ITR-6 is due on"],
            [mgt, "MGT-7 is due on"],
            [new Date(2027, 3, 30), "MSME-1 (Oct–Mar) is due on"],
            [new Date(2027, 5, 30), "DPT-3 is due on"],
            [new Date(2027, 8, 30), "The next AGM is due by"],
          ];
          var next = list.filter(function (d) {
            return d[0] >= today;
          })[0] || list[list.length - 1];
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-next-label]", next[1]);
          setText("[data-next-date]", dmy(next[0]));
          var roc = today <= aoc ? [aoc, "AOC-4 is due by"] : [mgt, "MGT-7 is due by"];
          setText("[data-hero-label]", roc[1]);
          setText("[data-hero-date]", dmy(roc[0]));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='next']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left: " + next[1] + " " + dmy(next[0]));
          }
          setText("[data-msme-by]", dmy(msme));
          setText("[data-msme-sub]", msme.getMonth() === 9 ? "For April to September." : "For October to March.");
          var late = daysLate(aoc, today) + daysLate(mgt, today);
          if (late) {
            setText("[data-roc-label]", "AGM on 30 September, forms still pending? Fees so far");
            setText("[data-roc-big]", inr(late * 100));
          }
          setText("[data-dpt-by]", dmy(nextOn(today, 5, 30)));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Compliance calendar planner ---- */
        var cp = document.getElementById("cal-plan");
        if (cp) {
          var agmIn = cp.querySelector("[name='agm']");
          var renderPlan = function () {
            var type = cp.querySelector("[name='type']").value;
            var opc = type === "opc";
            agmIn.disabled = opc;
            var agm = opc ? AGM : parse(agmIn.value);
            if (!agm) return;
            var lateAgm = !opc && agm > AGM;
            var v = document.getElementById("cp-verdict");
            v.textContent = lateAgm ? "AGM after 30 September needs an extension from the ROC." : "Your FY 2025-26 calendar is ready.";
            v.className = "result__verdict " + (lateAgm ? "is-yes" : "is-no");
            var rows = [row("Board meetings", type === "pvt" ? "4 a year, ≤120 days apart" : "2 a year, ≥90 days apart")];
            rows.push(row("AOC-4", opc ? dmy(new Date(2026, 8, 27)) + " (180 days)" : dmy(addDays(agm, 30))));
            rows.push(row(type === "pvt" ? "MGT-7" : "MGT-7A", dmy(addDays(agm, 60))));
            if (cp.querySelector("[name='auditor']").checked) rows.push(row("ADT-1", dmy(addDays(agm, 15))));
            if (cp.querySelector("[name='msme']").checked) rows.push(row("MSME-1", "31 Oct 2026 · 30 Apr 2027"));
            rows.push(row("DPT-3", "30 Jun 2027"));
            rows.push(row("ITR-6", dmy(ITR6), true));
            document.getElementById("cp-out").innerHTML = rows.join("");
            document.getElementById("cp-note").textContent = opc
              ? "An OPC holds no AGM. AOC-4 is due within 180 days of the year end; MGT-7A as for other companies."
              : type === "small"
                ? "Small company: capital up to ₹10 crore and turnover up to ₹100 crore, and not a holding, subsidiary or Section 8 company."
                : "DIR-3 KYC: once every three years by 30 June, for each director.";
          };
          cp.addEventListener("input", function () {
            trackUse("company_calendar_planner");
            renderPlan();
          });
          cp.addEventListener("change", renderPlan);
          renderPlan();
        }

        /* ---- ROC late fee calculator (₹100 a day for each late AOC-4 and MGT-7) ---- */
        var rf = document.getElementById("roc-fee");
        if (rf) {
          var aocIn = rf.querySelector("[name='aoc']"), mgtIn = rf.querySelector("[name='mgt']");
          aocIn.value = isoDate(new Date());
          mgtIn.value = isoDate(new Date());
          var renderFee = function () {
            var agm = parse(rf.querySelector("[name='agmdate']").value), aoc = parse(aocIn.value), mgt = parse(mgtIn.value);
            if (!agm || !aoc || !mgt) return;
            var aocDue = addDays(agm, 30), mgtDue = addDays(agm, 60);
            var a = daysLate(aocDue, aoc), m = daysLate(mgtDue, mgt);
            var v = document.getElementById("rf-verdict");
            v.textContent = a || m ? "Late fees: " + inr((a + m) * 100) + "." : "On time. No late fees.";
            v.className = "result__verdict " + (a || m ? "is-yes" : "is-no");
            document.getElementById("rf-out").innerHTML = [
              row("AOC-4 due · days late", dmy(aocDue) + " · " + a),
              row("MGT-7 due · days late", dmy(mgtDue) + " · " + m),
              row("Total additional fees", inr((a + m) * 100), true),
            ].join("");
          };
          rf.addEventListener("input", function () {
            trackUse("roc_late_fee");
            renderFee();
          });
          rf.addEventListener("change", renderFee);
          renderFee();
        }
      })();
    </script>
