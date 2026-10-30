    <script>
      /* FDI filing: live FEMA calendar, FDI deadline calculator, FDI readiness checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* FEMA (Mode of Payment and Reporting of Non-Debt Instruments) Regulations, 2019 and the RBI Master Direction on Foreign Investment in
           India: capital instruments to be issued within 60 days of receipt of consideration, else refunded within 15 days after that;
           FC-GPR within 30 days of issue; FC-TRS within 60 days of transfer or receipt/remittance of funds, whichever is earlier; LLP-I within
           30 days of receipt of consideration; LLP-II within 60 days of receipt of funds; FLA return by 15 July each year. Delays can be
           regularised with a late submission fee within three years of the due date. */
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
          window.dataLayer.push({ event: "calculator_use", service: "fdi-filing", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live FEMA calendar ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var gpr = addDays(today, 30), allot = addDays(today, 60);
          var end = new Date(gpr.getFullYear(), gpr.getMonth(), gpr.getDate(), 23, 59, 59);
          setText("[data-gpr-by]", dmy(gpr));
          setText("[data-allot-by]", dmy(allot));
          setText("[data-refund-by]", dmy(addDays(allot, 15)));
          var fla = new Date(today.getFullYear(), 6, 15);
          if (fla < today) fla = new Date(today.getFullYear() + 1, 6, 15);
          setText("[data-fla-by]", dmy(fla));
          setText("[data-fla-label]", "The FLA return for 31 March " + fla.getFullYear() + " is due by");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='gpr']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours to file FC-GPR for shares allotted today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- FDI deadline calculator ---- */
        var dl = document.getElementById("deadline-calc");
        if (dl) {
          var typeIn = dl.querySelector("[name='event']"), fundsIn = dl.querySelector("[name='funds']"), evIn = dl.querySelector("[name='eventdate']");
          var evLabel = document.getElementById("dl-event-label");
          var t0 = day(new Date());
          fundsIn.value = isoDate(addDays(t0, -10));
          evIn.value = isoDate(t0);
          var renderDl = function () {
            var type = typeIn.value, today = day(new Date());
            var llp = type === "llp1" || type === "llp2";
            evIn.disabled = llp;
            evLabel.textContent = type === "gpr" ? "Shares allotted on" : type === "trs" ? "Shares transferred on" : "Not needed for this form";
            var funds = parse(fundsIn.value), ev = parse(evIn.value);
            if (!funds || (!llp && !ev)) return;
            var form, due, rows = [], warn = "";
            if (type === "gpr") {
              form = "FC-GPR";
              var allotBy = addDays(funds, 60);
              due = addDays(ev, 30);
              rows.push(row("Allot by", dmy(allotBy)));
              if (ev > allotBy) warn = "Shares were allotted more than 60 days after the money came in, which is a contravention. Talk to us about regularising it. ";
              if (ev < funds) warn = "Shares are normally allotted after the money is received. Check the dates. ";
            } else if (type === "trs") {
              form = "FC-TRS";
              due = addDays(ev < funds ? ev : funds, 60);
            } else if (type === "llp1") {
              form = "LLP-I";
              due = addDays(funds, 30);
            } else {
              form = "LLP-II";
              due = addDays(funds, 60);
            }
            var left = daysBetween(today, due);
            var v = document.getElementById("dl-verdict");
            if (left < 0) {
              v.textContent = form + " is overdue by " + -left + (left === -1 ? " day." : " days.");
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = form + " is due in " + left + (left === 1 ? " day." : " days.");
              v.className = "result__verdict " + (left <= 7 ? "is-yes" : "is-no");
            }
            rows.unshift(row("Form", form));
            rows.push(row("Due by", dmy(due), true));
            document.getElementById("dl-out").innerHTML = rows.join("");
            document.getElementById("dl-note").textContent =
              warn +
              (left < 0
                ? daysBetween(due, today) <= 1095
                  ? "Within three years of the due date, you can still file with a late submission fee."
                  : "More than three years late, so this needs compounding with the RBI."
                : type === "trs"
                ? "The resident party to the transfer files FC-TRS."
                : "File on the FIRMS portal; your AD bank reviews it.");
          };
          dl.addEventListener("input", function () {
            trackUse("fdi_deadline");
            renderDl();
          });
          dl.addEventListener("change", renderDl);
          renderDl();
        }

        /* ---- FDI readiness checker ---- */
        var rt = document.getElementById("route-check");
        if (rt) {
          var renderRoute = function () {
            var lb = rt.querySelector("[name='landborder']").checked, gs = rt.querySelector("[name='govsector']").checked;
            var price = rt.querySelector("[name='price']").checked, bank = rt.querySelector("[name='banking']").checked;
            var gov = lb || gs, issues = [];
            if (!price) issues.push("For an unlisted company, the issue price can’t be below the fair value certified by a CA, SEBI-registered merchant banker or practising cost accountant.");
            if (!bank) issues.push("FDI must come through banking channels, with the investor’s KYC from the remitting bank.");
            var v = document.getElementById("rt-verdict");
            if (issues.length) {
              v.textContent = issues.length + (issues.length === 1 ? " thing" : " things") + " to fix before allotting.";
              v.className = "result__verdict is-yes";
            } else if (gov) {
              v.textContent = "Government approval needed first.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Looks ready for the automatic route.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("rt-out").innerHTML = [
              row("Route", gov ? "Government" : "Automatic"),
              row("Issue price", price ? "At or above fair value" : "Too low"),
              row("Funds", bank ? "Banking channel" : "Not allowed"),
              row("Then file", "FC-GPR in 30 days", true),
            ].join("");
            document.getElementById("rt-note").textContent = issues.length
              ? issues[0]
              : lb
              ? "Under Press Note 3 (2020), investment where the investor or beneficial owner is from a country sharing a land border with India needs government approval."
              : gs
              ? "Check the sector’s cap and conditions in the FDI policy and get approval before accepting the money."
              : "Confirm your sector’s cap in the current FDI policy before the money arrives.";
          };
          rt.addEventListener("input", function () {
            trackUse("fdi_readiness");
            renderRoute();
          });
          rt.addEventListener("change", renderRoute);
          renderRoute();
        }
      })();
    </script>
