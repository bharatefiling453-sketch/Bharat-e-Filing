    <script>
      /* DPT-3: live DPT-3 clock, need-to-file checker, deposit trap timer (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* DPT-3 by 30 June, figures as on 31 March (Rule 16); customer advances exempted only if adjusted within 365 days (Rule 2(1)(c)(xii)(a));
           share application money: allot within 60 days, else refund within 15 days (Rule 2(1)(c)(x)); director and relative loans need declarations */
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
        function nextDue(today) {
          var d = new Date(today.getFullYear(), 5, 30);
          return d < today ? new Date(today.getFullYear() + 1, 5, 30) : d;
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
          window.dataLayer.push({ event: "calculator_use", service: "dpt-3-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live DPT-3 clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = nextDue(today), asOf = new Date(due.getFullYear(), 2, 31);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-dpt-by]", dmy(due));
          setText("[data-asof]", dmy(asOf));
          setText("[data-dpt-label]", "The return as on " + dmy(asOf));
          setText("[data-allot-by]", dmy(addDays(today, 60)));
          setText("[data-refund-by]", dmy(addDays(today, 75)));
          setText("[data-advance-by]", dmy(addDays(today, 365)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='dpt3']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next DPT-3 due date");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Do I need to file DPT-3? ---- */
        var nc = document.getElementById("need-check");
        if (nc) {
          var renderNeed = function () {
            var type = nc.querySelector("[name='ctype']").value;
            var on = function (n) {
              return nc.querySelector("[name='" + n + "']").checked;
            };
            var v = document.getElementById("nc-verdict");
            if (type === "excluded") {
              v.textContent = "The Deposit Rules don’t apply to your company.";
              v.className = "result__verdict is-no";
              document.getElementById("nc-out").innerHTML = [row("DPT-3", "Not required", true)].join("");
              document.getElementById("nc-note").textContent = "Government companies, banks, NBFCs and housing finance companies follow their own rules.";
              return;
            }
            var exempt = ["director", "company"].filter(on).length + (on("relative") && type === "pvt" ? 1 : 0);
            var deposits = (on("advance") ? 1 : 0) + (on("share") ? 1 : 0) + (on("member") ? 1 : 0) + (on("relative") && type === "pub" ? 1 : 0);
            var file = exempt + deposits > 0;
            v.textContent = !file ? "Nothing to report. DPT-3 isn’t needed this year." : deposits ? "File DPT-3, and check the deposits." : "File DPT-3 for exempted receipts.";
            v.className = "result__verdict " + (deposits ? "is-yes" : "is-no");
            var flags = [];
            if (on("advance")) flags.push("advance");
            if (on("share")) flags.push("share money");
            if (on("relative") && type === "pub") flags.push("relative’s loan");
            document.getElementById("nc-out").innerHTML = [
              row("Exempted items", String(exempt)),
              row("Deposits or likely deposits", String(deposits)),
              row("Declarations", on("director") || on("relative") ? "Needed" : "Not needed"),
              row("DPT-3 by", file ? "30 June" : "Not required", true),
            ].join("");
            document.getElementById("nc-note").textContent = flags.length
              ? "Treated as deposits: " + flags.join(", ") + ". These need attention under Section 73; talk to us before 31 March."
              : on("member")
              ? "Deposits from members need the auditor’s certificate and must stay within Section 73 limits."
              : "Keep the director and relative declarations on file with every loan.";
          };
          nc.addEventListener("change", function () {
            trackUse("dpt3_need_check");
            renderNeed();
          });
          renderNeed();
        }

        /* ---- Deposit trap timer ---- */
        var tt = document.getElementById("trap-timer");
        if (tt) {
          var renderTrap = function () {
            var kind = tt.querySelector("[name='kind']").value;
            var d = parse(tt.querySelector("[name='received']").value);
            if (!d) return;
            var today = day(new Date()), rows = [];
            var limit = kind === "advance" ? addDays(d, 365) : addDays(d, 75);
            var left = Math.round((limit - today) / 86400000);
            var v = document.getElementById("tt-verdict");
            if (kind === "advance") {
              rows.push(row("Adjust against supply by", dmy(limit)));
            } else {
              rows.push(row("Allot shares by", dmy(addDays(d, 60))));
              rows.push(row("Else refund by", dmy(limit)));
            }
            rows.push(row(left >= 0 ? "Days left" : "Deposit since", left >= 0 ? String(left) : dmy(addDays(limit, 1)), true));
            v.textContent = left >= 0 ? "Still exempted. " + left + " days to act." : "Now treated as a deposit. Act now.";
            v.className = "result__verdict " + (left >= 0 ? "is-no" : "is-yes");
            document.getElementById("tt-out").innerHTML = rows.join("");
          };
          tt.addEventListener("input", function () {
            trackUse("dpt3_trap_timer");
            renderTrap();
          });
          tt.addEventListener("change", renderTrap);
          renderTrap();
        }
      })();
    </script>
