    <script>
      /* Legal consultation: live legal deadlines, cheque bounce timeline, consumer forum finder (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Negotiable Instruments Act, 1881: demand notice within 30 days of the bank's return memo (Section 138(b)); drawer has 15 days from
           receiving the notice to pay (Section 138(c)); complaint within one month of the cause of action that follows (Section 142(1)(b)).
           Consumer Protection Act, 2019: complaint within two years of the cause of action (Section 69); District Commission up to ₹50 lakh,
           State Commission above ₹50 lakh up to ₹2 crore, National Commission above ₹2 crore (Consumer Protection (Jurisdiction) Rules, 2021).
           Limitation Act, 1963: most money suits within three years. */
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
        function plural(n, w) {
          return n + " " + w + (n === 1 ? "" : "s");
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
          window.dataLayer.push({ event: "calculator_use", service: "legal-consultation", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live legal deadlines ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var notice = addDays(today, 30);
          var end = new Date(notice.getFullYear(), notice.getMonth(), notice.getDate(), 23, 59, 59);
          setText("[data-notice-by]", dmy(notice));
          setText("[data-complaint-by]", dmy(addMonths(addDays(today, 15), 1)));
          setText("[data-consumer-by]", dmy(addMonths(today, 24)));
          setText("[data-recovery-by]", dmy(addMonths(today, 36)));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='notice']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours left to send a cheque bounce notice for a memo received today");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Cheque bounce timeline ---- */
        var cc = document.getElementById("cheque-calc");
        if (cc) {
          var memoIn = cc.querySelector("[name='memo']"), servedIn = cc.querySelector("[name='served']");
          var sentBox = cc.querySelector("[name='sent']");
          var t0 = day(new Date());
          memoIn.value = isoDate(addDays(t0, -10));
          servedIn.value = isoDate(t0);
          var renderChq = function () {
            var memo = parse(memoIn.value), today = day(new Date());
            if (!memo) return;
            var sent = sentBox.checked;
            servedIn.disabled = !sent;
            var noticeBy = addDays(memo, 30);
            var v = document.getElementById("cc-verdict"), rows = [row("Notice by", dmy(noticeBy))], note = "";
            if (!sent) {
              var left = daysBetween(today, noticeBy);
              if (left >= 0) {
                v.textContent = plural(left, "day") + " left to send the demand notice.";
                v.className = "result__verdict " + (left <= 7 ? "is-yes" : "is-no");
                note = "Send it in writing to the drawer, demanding the cheque amount. Tick the box once it’s sent.";
              } else {
                v.textContent = "The 30-day notice window has passed.";
                v.className = "result__verdict is-yes";
                note = "A Section 138 case may no longer be possible on this memo. Other remedies, like a recovery suit, may still be open: ask an advocate.";
              }
              rows.push(row("Payment window", "Starts when notice is received"));
              rows.push(row("Complaint by", "After the payment window", true));
            } else {
              var served = parse(servedIn.value);
              if (!served) return;
              var payBy = addDays(served, 15), complaintBy = addMonths(payBy, 1);
              rows.push(row("Payment due by", dmy(payBy)));
              rows.push(row("Complaint from", dmy(addDays(payBy, 1))));
              rows.push(row("Complaint by", dmy(complaintBy), true));
              if (today <= payBy) {
                v.textContent = "Waiting for payment until " + dmy(payBy) + ".";
                v.className = "result__verdict is-no";
                note = "If the drawer pays in full within 15 days of receiving the notice, the matter ends there.";
              } else if (today <= complaintBy) {
                v.textContent = "Not paid? File the complaint by " + dmy(complaintBy) + ".";
                v.className = "result__verdict is-yes";
                note = "The complaint is filed before the magistrate with jurisdiction, usually where the payee’s bank account is.";
              } else {
                v.textContent = "The usual complaint window has passed.";
                v.className = "result__verdict is-yes";
                note = "Courts can condone a delay for sufficient cause. Speak to an advocate quickly.";
              }
            }
            document.getElementById("cc-out").innerHTML = rows.join("");
            document.getElementById("cc-note").textContent = note;
          };
          cc.addEventListener("input", function () {
            trackUse("cheque_bounce");
            renderChq();
          });
          cc.addEventListener("change", renderChq);
          renderChq();
        }

        /* ---- Consumer forum finder ---- */
        var ff = document.getElementById("forum-find");
        if (ff) {
          var causeIn = ff.querySelector("[name='cause']");
          causeIn.value = isoDate(addMonths(day(new Date()), -3));
          var renderForum = function () {
            var value = Math.max(0, Number(ff.querySelector("[name='value']").value) || 0);
            var cause = parse(causeIn.value), today = day(new Date());
            if (!cause) return;
            var forum = value <= 5000000 ? "District Commission" : value <= 20000000 ? "State Commission" : "National Commission";
            var lastDay = addMonths(cause, 24);
            var v = document.getElementById("ff-verdict");
            if (today <= lastDay) {
              v.textContent = "File with the " + forum + " by " + dmy(lastDay) + ".";
              v.className = "result__verdict is-no";
            } else {
              v.textContent = "The two-year window has passed; a delay must be explained.";
              v.className = "result__verdict is-yes";
            }
            document.getElementById("ff-out").innerHTML = [
              row("Forum", forum),
              row("File online", "e-Daakhil"),
              row("Last date", dmy(lastDay), true),
            ].join("");
            document.getElementById("ff-note").textContent =
              today <= lastDay
                ? "Send a written complaint to the seller first and keep the bills and messages. A complaint can be filed where you live or work."
                : "The Commission can admit a late complaint if it accepts the reason for the delay.";
          };
          ff.addEventListener("input", function () {
            trackUse("consumer_forum");
            renderForum();
          });
          ff.addEventListener("change", renderForum);
          renderForum();
        }
      })();
    </script>
