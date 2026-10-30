    <script>
      /* Shop Act registration: live dates, registration route checker, document checklist (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* All four Labour Codes in force from 21 November 2025; the OSH Code provides for registration of establishments with 10 or more workers.
           Maharashtra Shops and Establishments (Regulation of Employment and Conditions of Service) Act, 2017: Form A registration for 10 or more
           workers, Form F intimation below 10, within 60 days of commencement; Maharashtra reportedly accepts OSH Code registration in place of
           separate registration from April 2026. Other states follow their own Acts and rules. */
        var LABOUR_CODES = new Date(2025, 10, 21);
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
          window.dataLayer.push({ event: "calculator_use", service: "shop-act-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live dates ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var by = addDays(today, 60);
          var end = new Date(by.getFullYear(), by.getMonth(), by.getDate(), 23, 59, 59);
          setText("[data-mh60]", dmy(by));
          setText("[data-lc-days]", String(Math.max(0, Math.round((today - LABOUR_CODES) / 86400000))));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='mh60']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left in the 60-day window for a Maharashtra establishment opened today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Registration route checker ---- */
        var rt = document.getElementById("route-check");
        if (rt) {
          var renderRoute = function () {
            var state = rt.querySelector("[name='state']").value;
            var workers = Math.max(0, Math.round(Number(rt.querySelector("[name='workers']").value) || 0));
            var big = workers >= 10;
            var v = document.getElementById("rt-verdict"), rows = [], note;
            if (state === "mh") {
              if (big) {
                v.textContent = "Registration needed: OSH Code or Form A.";
                note = "With 10 or more workers, the 2017 Act required Form A registration; Maharashtra reportedly accepts OSH Code registration in its place from April 2026. We confirm the current route before filing.";
                rows.push(row("Under the 2017 Act", "Form A registration"));
                rows.push(row("Under the OSH Code", "Registration applies"));
              } else {
                v.textContent = "Intimation in Form F, within 60 days.";
                note = "With fewer than 10 workers, the 2017 Act needs only a one-time intimation in Form F. We check for any newer notification before filing.";
                rows.push(row("Under the 2017 Act", "Form F intimation"));
                rows.push(row("Under the OSH Code", "Below 10 workers"));
              }
              rows.push(row("Opening today? File by", dmy(addDays(day(new Date()), 60)), true));
            } else {
              v.textContent = big ? "OSH Code registration applies; check your state Act." : "Your state’s Shop Act applies.";
              note = big
                ? "With 10 or more workers, OSH Code registration applies; whether it replaces your state’s Shop Act registration depends on your state’s rules."
                : "Most states require shops and offices to register or file an intimation under their own Act, with their own thresholds and deadlines. Tell us your state and we’ll confirm.";
              rows.push(row("State Shop Act", "Check thresholds"));
              rows.push(row("OSH Code", big ? "Registration applies" : "Below 10 workers"));
              rows.push(row("Deadline", "As your state sets", true));
            }
            v.className = "result__verdict " + (big ? "is-yes" : "is-no");
            rows.unshift(row("Workers", String(workers)));
            document.getElementById("rt-out").innerHTML = rows.join("");
            document.getElementById("rt-note").textContent = note;
          };
          rt.addEventListener("input", function () {
            trackUse("shop_route");
            renderRoute();
          });
          rt.addEventListener("change", renderRoute);
          renderRoute();
        }

        /* ---- Document checklist ---- */
        var ENTITY = {
          prop: ["Proprietor’s PAN and ID", "Proprietor’s address proof"],
          firm: ["Partnership deed and firm PAN", "Partners’ ID and address proof"],
          llp: ["LLP agreement, incorporation and PAN", "Designated partners’ ID"],
          co: ["Certificate of incorporation and PAN", "Directors’ ID and board authorisation"],
        };
        var PREMISES = {
          rented: "Rent agreement and NOC",
          owned: "Property or tax receipt",
          family: "Owner’s NOC",
        };
        var dc = document.getElementById("docs-check");
        if (dc) {
          var renderDocs = function () {
            var e = dc.querySelector("[name='entity']").value, p = dc.querySelector("[name='premises']").value;
            var list = ENTITY[e].concat([PREMISES[p], "Utility bill", "Photograph", "Number of workers"]);
            var v = document.getElementById("dc-verdict");
            v.textContent = list.length + " items to keep ready.";
            v.className = "result__verdict is-no";
            document.getElementById("dc-out").innerHTML = list
              .map(function (item, i) {
                return row(item, "Needed", i === list.length - 1);
              })
              .join("");
            document.getElementById("dc-note").textContent = "A typical list; some states ask for more, such as a photo of the shop with its signboard.";
          };
          dc.addEventListener("change", function () {
            trackUse("shop_docs");
            renderDocs();
          });
          renderDocs();
        }
      })();
    </script>
