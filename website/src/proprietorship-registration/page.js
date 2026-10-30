    <script>
      /* Proprietorship: live tax dates, registrations checker, presumptive income estimator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Advance tax under the Income-tax Act, 2025: 15 June, 15 September, 15 December and 15 March (presumptive taxpayers by 15 March).
           GST registration threshold: ₹40 lakh for goods and ₹20 lakh for services in most states (₹20 lakh and ₹10 lakh in some special category
           states); interstate supply of goods needs registration regardless of turnover. Section 58 (formerly 44AD/44ADA): business 8% of turnover or
           6% of digital receipts, turnover up to ₹2 crore (₹3 crore if cash receipts are within 5%); specified professions 50% of receipts, up to
           ₹50 lakh (₹75 lakh if cash receipts are within 5%). */
        var STEPS = [[6, 15, "1st"], [9, 15, "2nd"], [12, 15, "3rd"], [3, 15, "4th"]];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function fyStart(d) {
          return d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1;
        }
        function lakh(n) {
          if (n >= 100) return "₹" + (Math.round(n) / 100).toLocaleString("en-IN") + " crore";
          return "₹" + (Math.round(n * 100) / 100).toLocaleString("en-IN") + " lakh";
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
          window.dataLayer.push({ event: "calculator_use", service: "proprietorship-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live tax dates ---- */
        function tick() {
          var now = new Date(), today = day(now), fy = fyStart(today);
          var list = [];
          [fy, fy + 1].forEach(function (y) {
            STEPS.forEach(function (s) {
              list.push({ d: new Date(s[0] === 3 ? y + 1 : y, s[0] - 1, s[1]), n: s[2] });
            });
          });
          var next = list.filter(function (x) {
            return x.d >= today;
          })[0];
          var end = new Date(next.d.getFullYear(), next.d.getMonth(), next.d.getDate(), 23, 59, 59);
          setText("[data-adv-due]", dmy(next.d));
          setText("[data-adv-label]", "The " + next.n + " advance tax instalment is due in");
          setText("[data-adv-last]", dmy(new Date(fy + 1, 2, 15)));
          var gst = new Date(today.getFullYear(), today.getMonth(), 20);
          if (gst < today) gst = new Date(today.getFullYear(), today.getMonth() + 1, 20);
          var gm = new Date(gst.getFullYear(), gst.getMonth() - 1, 1);
          setText("[data-gst-by]", dmy(gst));
          setText("[data-gst-label]", "GSTR-3B for " + MONTHS[gm.getMonth()] + " " + gm.getFullYear() + " is due by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='advtax']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next advance tax instalment");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Registrations checker ---- */
        var rc = document.getElementById("reg-check");
        if (rc) {
          var renderReg = function () {
            var supply = rc.querySelector("[name='supply']").value;
            var turnover = Math.max(0, Number(rc.querySelector("[name='turnover']").value) || 0);
            var special = rc.querySelector("[name='special']").checked, inter = rc.querySelector("[name='interstate']").checked;
            var premises = rc.querySelector("[name='premises']").checked, exim = rc.querySelector("[name='exim']").checked;
            var limit = supply === "goods" ? (special ? 20 : 40) : special ? 10 : 20;
            var gstNeeded = turnover > limit || (inter && supply === "goods");
            var rows = [], count = 1;
            rows.push(row("GST", gstNeeded ? "Required" : "Not yet (limit " + lakh(limit) + ")"));
            if (gstNeeded) count++;
            rows.push(row("Udyam", "Recommended"));
            count++;
            rows.push(row("Shop Act", premises ? "As your state requires" : "Usually not, without premises"));
            if (premises) count++;
            if (exim) {
              rows.push(row("IEC", "Required"));
              count++;
            }
            rows.push(row("Current account", "Two proofs of business", true));
            var v = document.getElementById("rc-verdict");
            v.textContent = "About " + count + " registrations for your proprietorship.";
            v.className = "result__verdict " + (gstNeeded ? "is-yes" : "is-no");
            document.getElementById("rc-note").textContent = gstNeeded
              ? inter && supply === "goods" && turnover <= limit
                ? "Selling goods to other states needs GST registration regardless of turnover."
                : "Your turnover is above the GST threshold, so register before crossing it."
              : "Below the GST threshold you can register voluntarily, for example to claim input tax credit or sell to businesses that want GST invoices.";
            document.getElementById("rc-out").innerHTML = rows.join("");
          };
          rc.addEventListener("input", function () {
            trackUse("proprietor_regs");
            renderReg();
          });
          rc.addEventListener("change", renderReg);
          renderReg();
        }

        /* ---- Presumptive income estimator ---- */
        var pt = document.getElementById("presumptive-calc");
        if (pt) {
          var renderPt = function () {
            var kind = pt.querySelector("[name='kind']").value;
            var t = Math.max(0, Number(pt.querySelector("[name='receipts']").value) || 0);
            var dig = Math.min(100, Math.max(0, Number(pt.querySelector("[name='digital']").value) || 0));
            var cashOk = 100 - dig <= 5;
            var cap = kind === "business" ? (cashOk ? 300 : 200) : cashOk ? 75 : 50;
            var v = document.getElementById("pt-verdict"), rows = [], note;
            if (t > cap) {
              v.textContent = "Above the presumptive limit of " + lakh(cap) + ".";
              v.className = "result__verdict is-yes";
              rows.push(row("Limit", lakh(cap)));
              rows.push(row("Presumptive tax", "Not available", true));
              note = "Keep regular books and declare actual profit. A tax audit may apply under section 63.";
            } else {
              var income = kind === "business" ? (t * dig) / 100 * 0.06 + (t * (100 - dig)) / 100 * 0.08 : t * 0.5;
              v.textContent = "Eligible. Minimum profit to declare: about " + lakh(income) + ".";
              v.className = "result__verdict is-no";
              rows.push(row("Limit", lakh(cap)));
              rows.push(row("Rate", kind === "business" ? "6% digital, 8% other" : "50% of receipts"));
              rows.push(row("Deemed profit", lakh(income), true));
              note = kind === "business"
                ? "You can declare more than this. Advance tax is due in full by 15 March."
                : "Applies to specified professions such as legal, medical, engineering, architecture, accountancy and interior decoration. Advance tax is due by 15 March.";
            }
            document.getElementById("pt-out").innerHTML = rows.join("");
            document.getElementById("pt-note").textContent = note;
          };
          pt.addEventListener("input", function () {
            trackUse("presumptive");
            renderPt();
          });
          pt.addEventListener("change", renderPt);
          renderPt();
        }
      })();
    </script>
