    <script>
      /* Digital signature: live DSC dates, DSC finder, DSC expiry checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Filings signed with a DSC: DIR-3 KYC by 30 September; AOC-4 within 30 days and MGT-7 within 60 days of the AGM (taken as 30 September,
           so 30 October and 29 November); GSTR-9 by 31 December for the previous financial year (companies sign GST returns with a DSC under
           CGST Rule 26). Class 3 is the only class issued since 1 January 2021 (CCA). */
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function addMonths(from, n) {
          return new Date(from.getFullYear(), from.getMonth() + n, from.getDate());
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
        /* Upcoming DSC-signed deadlines from a date, for the next 12 months */
        function deadlines(from) {
          var list = [];
          [from.getFullYear(), from.getFullYear() + 1].forEach(function (y) {
            list.push({ d: new Date(y, 8, 30), name: "DIR-3 KYC" });
            list.push({ d: new Date(y, 9, 30), name: "AOC-4" });
            list.push({ d: new Date(y, 10, 29), name: "MGT-7" });
            list.push({ d: new Date(y, 11, 31), name: "GSTR-9" });
          });
          var limit = addMonths(from, 12);
          return list
            .filter(function (x) {
              return x.d >= from && x.d <= limit;
            })
            .sort(function (a, b) {
              return a.d - b.d;
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
          window.dataLayer.push({ event: "calculator_use", service: "digital-signature", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live DSC dates ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var next = deadlines(today).filter(function (x) {
            return x.name !== "GSTR-9";
          })[0];
          var end = new Date(next.d.getFullYear(), next.d.getMonth(), next.d.getDate(), 23, 59, 59);
          setText("[data-roc-due]", dmy(next.d));
          setText("[data-roc-label]", "Your next MCA filing that needs a director’s DSC, " + next.name + ", is due in");
          var g9 = new Date(today.getFullYear(), 11, 31);
          setText("[data-gst9-by]", dmy(g9));
          setText("[data-gst9-label]", "GSTR-9 for FY " + (g9.getFullYear() - 1) + "-" + String(g9.getFullYear()).slice(2) + " is due by");
          setText("[data-valid1]", dmy(addDays(addMonths(today, 12), -1)));
          setText("[data-valid2]", dmy(addDays(addMonths(today, 24), -1)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='roc']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next MCA filing that needs a DSC");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- DSC finder ---- */
        var USES = {
          mca: ["MCA filings", "Register it on the MCA portal before signing e-forms."],
          itr: ["Income tax", "Register it on the e-filing portal. Companies must verify returns with a DSC."],
          gst: ["GST", "Register it on the GST portal. Companies must sign GST returns with a DSC."],
          tender: ["E-tenders", "Most e-tender portals need both signing and encryption, so choose a combo DSC."],
        };
        var df = document.getElementById("dsc-finder");
        if (df) {
          var renderFind = function () {
            var who = df.querySelector("[name='who']").value, use = df.querySelector("[name='use']").value;
            var often = df.querySelector("[name='often']").checked;
            var type = use === "tender" ? "Combo" : "Signature";
            var holder = who === "org" ? "Organisation" : who === "foreign" ? "Foreign national" : "Individual";
            var years = often || use === "mca" ? "2 years" : "1 year";
            var docs = who === "org" ? "PAN and organisation proof" : who === "foreign" ? "Passport" : "PAN and Aadhaar mobile";
            var v = document.getElementById("df-verdict");
            v.textContent = "You need: Class 3 " + (use === "tender" ? "combo" : "signature") + " DSC, " + years + ".";
            v.className = "result__verdict is-no";
            document.getElementById("df-out").innerHTML = [
              row("Class", "Class 3"),
              row("Type", type),
              row("Holder", holder),
              row("Keep ready", docs),
              row("Suggested validity", years, true),
            ].join("");
            document.getElementById("df-note").textContent = USES[use][1];
          };
          df.addEventListener("change", function () {
            trackUse("dsc_finder");
            renderFind();
          });
          renderFind();
        }

        /* ---- DSC expiry checker ---- */
        var ec = document.getElementById("expiry-check");
        if (ec) {
          var expIn = ec.querySelector("[name='expiry']");
          expIn.value = isoDate(addDays(day(new Date()), 45));
          var renderExp = function () {
            var exp = parse(expIn.value), today = day(new Date());
            if (!exp) return;
            var left = daysBetween(today, exp);
            var missed = deadlines(today).filter(function (x) {
              return x.d > exp;
            });
            var v = document.getElementById("ec-verdict"), rows = [];
            if (left < 0) {
              v.textContent = "Your DSC has expired. Apply for a new one before your next filing.";
              v.className = "result__verdict is-yes";
            } else if (missed.length) {
              v.textContent = left + (left === 1 ? " day" : " days") + " left. It expires before " + missed[0].name + " on " + dmy(missed[0].d) + ".";
              v.className = "result__verdict is-yes";
            } else {
              v.textContent = left + " days left. It covers your filings for the next 12 months.";
              v.className = "result__verdict is-no";
            }
            rows.push(row("Valid until", dmy(exp)));
            rows.push(row("Days left", String(Math.max(0, left))));
            rows.push(row("Filings at risk", missed.length ? String(missed.length) : "None"));
            rows.push(row("Apply for renewal by", left < 0 ? "Now" : dmy(addDays(exp, -15)), true));
            document.getElementById("ec-out").innerHTML = rows.join("");
            document.getElementById("ec-note").textContent =
              "A renewal is a fresh certificate with new verification, so leave time. Register the new DSC on each portal afterwards. Filings listed: DIR-3 KYC, AOC-4, MGT-7 and GSTR-9.";
          };
          ec.addEventListener("input", function () {
            trackUse("dsc_expiry");
            renderExp();
          });
          ec.addEventListener("change", renderExp);
          renderExp();
        }
      })();
    </script>
