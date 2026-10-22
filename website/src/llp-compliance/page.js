    <script>
      /* LLP compliance: live LLP compliance clock, LLP compliance checker, LLP late fee calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* LLP Act: Form 11 by 30 May (Section 35), Form 8 by 30 Oct (Section 34); ₹100 a day per late form (Rule 24); ITR-5 per Section 139 and CBDT Circular 7/2026 */
        var ITR = { nonAudit: new Date(2026, 7, 31), audit: new Date(2026, 10, 21) };
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
          window.dataLayer.push({ event: "calculator_use", service: "llp-compliance", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live LLP compliance clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var f8 = nextOn(today, 9, 30), f11 = nextOn(today, 4, 30);
          var list = [
            [f8, "Form 8 (statement of account and solvency) is due in", "LLP Form 8 is due by"],
            [ITR.audit, "Audit-case ITR-5 is due in", "Audit-case ITR-5 is due by"],
            [f11, "Form 11 (annual return) is due in", "LLP Form 11 is due by"],
          ].filter(function (d) {
            return d[0] >= today;
          }).sort(function (a, b) {
            return a[0] - b[0];
          });
          var next = list[0];
          var end = new Date(next[0].getFullYear(), next[0].getMonth(), next[0].getDate(), 23, 59, 59);
          setText("[data-next-label]", next[1]);
          setText("[data-next-date]", dmy(next[0]));
          var mca = f8 < f11 ? [f8, "LLP Form 8 is due by"] : [f11, "LLP Form 11 is due by"];
          setText("[data-hero-label]", mca[1]);
          setText("[data-hero-date]", dmy(mca[0]));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='next']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left: " + next[1]);
          }
          /* Most recent Form 11 due date that has passed */
          var lastF11 = new Date(today.getFullYear(), 4, 30);
          if (lastF11 > today) lastF11 = new Date(today.getFullYear() - 1, 4, 30);
          setText("[data-f11-label]", "Form 11 was due on " + dmy(lastF11) + ". Additional fee so far");
          setText("[data-f11-fee]", inr(daysLate(lastF11, today) * 100));
          setText("[data-f11-next]", dmy(f11));
          setText("[data-itr-by]", dmy(ITR.audit));
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- LLP compliance checker (LLP audit: turnover > ₹40 lakh or contribution > ₹25 lakh; Form 11 CS certificate: contribution > ₹50 lakh or turnover > ₹5 crore) ---- */
        var lc = document.getElementById("llp-check");
        if (lc) {
          var renderCheck = function () {
            var t = Math.max(0, Number(lc.querySelector("[name='turnover']").value) || 0);
            var c = Math.max(0, Number(lc.querySelector("[name='contribution']").value) || 0);
            var digital = lc.querySelector("[name='digital']").checked;
            var llpAudit = t > 4e6 || c > 2.5e6;
            var taxAudit = t > (digital ? 1e8 : 1e7);
            var csCert = c > 5e6 || t > 5e7;
            var small = c <= 2.5e6 && t <= 4e6;
            var v = document.getElementById("lc-verdict");
            v.textContent = llpAudit ? "Accounts must be audited under the LLP Act." : "No LLP Act audit needed this year.";
            v.className = "result__verdict " + (llpAudit ? "is-yes" : "is-no");
            document.getElementById("lc-out").innerHTML = [
              row("Small LLP", small ? "Yes" : "No"),
              row("Tax audit (44AB)", taxAudit ? "Required" : "Not required"),
              row("Form 11 certified by a CS", csCert ? "Required" : "Not required"),
              row("ITR-5 due", dmy(taxAudit ? ITR.audit : ITR.nonAudit)),
              row("Form 8 due", "30 Oct 2026", true),
            ].join("");
            document.getElementById("lc-note").textContent = llpAudit
              ? "Form 8 is filed with the audited accounts and certified by a practising professional."
              : "Form 8 is still filed, signed by two designated partners and certified by a practising professional.";
          };
          lc.addEventListener("input", function () {
            trackUse("llp_compliance_checker");
            renderCheck();
          });
          lc.addEventListener("change", renderCheck);
          renderCheck();
        }

        /* ---- LLP late fee calculator (₹100 a day for each late Form 11 and Form 8) ---- */
        var lf = document.getElementById("llp-fee");
        if (lf) {
          var f11In = lf.querySelector("[name='f11']"), f8In = lf.querySelector("[name='f8']");
          f11In.value = "2026-05-25";
          f8In.value = isoDate(new Date());
          var renderFee = function () {
            var fy = Number(lf.querySelector("[name='fy']").value);
            var f11 = parse(f11In.value), f8 = parse(f8In.value);
            if (!f11 || !f8) return;
            var due11 = new Date(fy + 1, 4, 30), due8 = new Date(fy + 1, 9, 30);
            var a = daysLate(due11, f11), b = daysLate(due8, f8);
            var v = document.getElementById("lf-verdict");
            v.textContent = a || b ? "Late fees: " + inr((a + b) * 100) + "." : "On time. No late fees.";
            v.className = "result__verdict " + (a || b ? "is-yes" : "is-no");
            document.getElementById("lf-out").innerHTML = [
              row("Form 11 · days late", dmy(due11) + " · " + a),
              row("Form 8 · days late", dmy(due8) + " · " + b),
              row("Total additional fees", inr((a + b) * 100), true),
            ].join("");
          };
          lf.addEventListener("input", function () {
            trackUse("llp_late_fee");
            renderFee();
          });
          lf.addEventListener("change", renderFee);
          renderFee();
        }
      })();
    </script>
