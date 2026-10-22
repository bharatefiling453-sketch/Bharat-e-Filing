    <script>
      /* Company name change: live name change clock, name readiness checker, timeline planner (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* RUN for change of name: 60 days (Rule 9); RUN-LLP: 90 days; MGT-14: 30 days (Section 117); GST core amendment: 15 days (Rule 19); former name: 2 years (Section 12) */
        var RUN_DAYS = { company: 60, llp: 90 };
        /* Words that need Central Government or regulator approval (Rule 8B, illustrative list) */
        var RESTRICTED = ["bank", "banking", "insurance", "stock exchange", "mutual fund", "venture capital", "asset management", "nidhi", "board", "commission", "authority", "undertaking", "national", "union", "central", "federal", "republic", "president", "rashtrapati", "federation", "chamber", "small scale industries", "khadi"];
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
        function escapeHtml(s) {
          return s.replace(/[&<>"']/g, function (c) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
          });
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
          window.dataLayer.push({ event: "calculator_use", service: "company-name-change", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live name change clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var run = addDays(today, RUN_DAYS.company);
          var end = new Date(run.getFullYear(), run.getMonth(), run.getDate(), 23, 59, 59);
          setText("[data-run-by]", dmy(run));
          setText("[data-mgt14-by]", dmy(addDays(today, 30)));
          setText("[data-gst-by]", dmy(addDays(today, 15)));
          setText("[data-former-by]", dmy(new Date(today.getFullYear() + 2, today.getMonth(), today.getDate())));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='run']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until a name reserved today expires");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Name readiness checker ---- */
        var nm = document.getElementById("name-check");
        if (nm) {
          var SUFFIX = { pvt: /private limited$/i, opc: /\(opc\) private limited$/i, llp: /\bllp$/i };
          var SUFFIX_LABEL = { pvt: "Private Limited", opc: "(OPC) Private Limited", llp: "LLP" };
          var renderName = function () {
            var type = nm.querySelector("[name='type']").value;
            var name = (nm.querySelector("[name='proposed']").value || "").trim().replace(/\s+/g, " ");
            var filings = nm.querySelector("[name='filings']").checked, deposits = nm.querySelector("[name='deposits']").checked;
            var lower = " " + name.toLowerCase() + " ";
            var hits = RESTRICTED.filter(function (w) {
              return lower.indexOf(" " + w + " ") >= 0;
            });
            var suffixOk = type === "pvt" ? SUFFIX.pvt.test(name) && !SUFFIX.opc.test(name) : SUFFIX[type].test(name);
            var blocked = !filings || (!deposits && type !== "llp");
            var v = document.getElementById("nm-verdict");
            if (!name) {
              v.textContent = "Type a proposed name to check it.";
              v.className = "result__verdict is-yes";
            } else if (blocked) {
              v.textContent = "Clear pending filings first. The change can’t be approved yet.";
              v.className = "result__verdict is-yes";
            } else if (!suffixOk || hits.length) {
              v.textContent = "Fix the points below before reserving.";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = "Looks ready for a name search and RUN.";
              v.className = "result__verdict is-no";
            }
            document.getElementById("nm-out").innerHTML = [
              row("Ending", suffixOk ? "Correct" : "Should end with “" + SUFFIX_LABEL[type] + "”"),
              row("Restricted words", hits.length ? escapeHtml(hits.join(", ")) + " (approval needed)" : "None found"),
              row("Filing status", filings && (deposits || type === "llp") ? "OK" : "Default to clear", true),
            ].join("");
            document.getElementById("nm-note").textContent =
              "This checks form only. Similarity with existing companies and trademarks is checked on the MCA and IP India databases before filing.";
          };
          nm.addEventListener("input", function () {
            trackUse("name_readiness");
            renderName();
          });
          nm.addEventListener("change", renderName);
          renderName();
        }

        /* ---- Name change timeline planner ---- */
        var tp = document.getElementById("timeline-plan");
        if (tp) {
          var startIn = tp.querySelector("[name='start']");
          startIn.value = isoDate(new Date());
          var renderPlan = function () {
            var llp = tp.querySelector("[name='ttype']").value === "llp";
            var start = parse(startIn.value);
            if (!start) return;
            var shortNotice = tp.querySelector("[name='short']").checked;
            var runEnd = addDays(start, llp ? RUN_DAYS.llp : RUN_DAYS.company);
            var rows = [];
            if (llp) {
              var consent = addDays(start, 3);
              rows.push(row("Partners’ consent (target)", dmy(consent)));
              rows.push(row("Form 5 by", dmy(addDays(consent, 30))));
              rows.push(row("Form 3 by", dmy(addDays(consent, 30))));
            } else {
              var egm = addDays(start, shortNotice ? 4 : 23);
              rows.push(row("General meeting (earliest)", dmy(egm) + (shortNotice ? " · short notice" : " · 21 days’ notice")));
              rows.push(row("MGT-14 by", dmy(addDays(egm, 30))));
              rows.push(row("INC-24 (target)", dmy(addDays(egm, 3))));
            }
            rows.push(row("Name reservation ends", dmy(runEnd), true));
            var v = document.getElementById("tp-verdict");
            v.textContent = llp ? "LLP: Form 5 and Form 3 within 30 days of consent." : "Company: file INC-24 before the reservation ends.";
            v.className = "result__verdict is-no";
            document.getElementById("tp-out").innerHTML = rows.join("");
          };
          tp.addEventListener("input", function () {
            trackUse("name_change_timeline");
            renderPlan();
          });
          tp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
