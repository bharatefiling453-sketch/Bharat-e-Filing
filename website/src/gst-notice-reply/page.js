    <script>
      /* GST Notice Reply: live notice clock, notice identifier, reply deadline planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function addMonths(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth() + n, 1);
          var last = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
          d.setDate(Math.min(from.getDate(), last));
          return d;
        }
        /* Working days: Monday to Friday. Public holidays are not excluded (estimate). */
        function addWorkingDays(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth(), from.getDate());
          while (n > 0) {
            d.setDate(d.getDate() + 1);
            if (d.getDay() !== 0 && d.getDay() !== 6) n--;
          }
          return d;
        }
        function fyStart(d) {
          return new Date(d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1, 3, 1);
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
          window.dataLayer.push({ event: "calculator_use", service: "gst-notice-reply", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live notice clock ---- */
        /* Section 74A for FY 2024-25: 42 months from the GSTR-9 due date (31 Dec 2025) = 30 Jun 2029 */
        var S74A_FROM = new Date(2025, 11, 31, 23, 59, 59), S74A_END = new Date(2029, 5, 30, 23, 59, 59);
        function tick() {
          var now = new Date();
          setText("[data-reply-30]", dmy(addDays(now, 30)));
          setText("[data-reply-7]", dmy(addDays(now, 7)));
          setText("[data-reply-7w]", dmy(addWorkingDays(now, 7)));
          setText("[data-appeal-by]", dmy(addMonths(now, 3)));
          var ms = Math.max(0, S74A_END - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='s74a']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = i === 0 ? String(v) : pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days left for Section 74A notices on FY 2024-25");
          }
          var sb = document.querySelector("[data-s74a-bar]");
          if (sb) sb.style.width = Math.min(100, Math.max(0, ((now - S74A_FROM) / (S74A_END - S74A_FROM)) * 100)) + "%";
          var start = fyStart(now);
          setText("[data-fy-start]", dmy(start));
          /* Section 50: 18% a year on ₹1 lakh of tax from the start of the financial year (illustration) */
          var interest = (100000 * 0.18 * (now - start)) / (365 * 86400000);
          setText("[data-notice-int]", "₹" + interest.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
          var ib = document.querySelector("[data-int-bar]");
          if (ib) ib.style.width = Math.min(100, (interest / 18000) * 100) + "%";
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Notice identifier ---- */
        var NOTICES = {
          "ASMT-10": { what: "Scrutiny of your returns", law: "Section 61, Rule 99", reply: "ASMT-11", time: "30 days", risk: "Medium", note: "Explain each difference with documents, or pay with interest in DRC-03. If not accepted, a show cause notice can follow." },
          "DRC-01A": { what: "Intimation of tax before a show cause notice", law: "Rule 142(1A)", reply: "DRC-01A Part B, or pay in DRC-03", time: "As stated in the intimation", risk: "Medium", note: "Your chance to settle or disagree before a formal show cause notice." },
          "DRC-01": { what: "Show cause notice for tax, interest and penalty", law: "Section 73, 74 or 74A", reply: "DRC-06", time: "As stated, often 30 days", risk: "High", note: "Ask for a personal hearing. In non-fraud 74A cases, paying tax and interest within 60 days means no penalty." },
          "DRC-01B": { what: "Tax in GSTR-1 higher than paid in GSTR-3B", law: "Rule 88C", reply: "Part B, or pay in DRC-03", time: "7 days", risk: "Medium", note: "If you don’t respond in 7 days, your next GSTR-1 is blocked." },
          "DRC-01C": { what: "ITC in GSTR-3B higher than GSTR-2B", law: "Rule 88D", reply: "Part B, or pay/reverse in DRC-03", time: "7 days", risk: "Medium", note: "If you don’t respond in 7 days, your next GSTR-1 is blocked." },
          "GSTR-3A": { what: "A return has not been filed", law: "Section 46", reply: "File the pending return", time: "15 days", risk: "Medium", note: "Otherwise the officer can assess your tax on best judgment under Section 62." },
          "REG-17": { what: "Proposed cancellation of your registration", law: "Section 29, Rule 22", reply: "REG-18", time: "7 working days", risk: "High", note: "Registration can be suspended meanwhile. If cancelled, you can apply for revocation." },
          "REG-03": { what: "Query on your new registration application", law: "Rule 9", reply: "REG-04", time: "7 working days", risk: "Low", note: "Unanswered queries lead to rejection of the application." },
          "ADT-01": { what: "Audit of your records by tax authorities", law: "Section 65", reply: "Produce books and records", time: "On the audit date given", risk: "Medium", note: "You get at least 15 working days’ notice. Keep reconciliations ready." },
          "DRC-07": { what: "Summary of a demand order", law: "Section 73, 74 or 74A", reply: "Appeal in APL-01", time: "3 months (+1 month for cause)", risk: "High", note: "Pay the admitted tax and a 10% pre-deposit of the disputed tax to file the appeal." },
        };
        var nc = document.getElementById("notice-check");
        if (nc) {
          var renderNotice = function () {
            var k = nc.querySelector("[name='form']").value, n = NOTICES[k];
            var v = document.getElementById("nc-verdict");
            v.textContent = k + ": " + n.what;
            v.className = "result__verdict " + (n.risk === "Low" ? "is-no" : "is-yes");
            document.getElementById("nc-out").innerHTML = [row("Law", n.law), row("Reply in", n.reply), row("Risk", n.risk), row("Time to reply", n.time, true)].join("");
            document.getElementById("nc-note").textContent = n.note;
          };
          nc.addEventListener("change", function () {
            trackUse("notice_identifier");
            renderNotice();
          });
          renderNotice();
        }

        /* ---- Reply deadline planner ---- */
        var rp = document.getElementById("reply-plan");
        if (rp) {
          var input = rp.querySelector("[name='date']");
          var t = new Date();
          input.value = t.getFullYear() + "-" + pad(t.getMonth() + 1) + "-" + pad(t.getDate());
          var renderPlan = function () {
            var p = (input.value || "").split("-");
            if (p.length < 3) return;
            var d = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
            var f = rp.querySelector("[name='rform']").value;
            var rows = [];
            if (f === "ASMT-10") rows.push(row("Reply in ASMT-11 by", dmy(addDays(d, 30)), true));
            if (f === "DRC-01") {
              rows.push(row("Reply in DRC-06 by (typical)", dmy(addDays(d, 30)), true));
              rows.push(row("Pay tax + interest, no penalty (non-fraud), by", dmy(addDays(d, 60))));
              rows.push(row("Order due by (12 months)", dmy(addMonths(d, 12))));
            }
            if (f === "DRC-01B" || f === "DRC-01C") rows.push(row("Reply in Part B or pay by", dmy(addDays(d, 7)), true));
            if (f === "GSTR-3A") rows.push(row("File the pending return by", dmy(addDays(d, 15)), true));
            if (f === "REG-17") rows.push(row("Reply in REG-18 by", dmy(addWorkingDays(d, 7)), true));
            if (f === "DRC-07") {
              rows.push(row("File appeal in APL-01 by", dmy(addMonths(d, 3)), true));
              rows.push(row("Latest with condonation (1 month)", dmy(addMonths(d, 4))));
              rows.push(row("Pay tax + interest, 10% penalty (non-fraud 74A), by", dmy(addDays(d, 60))));
            }
            document.getElementById("rp-out").innerHTML = rows.join("");
          };
          rp.addEventListener("input", function () {
            trackUse("reply_deadline_planner");
            renderPlan();
          });
          rp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
