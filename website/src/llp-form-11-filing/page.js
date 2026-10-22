    <script>
      /* LLP Form 11: live Form 11 clock, late fee calculator, requirement checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Form 11 by 30 May, within 60 days of the year end (Section 35, Rule 25); ₹100 a day additional fee (Rule 24); Form 8 by 30 October (Section 34);
           Form 4 within 30 days of a partner change (Rule 22); CS certificate if contribution > ₹50 lakh or turnover > ₹5 crore;
           small LLP: contribution ≤ ₹25 lakh and turnover ≤ ₹40 lakh; LLP audit if turnover > ₹40 lakh or contribution > ₹25 lakh */
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
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
        }
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
        }
        function daysLate(due, on) {
          return Math.max(0, Math.round((on - due) / 86400000));
        }
        function fyLabel(y) {
          return y + "-" + String(y + 1).slice(2);
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
          window.dataLayer.push({ event: "calculator_use", service: "llp-form-11-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live Form 11 clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var next = new Date(today.getFullYear(), 4, 30);
          if (next < today) next = new Date(today.getFullYear() + 1, 4, 30);
          var last = new Date(next.getFullYear() - 1, 4, 30);
          var end = new Date(next.getFullYear(), 4, 30, 23, 59, 59);
          setText("[data-f11-by]", dmy(next));
          setText("[data-f11-label]", "Form 11 for FY " + fyLabel(next.getFullYear() - 1));
          setText("[data-late-label]", "Form 11 for FY " + fyLabel(last.getFullYear() - 1) + " was due on " + dmy(last) + ". Late fee so far");
          setText("[data-late-fee]", inr(daysLate(last, today) * 100));
          setText("[data-f4-by]", dmy(addDays(today, 30)));
          var f8 = new Date(today.getFullYear(), 9, 30);
          if (f8 < today) f8 = new Date(today.getFullYear() + 1, 9, 30);
          setText("[data-f8-by]", dmy(f8));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='f11']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next Form 11 due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Form 11 late fee calculator ---- */
        var fc = document.getElementById("fee-calc");
        if (fc) {
          var renderFee = function () {
            var fy = Number(fc.querySelector("[name='fy']").value);
            var d = parse(fc.querySelector("[name='filedon']").value);
            if (!d) return;
            var due = new Date(fy + 1, 4, 30), late = daysLate(due, d);
            var v = document.getElementById("fc-verdict");
            v.textContent = late ? "Late fee: " + inr(late * 100) + "." : "On time. No late fee.";
            v.className = "result__verdict " + (late ? "is-yes" : "is-no");
            document.getElementById("fc-out").innerHTML = [
              row("Due date", dmy(due)),
              row("Days late", String(late)),
              row("Additional fee", inr(late * 100), true),
            ].join("");
          };
          fc.addEventListener("input", function () {
            trackUse("form11_late_fee");
            renderFee();
          });
          fc.addEventListener("change", renderFee);
          renderFee();
        }

        /* ---- Form 11 requirement checker ---- */
        var rq = document.getElementById("req-check");
        if (rq) {
          var renderReq = function () {
            var c = Math.max(0, Number(rq.querySelector("[name='contribution']").value) || 0);
            var t = Math.max(0, Number(rq.querySelector("[name='turnover']").value) || 0);
            var changed = rq.querySelector("[name='changed']").checked, body = rq.querySelector("[name='bodycorp']").checked;
            var cs = c > 5e6 || t > 5e7, small = c <= 2.5e6 && t <= 4e6, audit = t > 4e6 || c > 2.5e6;
            var v = document.getElementById("rq-verdict");
            v.textContent = cs ? "Form 11 needs a CS certificate." : "A designated partner can sign alone.";
            v.className = "result__verdict " + (cs ? "is-yes" : "is-no");
            document.getElementById("rq-out").innerHTML = [
              row("Small LLP", small ? "Yes" : "No"),
              row("CS certificate", cs ? "Required" : "Not required"),
              row("LLP audit", audit ? "Required" : "Not needed"),
              row("Form 11 due", "30 May", true),
            ].join("");
            var notes = [];
            if (changed) notes.push("Check that Form 4 was filed within 30 days for each partner change.");
            if (body) notes.push("Give the company partner’s nominee details in Form 11.");
            document.getElementById("rq-note").textContent = notes.length ? notes.join(" ") : "Form 11 is filed every year, even with no business.";
          };
          rq.addEventListener("input", function () {
            trackUse("form11_requirements");
            renderReq();
          });
          rq.addEventListener("change", renderReq);
          renderReq();
        }
      })();
    </script>
