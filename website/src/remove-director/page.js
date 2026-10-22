    <script>
      /* Remove a director: live removal clock, removal route finder, removal timeline checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Special notice: at least 14 clear days before the meeting (excluding both days) and not earlier than three months before it (Section 115, Rule 23);
           members told at least 7 days before; DIR-12 within 30 days (Section 170(2)); requisitioned EGM held within 45 days (Section 100(4));
           office vacates after absence from all board meetings for 12 months (Section 167(1)(b)) */
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
          window.dataLayer.push({ event: "calculator_use", service: "remove-director", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live removal clock ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var due = addDays(today, 30);
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          setText("[data-dir12-by]", dmy(due));
          setText("[data-meeting-from]", dmy(addDays(today, 15)));
          setText("[data-egm-by]", dmy(addDays(today, 45)));
          setText("[data-absent-by]", dmy(addMonths(today, 12)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='dir12']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to file DIR-12 for a removal today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Director removal route finder ---- */
        var rt = document.getElementById("route-find");
        if (rt) {
          var ROUTE = {
            remove: ["Section 169 removal", "Ordinary resolution", "Special notice, DIR-12", "3–6 weeks"],
            absent: ["Office vacated (Section 167)", "None; board notes it", "DIR-12", "About 1 week"],
            disq: ["Office vacated (Section 167)", "None; board notes it", "DIR-12", "About 1 week"],
            self: ["Resignation (Section 168)", "Your written notice", "DIR-11, company’s DIR-12", "About 1 week"],
            unfiled: ["Your own DIR-11", "Proof of resignation", "DIR-11", "Within 30 days of resigning"],
          };
          var renderRoute = function () {
            var c = rt.querySelector("[name='situation']").value;
            var tribunal = rt.querySelector("[name='tribunal']").checked, board = rt.querySelector("[name='board']").checked;
            var r = ROUTE[c];
            var v = document.getElementById("rt-verdict");
            var blocked = c === "remove" && tribunal;
            v.textContent = blocked ? "A Tribunal-appointed director can’t be removed under Section 169." : r[0] + ".";
            v.className = "result__verdict " + (blocked || (c === "remove" && !board) ? "is-yes" : "is-no");
            document.getElementById("rt-out").innerHTML = [
              row("Approval", blocked ? "Apply to the Tribunal" : r[1]),
              row("Forms", r[2]),
              row("Meeting", c === "remove" ? (board ? "Board calls the EGM" : "Requisition (Section 100)") : "Not needed"),
              row("Typical time", r[3], true),
            ].join("");
            document.getElementById("rt-note").textContent = blocked
              ? "Directors appointed by the Tribunal under Section 242 can only be changed through the Tribunal."
              : c === "remove"
              ? board
                ? "Special notice from members with 1% voting power, 14 clear days before the meeting; the director must be heard."
                : "Members with 10% of the voting capital requisition the EGM; the board must call it within 21 days."
              : c === "unfiled"
              ? "Your DIR-11 with proof of delivery records the resignation even if the company doesn’t file DIR-12."
              : "The company still records the change in DIR-12 within 30 days.";
          };
          rt.addEventListener("change", function () {
            trackUse("removal_route_finder");
            renderRoute();
          });
          renderRoute();
        }

        /* ---- Removal timeline checker ---- */
        var rp = document.getElementById("removal-plan");
        if (rp) {
          var noticeIn = rp.querySelector("[name='noticedate']"), meetIn = rp.querySelector("[name='meetingdate']");
          var t = day(new Date());
          noticeIn.value = isoDate(t);
          meetIn.value = isoDate(addDays(t, 20));
          var renderPlan = function () {
            var n = parse(noticeIn.value), m = parse(meetIn.value);
            if (!n || !m) return;
            var earliest = addDays(n, 15), latestNotice = addMonths(m, -3);
            var tooSoon = m < earliest, tooEarly = n < latestNotice;
            var v = document.getElementById("rp-verdict");
            v.textContent = tooSoon
              ? "Too soon. Hold the meeting on or after " + dmy(earliest) + "."
              : tooEarly
              ? "Notice is more than three months before the meeting."
              : "Timeline works for the special notice.";
            v.className = "result__verdict " + (tooSoon || tooEarly ? "is-yes" : "is-no");
            document.getElementById("rp-out").innerHTML = [
              row("Earliest meeting", dmy(earliest)),
              row("Tell members by", dmy(addDays(m, -7))),
              row("DIR-12 by", dmy(addDays(m, 30)), true),
            ].join("");
          };
          rp.addEventListener("input", function () {
            trackUse("removal_timeline");
            renderPlan();
          });
          rp.addEventListener("change", renderPlan);
          renderPlan();
        }
      })();
    </script>
