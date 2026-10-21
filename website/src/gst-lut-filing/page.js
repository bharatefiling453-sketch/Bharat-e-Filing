    <script>
      /* GST LUT: live export clock, LUT eligibility checker, export deadline planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        /* Same day of the month, n months later (clamped to the month's last day) */
        function addMonths(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth() + n, 1);
          var last = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
          d.setDate(Math.min(from.getDate(), last));
          return d;
        }
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function fyOf(d) {
          var y = d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1;
          return { y: y, start: new Date(y, 3, 1), end: new Date(y + 1, 2, 31, 23, 59, 59, 999), label: "FY " + y + "-" + String(y + 1).slice(2) };
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
          window.dataLayer.push({ event: "calculator_use", service: "gst-lut-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live export clock ---- */
        function tick() {
          var now = new Date();
          var fy = fyOf(now);
          var ms = fy.end - now;
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          setText("[data-fy-label]", fy.label);
          setText("[data-fy-start]", dmy(fy.start));
          setText("[data-fy-renew]", dmy(new Date(fy.y + 1, 3, 1)));
          setText("[data-lut-days]", parts[0] + " more days");
          var box = document.querySelector("[data-cd='fy']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left on the " + fy.label + " LUT");
          }
          var fb = document.querySelector("[data-fy-bar]");
          if (fb) fb.style.width = ((now - fy.start) / (fy.end - fy.start)) * 100 + "%";
          setText("[data-goods-by]", dmy(addMonths(now, 3)));
          setText("[data-services-by]", dmy(addMonths(now, 12)));
          setText("[data-refund-by]", dmy(addMonths(now, 24)));
          /* Section 50: 18% a year on ₹1 lakh of IGST, from the start of the financial year (illustration) */
          var interest = (100000 * 0.18 * (now - fy.start)) / (365 * 86400000);
          setText("[data-lut-int]", "₹" + interest.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
          var ib = document.querySelector("[data-int-bar]");
          if (ib) ib.style.width = Math.min(100, (interest / 18000) * 100) + "%";
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- LUT eligibility checker (Rule 96A; Notification 37/2017-CT) ---- */
        var lc = document.getElementById("lut-check");
        if (lc) {
          var renderCheck = function () {
            var kind = lc.querySelector("[name='kind']:checked").value;
            var registered = lc.querySelector("[name='registered']").checked;
            var prosecuted = lc.querySelector("[name='prosecuted']").checked;
            var lastyear = lc.querySelector("[name='lastyear']").checked;
            var verdict = document.getElementById("lc-verdict");
            var fy = fyOf(new Date());
            var rows = [], note = "", ok = false;
            if (!registered) {
              verdict.textContent = "Get a GSTIN first.";
              rows.push(row("Why", "The LUT is filed from your GST portal login", true));
              note = "We can register you and file the LUT together.";
            } else if (prosecuted) {
              verdict.textContent = "LUT not allowed. Export under a bond.";
              rows.push(row("Why", "Prosecuted for evasion of ₹2.5 crore or more", true));
              note = "A bond, usually backed by a bank guarantee, lets you export without paying IGST.";
            } else {
              ok = true;
              verdict.textContent = "Yes, you can file an LUT.";
              rows.push(row("Form", "GST RFD-11"));
              rows.push(row("Covers", fy.label + " (till " + dmy(fy.end) + ")"));
              rows.push(
                row(
                  "Your condition",
                  kind === "goods" ? "Export within 3 months of invoice" : kind === "services" ? "Payment within 1 year of invoice" : "SEZ unit/developer, authorised operations",
                  true,
                ),
              );
              note = lastyear
                ? "Last year’s LUT does not carry over. File a fresh one for " + fy.label + " before your next export invoice."
                : "File before your first zero-rated invoice of the year and quote the ARN on every invoice.";
            }
            verdict.className = "result__verdict " + (ok ? "is-no" : "is-yes");
            document.getElementById("lc-out").innerHTML = rows.join("");
            document.getElementById("lc-note").textContent = note;
          };
          lc.addEventListener("input", function () {
            trackUse("lut_eligibility_checker");
            renderCheck();
          });
          lc.addEventListener("change", renderCheck);
          renderCheck();
        }

        /* ---- Export deadline planner (Rule 96A; Section 54) ---- */
        var dp = document.getElementById("deadline-plan");
        if (dp) {
          var input = dp.querySelector("[name='date']");
          var t = new Date();
          input.value = t.getFullYear() + "-" + pad(t.getMonth() + 1) + "-" + pad(t.getDate());
          var renderPlan = function () {
            var p = (input.value || "").split("-");
            if (p.length < 3) return;
            var d = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
            var goods = dp.querySelector("[name='ptype']:checked").value === "goods";
            var deadline = goods ? addMonths(d, 3) : addMonths(d, 12);
            var fy = fyOf(d);
            document.getElementById("dp-out").innerHTML = [
              row(goods ? "Export the goods by" : "Receive payment by", dmy(deadline), true),
              row("If missed, pay IGST + 18% interest by", dmy(addDays(deadline, 15))),
              row("LUT needed for", fy.label + " (valid till " + dmy(fy.end) + ")"),
              row("Renew LUT for next year before", dmy(new Date(fy.y + 1, 3, 1))),
              row("Claim ITC refund (RFD-01) by, approx.", dmy(addMonths(d, 24))),
            ].join("");
          };
          dp.addEventListener("input", function () {
            trackUse("export_deadline_planner");
            renderPlan();
          });
          dp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
