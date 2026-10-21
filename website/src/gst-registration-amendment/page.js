    <script>
      /* GST amendment: live amendment clock, core/non-core checker, amendment date planner (no dependencies) */
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
        /* Working days: Monday to Friday. Public holidays are not excluded (estimate). */
        function addWorkingDays(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth(), from.getDate());
          while (n > 0) {
            d.setDate(d.getDate() + 1);
            if (d.getDay() !== 0 && d.getDay() !== 6) n--;
          }
          return d;
        }
        function isoDate(d) {
          return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
        }
        function parse(v) {
          var p = (v || "").split("-");
          return p.length === 3 ? new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2])) : null;
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
          window.dataLayer.push({ event: "calculator_use", service: "gst-registration-amendment", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live amendment clock (Rule 19: apply within 15 days; officer decides within 15 working days) ---- */
        function tick() {
          var now = new Date();
          var applyBy = addDays(now, 15);
          var end = new Date(applyBy.getFullYear(), applyBy.getMonth(), applyBy.getDate(), 23, 59, 59);
          setText("[data-apply-by]", dmy(applyBy));
          setText("[data-officer-by]", dmy(addWorkingDays(now, 15)));
          var ms = end - now;
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='apply']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file REG-14 for a change made today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Core or non-core checker ---- */
        var CHANGES = {
          address: { type: "Core", form: "REG-14", approval: "Officer, within 15 working days", docs: "Address proof, rent agreement or consent letter", note: "Your GSTIN stays the same. The amended certificate shows the new address." },
          state: { type: "New registration", form: "REG-01 in the new state", approval: "New GSTIN for that state", docs: "PAN, Aadhaar, address proof in the new state", note: "A GSTIN is state-wise, so an amendment cannot move it. Keep or cancel the old one as needed." },
          additional: { type: "Core", form: "REG-14", approval: "Officer, within 15 working days", docs: "Address proof for the new place", note: "Branches and warehouses in the same state are added to your existing GSTIN." },
          partner: { type: "Core", form: "REG-14", approval: "Officer, within 15 working days", docs: "PAN, Aadhaar, photograph; amended deed or appointment proof", note: "If the change creates a new PAN (for example a proprietorship becoming a firm), you need a new registration instead." },
          name: { type: "Core", form: "REG-14", approval: "Officer, within 15 working days", docs: "Name-change certificate or amended deed; updated PAN", note: "Update the name with the Income Tax Department or Registrar first, then in GST." },
          contact: { type: "Non-core", form: "REG-14", approval: "OTP on the new mobile or email", docs: "Access to the new mobile and email", note: "Lost the old mobile or email? The change can be made through your jurisdictional officer." },
          bank: { type: "Non-core", form: "REG-14", approval: "None", docs: "Cancelled cheque or bank statement", note: "A registration must have a bank account (Rule 10A)." },
          hsn: { type: "Non-core", form: "REG-14", approval: "None", docs: "None", note: "Worth reviewing after the GST 2.0 rate changes of 22 September 2025." },
          signatory: { type: "Non-core", form: "REG-14", approval: "None", docs: "Authorisation letter or board resolution; PAN and photograph", note: "The new signatory signs future returns with their own DSC or EVC." },
          pan: { type: "New registration", form: "REG-01 under the new PAN", approval: "New GSTIN", docs: "Documents of the new entity", note: "A new PAN always means a new GSTIN. Credit can be transferred in ITC-02 where the law allows." },
        };
        var cc = document.getElementById("change-check");
        if (cc) {
          var renderChange = function () {
            var c = CHANGES[cc.querySelector("[name='change']").value];
            var v = document.getElementById("cc-verdict");
            v.textContent = c.type === "New registration" ? "You need a new registration." : c.type + " amendment";
            v.className = "result__verdict " + (c.type === "Non-core" ? "is-no" : "is-yes");
            document.getElementById("cc-out").innerHTML = [row("Form", c.form), row("Documents", c.docs), row("Approval", c.approval, true)].join("");
            document.getElementById("cc-note").textContent = c.note;
          };
          cc.addEventListener("change", function () {
            trackUse("core_noncore_checker");
            renderChange();
          });
          renderChange();
        }

        /* ---- Amendment date planner ---- */
        var ap = document.getElementById("amend-plan");
        if (ap) {
          var changedIn = ap.querySelector("[name='changed']"), filedIn = ap.querySelector("[name='filed']");
          var today = new Date();
          changedIn.value = isoDate(today);
          filedIn.value = isoDate(today);
          var renderPlan = function () {
            var changed = parse(changedIn.value), filed = parse(filedIn.value);
            if (!changed || !filed) return;
            var applyBy = addDays(changed, 15);
            var late = filed > applyBy;
            document.getElementById("ap-out").innerHTML = [
              row("File REG-14 by", dmy(applyBy)),
              row("Your filing", late ? "Late by " + Math.round((filed - applyBy) / 86400000) + " days" : "On time"),
              row("Officer decision due (core)", dmy(addWorkingDays(filed, 15)), true),
              row("If a query is raised, reply within", "7 working days of the query"),
            ].join("");
          };
          ap.addEventListener("input", function () {
            trackUse("amendment_date_planner");
            renderPlan();
          });
          ap.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
