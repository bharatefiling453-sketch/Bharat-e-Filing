    <script>
      /* AOA amendment: live AOA clock, articles health check, AOA change route finder (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Articles altered by special resolution (Section 14); MGT-14 within 30 days (Section 117); entrenchment notice in MGT-14 within 30 days
           (Section 5(5), Rule 10); general meeting on 21 clear days' notice (Section 101); capital increase needs power in the articles (Section 61) */
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
          window.dataLayer.push({ event: "calculator_use", service: "aoa-amendment", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live AOA amendment clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-file-by]", dmy(due));
          setText("[data-egm-from]", dmy(addDays(today, 22)));
          setText("[data-entrench-by]", dmy(due));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='mgt14']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file MGT-14 for a resolution passed today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Articles health check ---- */
        var hc = document.getElementById("health");
        if (hc) {
          var CHECKS = [
            ["act2013", "Old 1956 Act references"],
            ["cappower", "No power to raise capital"],
            ["video", "No video meetings"],
            ["transfer", "No transfer restriction"],
            ["sharights", "Investor rights missing"],
            ["borrow", "No borrowing powers"],
          ];
          var renderHealth = function () {
            var gaps = CHECKS.filter(function (c) {
              return !hc.querySelector("[name='" + c[0] + "']").checked;
            });
            var v = document.getElementById("hc-verdict");
            var route = gaps.length >= 3 ? "Adopt new articles" : gaps.length ? "Alter the clauses" : "No change needed";
            v.textContent = gaps.length ? gaps.length + " gap" + (gaps.length > 1 ? "s" : "") + " found. " + route + "." : "Your articles look up to date.";
            v.className = "result__verdict " + (gaps.length ? "is-yes" : "is-no");
            document.getElementById("hc-out").innerHTML = [
              row("Gaps", String(gaps.length) + " of 6"),
              row("Resolution", gaps.length ? "Special" : "None"),
              row("Suggested route", route, true),
            ].join("");
            document.getElementById("hc-note").textContent = gaps.length
              ? "To fix: " + gaps.map(function (g) {
                  return g[1];
                }).join("; ") + "."
              : "Review again before your next funding round or capital increase.";
          };
          hc.addEventListener("change", function () {
            trackUse("aoa_health_check");
            renderHealth();
          });
          renderHealth();
        }

        /* ---- AOA change route finder ---- */
        var rf = document.getElementById("route-find");
        if (rf) {
          var renderRoute = function () {
            var pub = rf.querySelector("[name='ctype']").value === "pub";
            var change = rf.querySelector("[name='change']").value;
            var r, note;
            if (change === "alter") {
              r = ["Special resolution", "MGT-14", "None", "1–2 weeks"];
              note = "Attach the altered articles to MGT-14 within 30 days.";
            } else if (change === "new") {
              r = ["Special resolution", "MGT-14", "None", "2–3 weeks"];
              note = "One resolution adopts the new set in place of the old articles.";
            } else if (change === "entrench") {
              r = [pub ? "Special resolution" : "All members agree", "MGT-14", "None", "1–2 weeks"];
              note = pub ? "Public company: added by special resolution." : "Private company: every member must agree to the entrenchment.";
            } else {
              r = pub ? ["Special resolution", "MGT-14, INC-27", "Regional Director", "1–2 months"] : ["Special resolution", "MGT-14, INC-27", "Registrar", "2–4 weeks"];
              note = pub
                ? "Public to private needs Regional Director approval before the new certificate."
                : "Private to public: at least three directors and seven members, and “Private” removed from the name.";
            }
            var v = document.getElementById("rf-verdict");
            v.textContent = change === "convert" ? (pub ? "Public to private: approval needed." : "Private to public conversion.") : "File MGT-14 within 30 days.";
            v.className = "result__verdict " + (change === "convert" && pub ? "is-yes" : "is-no");
            document.getElementById("rf-out").innerHTML = [
              row("Approval", r[0]),
              row("Forms", r[1]),
              row("Outside approval", r[2]),
              row("Typical time", r[3], true),
            ].join("");
            document.getElementById("rf-note").textContent = note;
          };
          rf.addEventListener("change", function () {
            trackUse("aoa_route_finder");
            renderRoute();
          });
          renderRoute();
        }
      })();
    </script>
