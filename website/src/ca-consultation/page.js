    <script>
      /* CA consultation: live tax dates, consultation finder, advance tax calculator (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Advance tax under the Income-tax Act, 2025 when the year's tax after TDS and TCS is ₹10,000 or more: 15%, 45%, 75% and 100% by
           15 June, 15 September, 15 December and 15 March; presumptive taxpayers pay 100% by 15 March; resident senior citizens without business
           income are exempt. GSTR-3B for monthly filers by the 20th of the next month. Updated return within 48 months from the end of the
           assessment year (FY 2025-26 → 31 March 2031). */
        var STEPS = [[6, 15, 0.15], [9, 15, 0.45], [12, 15, 0.75], [3, 15, 1]];
        var ORD = ["1st", "2nd", "3rd", "4th"];
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function day(d) {
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function inr(n) {
          return "₹" + Math.round(n).toLocaleString("en-IN");
        }
        function num(el) {
          return Math.max(0, Number(el.value) || 0);
        }
        function fyStart(d) {
          return d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1;
        }
        function schedule(start) {
          return STEPS.map(function (s, i) {
            return { date: new Date(i === 3 ? start + 1 : start, s[0] - 1, s[1]), share: s[2], n: i };
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
          window.dataLayer.push({ event: "calculator_use", service: "ca-consultation", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        function nextInstalment(today) {
          var start = fyStart(today);
          var list = schedule(start).concat(schedule(start + 1));
          return list.filter(function (s) {
            return s.date >= today;
          })[0];
        }

        /* ---- Live tax dates ---- */
        function tick() {
          var now = new Date(), today = day(now);
          var next = nextInstalment(today);
          var end = new Date(next.date.getFullYear(), next.date.getMonth(), next.date.getDate(), 23, 59, 59);
          setText("[data-adv-due]", dmy(next.date));
          setText("[data-adv-label]", "The " + ORD[next.n] + " advance tax instalment (" + Math.round(next.share * 100) + "%) is due in");
          setText("[data-adv-last]", dmy(new Date(fyStart(today) + 1, 2, 15)));
          var gst = new Date(today.getFullYear(), today.getMonth(), 20);
          if (gst < today) gst = new Date(today.getFullYear(), today.getMonth() + 1, 20);
          setText("[data-gst-by]", dmy(gst));
          var gstFor = new Date(gst.getFullYear(), gst.getMonth() - 1, 1);
          setText("[data-gst-label]", "GSTR-3B for " + MONTHS[gstFor.getMonth()] + " " + gstFor.getFullYear() + " is due by");
          var last = fyStart(today) - 1;
          setText("[data-itru-label]", "An updated return for FY " + last + "-" + String(last + 1).slice(2) + " can be filed until");
          setText("[data-itru-by]", "31 Mar " + (last + 6));
          var ms = Math.max(0, end - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='advtax']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours until the next advance tax instalment");
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Consultation finder ---- */
        var TOPICS = {
          itr: ["Income tax return", "your Form 16, annual information statement and bank interest certificates"],
          gains: ["Capital gains", "sale and purchase papers and broker statements"],
          gst: ["GST", "your GSTIN, recent returns and invoices"],
          business: ["Starting a business", "your business plan, partners and expected turnover"],
          notice: ["Tax notice", "the notice and the return it refers to"],
          nri: ["NRI taxation", "your days in India and your foreign and Indian income"],
        };
        var cf = document.getElementById("consult-finder");
        if (cf) {
          var renderFind = function () {
            var topic = cf.querySelector("[name='topic']").value;
            var multi = cf.querySelector("[name='multi']").checked, foreign = cf.querySelector("[name='foreign']").checked;
            var ongoing = cf.querySelector("[name='ongoing']").checked;
            var plan, mode, length;
            if (ongoing) {
              plan = "Advisory Plan"; mode = "Calls, WhatsApp and email"; length = "Two calls a month";
            } else if (multi || foreign || topic === "gains" || topic === "notice" || topic === "nri" || topic === "business") {
              plan = "Expert Consultation"; mode = "Video call"; length = "60 minutes";
            } else {
              plan = "Quick Call"; mode = "Phone call"; length = "30 minutes";
            }
            var v = document.getElementById("cf-verdict");
            v.textContent = "Best fit: " + plan + ".";
            v.className = "result__verdict is-no";
            document.getElementById("cf-out").innerHTML = [
              row("Topic", TOPICS[topic][0]),
              row("Format", mode),
              row("Length", length, true),
            ].join("");
            document.getElementById("cf-note").textContent =
              "Keep ready: PAN, your question, and " + TOPICS[topic][1] + (foreign ? ", plus foreign income and asset details." : ".");
          };
          cf.addEventListener("change", function () {
            trackUse("consult_finder");
            renderFind();
          });
          renderFind();
        }

        /* ---- Advance tax calculator ---- */
        var ac = document.getElementById("adv-calc");
        if (ac) {
          var renderAdv = function () {
            var tax = num(ac.querySelector("[name='tax']")), tds = num(ac.querySelector("[name='tds']")), paid = num(ac.querySelector("[name='paid']"));
            var presumptive = ac.querySelector("[name='presumptive']").checked, senior = ac.querySelector("[name='senior']").checked;
            var net = Math.max(0, tax - tds);
            var v = document.getElementById("ac-verdict"), rows = [row("Tax after TDS and TCS", inr(net))], note = "";
            var today = day(new Date());
            if (senior) {
              v.textContent = "No advance tax: resident seniors without business income are exempt.";
              v.className = "result__verdict is-no";
              rows.push(row("Pay instead", "Self-assessment tax", true));
              note = "Pay any balance as self-assessment tax before filing the return.";
            } else if (net < 10000) {
              v.textContent = "No advance tax: your tax after TDS is under ₹10,000.";
              v.className = "result__verdict is-no";
              rows.push(row("Advance tax", "Not required", true));
              note = "Recheck if your income changes during the year.";
            } else {
              var plan = schedule(2026).filter(function (s) {
                return !presumptive || s.n === 3;
              });
              plan.forEach(function (s) {
                rows.push(row("By " + dmy(s.date), inr(net * s.share) + " total"));
              });
              var due = plan.filter(function (s) {
                return s.date < today;
              });
              var dueNow = due.length ? net * due[due.length - 1].share : 0;
              var short = Math.max(0, dueNow - paid);
              var nextS = plan.filter(function (s) {
                return s.date >= today;
              })[0];
              var nextGap = nextS ? Math.max(0, net * nextS.share - paid) : 0;
              if (short > 0) {
                v.textContent = "Shortfall of " + inr(short) + " on instalments already due. Pay now to limit interest.";
                v.className = "result__verdict is-yes";
              } else {
                v.textContent = nextS ? "On track. Pay " + inr(nextGap) + " more by " + dmy(nextS.date) + "." : "All instalments for tax year 2026-27 have passed.";
                v.className = "result__verdict is-no";
              }
              rows.push(row(nextS ? "Pay by " + dmy(nextS.date) : "Balance", inr(nextS ? nextGap : Math.max(0, net - paid)), true));
              note = (presumptive ? "Presumptive taxpayers may pay the whole amount by 15 March. " : "") + "Shortfalls attract interest under Sections 424 and 425 of the Income-tax Act, 2025.";
            }
            document.getElementById("ac-out").innerHTML = rows.join("");
            document.getElementById("ac-note").textContent = note;
          };
          ac.addEventListener("input", function () {
            trackUse("advance_tax");
            renderAdv();
          });
          ac.addEventListener("change", renderAdv);
          renderAdv();
        }
      })();
    </script>
