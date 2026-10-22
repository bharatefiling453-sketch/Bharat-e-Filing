    <script>
      /* Income tax notice: live notice clock, notice checker, demand & penalty estimator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function isoDate(d) {
          return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
        }
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
        }
        /* Months or part of a month after a date (Section 220(2) interest) */
        function monthsOrPart(from, to) {
          if (to <= from) return 0;
          var n = (to.getFullYear() - from.getFullYear()) * 12 + to.getMonth() - from.getMonth();
          return to.getDate() > from.getDate() ? n + 1 : Math.max(n, 1);
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
          window.dataLayer.push({ event: "calculator_use", service: "income-tax-notice", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live notice clock (139(9): 15 days; 143(1)(a), 245, 156: 30 days; 143(2): three months from end of the FY of filing) ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var r15 = addDays(today, 15);
          var end = new Date(r15.getFullYear(), r15.getMonth(), r15.getDate(), 23, 59, 59);
          setText("[data-r15]", dmy(r15));
          setText("[data-r30]", dmy(addDays(today, 30)));
          setText("[data-r30b]", dmy(addDays(today, 30)));
          var fyEnd = today.getMonth() >= 3 ? today.getFullYear() + 1 : today.getFullYear();
          setText("[data-scrutiny]", dmy(new Date(fyEnd, 5, 30)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='r15']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to fix a defective return notice received today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Notice checker ---- */
        var NOTICES = {
          "1431a": { name: "Proposed adjustment", days: 30, risk: "Low", how: "Agree or disagree under e-Proceedings", note: "Usually a mismatch with AIS or Form 26AS. If you don’t respond, the adjustment is made and a demand follows." },
          "1399": { name: "Defective return", days: 15, risk: "Medium", how: "File a corrected return in response", note: "If the defect is not fixed in time, the return is treated as invalid, as if never filed." },
          "1431": { name: "Intimation after processing", days: 30, risk: "Low", how: "Pay, or file rectification under Section 154", note: "Check the demand line by line. Missed TDS credit and wrong regime are common causes." },
          "1432": { name: "Scrutiny assessment", days: 0, risk: "High", how: "Faceless submissions under e-Proceedings", note: "Reply by the date in the notice, issue by issue, with evidence. A video hearing can be requested." },
          "1421": { name: "Enquiry before assessment", days: 0, risk: "High", how: "Upload information under e-Proceedings", note: "Not complying can lead to a best judgement assessment and a ₹10,000 penalty." },
          "148a": { name: "Reassessment show cause", days: 0, risk: "High", how: "Reply with evidence under e-Proceedings", note: "First check the time limit: 3 years from the end of the assessment year, 5 if escaped income is ₹50 lakh or more." },
          "156": { name: "Demand notice", days: 30, risk: "Medium", how: "Pay, or disagree with the demand on the portal", note: "Interest of 1% a month runs after 30 days. Seek a stay if you appeal." },
          "245": { name: "Refund adjustment", days: 30, risk: "Low", how: "Agree, disagree or partly agree online", note: "If the old demand is wrong, disagree with reasons, or the refund is set off." },
          "270a": { name: "Penalty proceedings", days: 0, risk: "High", how: "Reply to the show cause notice", note: "50% of tax for under-reporting, 200% for misreporting. Immunity may be possible under Section 270AA." },
        };
        var nc = document.getElementById("notice-check");
        if (nc) {
          var dateIn = nc.querySelector("[name='date']");
          dateIn.value = isoDate(new Date());
          var renderNotice = function () {
            var n = NOTICES[nc.querySelector("[name='type']").value], got = parse(dateIn.value);
            if (!got) return;
            var v = document.getElementById("nc-verdict");
            v.textContent = n.name + " · risk: " + n.risk.toLowerCase() + ".";
            v.className = "result__verdict " + (n.risk === "Low" ? "is-no" : "is-yes");
            document.getElementById("nc-out").innerHTML = [
              row("How to respond", n.how),
              row("Reply by", n.days ? dmy(addDays(got, n.days)) : "Date given in the notice", true),
            ].join("");
            document.getElementById("nc-note").textContent = n.note;
          };
          nc.addEventListener("input", function () {
            trackUse("it_notice_checker");
            renderNotice();
          });
          nc.addEventListener("change", renderNotice);
          renderNotice();
        }

        /* ---- Demand & penalty estimator (Section 220(2): 1% a month after 30 days; Section 270A: 50% / 200%) ---- */
        var dc = document.getElementById("demand-calc");
        if (dc) {
          var paidIn = dc.querySelector("[name='paid']");
          paidIn.value = isoDate(new Date());
          var renderDemand = function () {
            var demand = Math.max(0, Number(dc.querySelector("[name='demand']").value) || 0);
            var served = parse(dc.querySelector("[name='served']").value), paid = parse(paidIn.value);
            if (!served || !paid) return;
            var due = addDays(served, 30);
            var months = monthsOrPart(due, paid);
            var interest = demand * 0.01 * months;
            var mis = dc.querySelector("[name='misreport']").checked, under = dc.querySelector("[name='penalty']").checked;
            var penalty = mis ? demand * 2 : under ? demand * 0.5 : 0;
            var v = document.getElementById("dc-verdict");
            v.textContent = months ? "Paying late: " + inr(interest) + " interest so far." : "Within 30 days. No interest yet.";
            v.className = "result__verdict " + (months ? "is-yes" : "is-no");
            document.getElementById("dc-out").innerHTML = [
              row("Pay or dispute by", dmy(due)),
              row("Interest (" + months + " month" + (months === 1 ? "" : "s") + " at 1%)", inr(interest)),
              row("Possible penalty on this tax", penalty ? inr(penalty) + (mis ? " (200%)" : " (50%)") : "None selected"),
              row("Total if all applies", inr(demand + interest + penalty), true),
            ].join("");
          };
          dc.addEventListener("input", function () {
            trackUse("it_demand_estimator");
            renderDemand();
          });
          dc.addEventListener("change", renderDemand);
          renderDemand();
        }
      })();
    </script>
