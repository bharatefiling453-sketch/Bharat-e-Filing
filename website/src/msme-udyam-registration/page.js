    <script>
      /* Udyam registration: live MSME dates, MSME category checker, 45-day payment calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Limits from 1 April 2025 (S.O. 1364(E), 21 March 2025): micro ≤ ₹2.5 cr investment and ≤ ₹10 cr turnover; small ≤ ₹25 cr and ≤ ₹100 cr;
           medium ≤ ₹125 cr and ≤ ₹500 cr; export turnover excluded; crossing either limit moves an enterprise up. MSMED Act Section 15: payment
           within the agreed period (not more than 45 days) or 15 days without agreement; Section 16: compound interest at three times the RBI bank
           rate. MSME Form 1: by 30 April (October–March) and 31 October (April–September). */
        var LIMITS = [["Micro", 2.5, 10], ["Small", 25, 100], ["Medium", 125, 500]];
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
        function crore(n) {
          return "₹" + (Math.round(n * 100) / 100).toLocaleString("en-IN") + " cr";
        }
        function fyLabel(start) {
          return "FY " + start + "-" + String(start + 1).slice(2);
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
          window.dataLayer.push({ event: "calculator_use", service: "msme-udyam-registration", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live MSME dates ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear();
          var due = [new Date(y, 3, 30), new Date(y, 9, 31), new Date(y + 1, 3, 30)].filter(function (d) {
            return d >= today;
          })[0];
          var end = new Date(due.getFullYear(), due.getMonth(), due.getDate(), 23, 59, 59);
          var period = due.getMonth() === 9 ? "April–September " + due.getFullYear() : "October " + (due.getFullYear() - 1) + "–March " + due.getFullYear();
          setText("[data-msme1-by]", dmy(due));
          setText("[data-msme1-label]", "MSME Form 1 for " + period + " is due in");
          setText("[data-pay45]", dmy(addDays(today, 45)));
          setText("[data-pay15]", dmy(addDays(today, 15)));
          var fy = today.getMonth() >= 3 ? y : y - 1;
          setText("[data-fy-end]", "31 Mar " + (fy + 1));
          setText("[data-class-label]", "Your " + fyLabel(fy + 1) + " category will be based on " + fyLabel(fy) + " figures, ending");
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='msme1']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until MSME Form 1 is due");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- MSME category checker ---- */
        var cc = document.getElementById("class-calc");
        if (cc) {
          var renderClass = function () {
            var inv = Math.max(0, Number(cc.querySelector("[name='investment']").value) || 0);
            var turn = Math.max(0, Number(cc.querySelector("[name='turnover']").value) || 0);
            var exp = Math.min(turn, Math.max(0, Number(cc.querySelector("[name='exports']").value) || 0));
            var net = turn - exp;
            var cat = LIMITS.filter(function (l) {
              return inv <= l[1] && net <= l[2];
            })[0];
            var v = document.getElementById("cc-verdict"), note;
            if (cat) {
              v.textContent = "You qualify as a " + cat[0].toLowerCase() + " enterprise.";
              v.className = "result__verdict is-no";
              note = cat[0] === "Medium"
                ? "Medium enterprises can register on Udyam, but the 45-day payment protection covers only micro and small enterprises."
                : "Micro and small enterprises are covered by the 45-day payment protection under the MSMED Act.";
            } else {
              v.textContent = "Above the medium limits: not an MSME.";
              v.className = "result__verdict is-yes";
              note = "Enterprises above ₹125 crore investment or ₹500 crore turnover (exports excluded) aren’t MSMEs.";
            }
            document.getElementById("cc-out").innerHTML = [
              row("Investment", crore(inv)),
              row("Turnover less exports", crore(net)),
              row("Category", cat ? cat[0] : "Not MSME", true),
            ].join("");
            document.getElementById("cc-note").textContent = note + " Crossing either limit moves you up a category.";
          };
          cc.addEventListener("input", function () {
            trackUse("msme_category");
            renderClass();
          });
          renderClass();
        }

        /* ---- 45-day payment calculator ---- */
        var pc = document.getElementById("pay-calc");
        if (pc) {
          var dateIn = pc.querySelector("[name='accepted']");
          dateIn.value = isoDate(addDays(day(new Date()), -30));
          var renderPay = function () {
            var acc = parse(dateIn.value), today = day(new Date());
            if (!acc) return;
            var written = pc.querySelector("[name='written']").checked, paid = pc.querySelector("[name='paid']").checked;
            var asked = Math.max(1, Math.round(Number(pc.querySelector("[name='days']").value) || 1));
            var allowed = written ? Math.min(asked, 45) : 15;
            var due = addDays(acc, allowed);
            var late = Math.round((today - due) / 86400000);
            var v = document.getElementById("pc-verdict"), note;
            if (paid) {
              v.textContent = "Paid. Check it was on or before " + dmy(due) + ".";
              v.className = "result__verdict is-no";
              note = "A late payment still carries interest from the due date to the date of payment.";
            } else if (late > 0) {
              v.textContent = late + (late === 1 ? " day" : " days") + " overdue. Interest is running.";
              v.className = "result__verdict is-yes";
              note = "Compound interest with monthly rests at three times the RBI bank rate applies from " + dmy(addDays(due, 1)) + ". You can apply to the MSE Facilitation Council through MSME Samadhaan.";
            } else {
              v.textContent = "Due by " + dmy(due) + ": " + -late + (late === -1 ? " day" : " days") + " left.";
              v.className = "result__verdict is-no";
              note = "If unpaid by then, the buyer owes interest and, under the Income-tax Act, can deduct the amount only when it’s actually paid.";
            }
            document.getElementById("pc-out").innerHTML = [
              row("Period allowed", allowed + " days" + (written && asked > 45 ? " (capped)" : "")),
              row("Accepted on", dmy(acc)),
              row("Payment due by", dmy(due), true),
            ].join("");
            document.getElementById("pc-note").textContent =
              (written && asked > 45 ? "Agreed terms can’t exceed 45 days under Section 15, so 45 days apply. " : "") + note;
          };
          pc.addEventListener("input", function () {
            trackUse("msme_45_day");
            renderPay();
          });
          pc.addEventListener("change", renderPay);
          renderPay();
        }
      })();
    </script>
