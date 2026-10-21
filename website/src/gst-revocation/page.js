    <script>
      /* GST revocation: live revocation clock, revocation checker, deadline planner (no dependencies) */
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
          window.dataLayer.push({ event: "calculator_use", service: "gst-revocation", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live revocation clock (Rule 23: 90 days, +180 days extension; gap returns within 30 days of REG-22) ---- */
        function tick() {
          var now = new Date();
          var by = addDays(now, 90);
          var end = new Date(by.getFullYear(), by.getMonth(), by.getDate(), 23, 59, 59);
          setText("[data-reg21-by]", dmy(by));
          setText("[data-ext-by]", dmy(addDays(now, 270)));
          setText("[data-gap-by]", dmy(addDays(now, 30)));
          setText("[data-barred-before]", dmy(new Date(now.getFullYear() - 3, now.getMonth(), now.getDate())));
          var ms = end - now;
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='reg21']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to apply in REG-21 for an order served today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Revocation checker ---- */
        var rc = document.getElementById("revoke-check");
        if (rc) {
          var renderCheck = function () {
            var who = rc.querySelector("[name='who']:checked").value;
            var days = Math.max(0, parseInt(rc.querySelector("[name='days']").value, 10) || 0);
            var pending = rc.querySelector("[name='pending']").checked;
            var barred = rc.querySelector("[name='barred']").checked;
            var v = document.getElementById("rc-verdict"), rows = [], note = "", good = false;
            if (who === "self") {
              v.textContent = "Revocation doesn’t apply. Register afresh.";
              rows.push(row("Why", "Section 30 covers only officer-cancelled registrations", true));
              note = "We can file a fresh registration and settle any dues on the old GSTIN.";
            } else if (days <= 90) {
              good = !barred;
              v.textContent = barred ? "Within time, but a return is time-barred." : "Yes, you can apply in REG-21.";
              rows.push(row("Days left to apply", String(90 - days)));
              rows.push(row("Before applying", pending ? "File pending returns and pay dues" : "Nothing pending", true));
              note = barred
                ? "A time-barred return can’t be filed, so the usual condition can’t be met. We’ll advise on appeal or other remedies."
                : "Apply early: the officer decides within 30 days of your application.";
            } else if (days <= 270) {
              v.textContent = "Ask for an extension first.";
              rows.push(row("Extension window left", String(270 - days) + " days"));
              rows.push(row("Who decides", "Commissioner or Joint/Additional Commissioner", true));
              note = days <= 120 ? "You may also still be within time to appeal in APL-01 (3 months + 1 month)." : "Show sufficient cause in writing, with evidence.";
            } else {
              v.textContent = "Revocation window has closed.";
              rows.push(row("Options", "Appeal if within time, High Court writ, or fresh registration", true));
              note = "Every case is different. Talk to us before you register afresh.";
            }
            v.className = "result__verdict " + (good ? "is-no" : "is-yes");
            document.getElementById("rc-out").innerHTML = rows.join("");
            document.getElementById("rc-note").textContent = note;
          };
          rc.addEventListener("input", function () {
            trackUse("revocation_checker");
            renderCheck();
          });
          rc.addEventListener("change", renderCheck);
          renderCheck();
        }

        /* ---- Revocation deadline planner ---- */
        var rp = document.getElementById("revoke-plan");
        if (rp) {
          var input = rp.querySelector("[name='date']");
          var t = new Date();
          input.value = t.getFullYear() + "-" + pad(t.getMonth() + 1) + "-" + pad(t.getDate());
          var renderPlan = function () {
            var p = (input.value || "").split("-");
            if (p.length < 3) return;
            var d = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
            document.getElementById("rp-out").innerHTML = [
              row("Apply in REG-21 by", dmy(addDays(d, 90)), true),
              row("With the Commissioner’s extension, by", dmy(addDays(d, 270))),
              row("Appeal in APL-01 by", dmy(addMonths(d, 3))),
              row("Appeal with condonation (1 month), by", dmy(addMonths(d, 4))),
            ].join("");
          };
          rp.addEventListener("input", function () {
            trackUse("revocation_deadline_planner");
            renderPlan();
          });
          rp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
