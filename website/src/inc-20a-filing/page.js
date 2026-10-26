    <script>
      /* INC-20A: live new-company clock, due date and penalty calculator, readiness checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Section 10A: companies with share capital incorporated on or after 2 November 2018 file INC-20A within 180 days of incorporation;
           penalty ₹50,000 on the company and ₹1,000 a day per officer in default up to ₹1,00,000; Section 446B halves penalties for small
           companies, OPCs, producer companies and startups. First board meeting within 30 days (Section 173(1)), first auditor within 30 days
           (Section 139(6)), share certificates within two months (Section 56(4)(a)). */
        var START = new Date(2018, 10, 2);
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
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
        }
        function daysBetween(a, b) {
          return Math.round((b - a) / 86400000);
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
          window.dataLayer.push({ event: "calculator_use", service: "inc-20a-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live new-company clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 180);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-inc-due]", dmy(due));
          setText("[data-cap-by]", dmy(addDays(today, 100)));
          setText("[data-bm-by]", dmy(addDays(today, 30)));
          setText("[data-sc-by]", dmy(new Date(today.getFullYear(), today.getMonth() + 2, today.getDate())));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='inc20a']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until INC-20A is due for a company incorporated today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Due date and penalty calculator ---- */
        var pc = document.getElementById("penalty-calc");
        if (pc) {
          var incIn = pc.querySelector("[name='incdate']"), fileIn = pc.querySelector("[name='filedate']");
          var today0 = day(new Date());
          incIn.value = isoDate(addDays(today0, -150));
          fileIn.value = isoDate(today0);
          var renderPen = function () {
            var inc = parse(incIn.value), on = parse(fileIn.value);
            if (!inc || !on) return;
            var officers = Math.min(15, Math.max(1, Math.round(Number(pc.querySelector("[name='officers']").value) || 1)));
            var small = pc.querySelector("[name='small']").checked;
            var v = document.getElementById("pc-verdict"), rows = [], note = "";
            var due = addDays(inc, 180);
            if (inc >= START) rows.push(row("Due by", dmy(due)));
            if (inc < START) {
              v.textContent = "INC-20A doesn’t apply to companies incorporated before 2 November 2018.";
              v.className = "result__verdict is-no";
              rows.push(row("Penalty", "Not applicable", true));
            } else if (on <= due) {
              var left = daysBetween(on, due);
              v.textContent = "On time. " + left + (left === 1 ? " day" : " days") + " left to file.";
              v.className = "result__verdict is-no";
              rows.push(row("Days left", String(left)));
              rows.push(row("Penalty", "Nil", true));
              note = "File before you start business or borrow, even if days remain.";
            } else {
              var late = daysBetween(due, on);
              var half = small ? 0.5 : 1;
              var co = 50000 * half, each = Math.min(late * 1000, 100000) * half;
              v.textContent = late + (late === 1 ? " day" : " days") + " late. Penalty exposure up to " + inr(co + each * officers) + ".";
              v.className = "result__verdict is-yes";
              rows.push(row("Days late", String(late)));
              rows.push(row("Company", inr(co)));
              rows.push(row("Each officer (" + officers + ")", inr(each)));
              rows.push(row("Total exposure", inr(co + each * officers), true));
              note = (small ? "Halved under Section 446B. " : "") + "The adjudicating officer decides the final amount. Higher additional fees also apply to late filing.";
            }
            document.getElementById("pc-out").innerHTML = rows.join("");
            document.getElementById("pc-note").textContent = note;
          };
          pc.addEventListener("input", function () {
            trackUse("inc20a_penalty");
            renderPen();
          });
          pc.addEventListener("change", renderPen);
          renderPen();
        }

        /* ---- Readiness checker ---- */
        var rc = document.getElementById("ready-check");
        if (rc) {
          var renderReady = function () {
            var type = rc.querySelector("[name='ctype']").value;
            var items = [
              ["bank", "Bank account"],
              ["paid", "Subscription money"],
              ["office", "Registered office"],
              ["dsc", "Director’s DSC"],
            ];
            var v = document.getElementById("rc-verdict"), rows = [], missing = [];
            if (type !== "share") {
              v.textContent = "INC-20A isn’t required for your company.";
              v.className = "result__verdict is-no";
              document.getElementById("rc-out").innerHTML = row("INC-20A", "Not required", true);
              document.getElementById("rc-note").textContent =
                type === "old" ? "Section 10A applies only to companies incorporated on or after 2 November 2018." : "Section 10A applies only to companies with a share capital.";
              return;
            }
            items.forEach(function (it) {
              var ok = rc.querySelector("[name='" + it[0] + "']").checked;
              if (!ok) missing.push(it[1]);
              rows.push(row(it[1], ok ? "Done" : "Pending"));
            });
            rows.push(row("Ready to file", missing.length ? "Not yet" : "Yes", true));
            if (missing.length) {
              v.textContent = missing.length + (missing.length === 1 ? " item" : " items") + " pending before INC-20A.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Ready to file INC-20A.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("rc-out").innerHTML = rows.join("");
            document.getElementById("rc-note").textContent = missing.length
              ? "Each subscriber must pay the full value of the shares agreed in the memorandum, shown in the company’s bank statement."
              : "Send us the bank statement and we’ll certify and file within 24 hours.";
          };
          rc.addEventListener("change", function () {
            trackUse("inc20a_ready");
            renderReady();
          });
          renderReady();
        }
      })();
    </script>
