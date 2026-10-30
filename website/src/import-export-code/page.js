    <script>
      /* Import Export Code: live IEC calendar, "do I need an IEC" checker, annual update checker (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* IEC under Section 7 of the Foreign Trade (Development and Regulation) Act, 1992; annual update with DGFT between 1 April and 30 June,
           failing which the IEC can be deactivated (reactivated on updating). GSTR-1 by the 11th for monthly filers; LUT for each financial
           year before exports without IGST. */
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
        /* The update window that applies now: this year's if 1 April has passed, else last year's */
        function windowYear(today) {
          return today >= new Date(today.getFullYear(), 3, 1) ? today.getFullYear() : today.getFullYear() - 1;
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
          window.dataLayer.push({ event: "calculator_use", service: "import-export-code", tool: tool });
        }
        function row(label, value, total) {
          return "<div" + (total ? ' class="is-total"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }

        /* ---- Live IEC calendar ---- */
        function tick() {
          var now = new Date(), today = day(now), y = today.getFullYear();
          var open = new Date(y, 3, 1), close = new Date(y, 5, 30);
          var inWindow = today >= open && today <= close;
          if (today > close) {
            open = new Date(y + 1, 3, 1);
            close = new Date(y + 1, 5, 30);
          }
          var target = inWindow ? new Date(close.getFullYear(), 5, 30, 23, 59, 59) : open;
          setText("[data-iec-open]", dmy(open));
          setText("[data-iec-close]", dmy(close));
          setText("[data-iec-label]", inWindow ? "This year’s IEC update window closes in" : "The next IEC update window opens in");
          setText("[data-iec-sub]", "Window: " + dmy(open) + " to " + dmy(close) + ".");
          var g1 = new Date(y, today.getMonth(), 11);
          if (g1 < today) g1 = new Date(y, today.getMonth() + 1, 11);
          var gm = new Date(g1.getFullYear(), g1.getMonth() - 1, 1);
          setText("[data-gstr1-by]", dmy(g1));
          setText("[data-gstr1-label]", "Report " + MONTHS[gm.getMonth()] + " " + gm.getFullYear() + " export invoices in GSTR-1 by");
          var fy = today.getMonth() >= 3 ? y + 1 : y;
          setText("[data-lut-label]", "Your LUT for FY " + fy + "-" + String(fy + 1).slice(2) + " should be in place before exports from");
          setText("[data-lut-by]", dmy(new Date(fy, 3, 1)));
          var ms = Math.max(0, target - now);
          var parts = [Math.floor(ms / 86400000), Math.floor(ms / 3600000) % 24, Math.floor(ms / 60000) % 60, Math.floor(ms / 1000) % 60];
          var box = document.querySelector("[data-cd='iec']");
          if (box) {
            var b = box.querySelectorAll("b");
            parts.forEach(function (v, i) {
              var t = pad(v);
              if (b[i] && b[i].textContent !== t) b[i].textContent = t;
            });
            box.setAttribute("aria-label", parts[0] + " days " + parts[1] + " hours " + (inWindow ? "until the IEC update window closes" : "until the IEC update window opens"));
          }
        }
        if (document.getElementById("live")) {
          tick();
          window.setInterval(tick, 1000);
        }

        /* ---- Do I need an IEC? ---- */
        var ACTS = {
          export: [true, "Yes, you need an IEC.", "Next: ICEGATE registration, and a LUT if you’ll export without paying IGST."],
          import: [true, "Yes, you need an IEC.", "Customs will ask for the IEC in your bill of entry. Register on ICEGATE to track it."],
          services: [null, "", ""],
          personal: [false, "No IEC needed for personal use.", "The exemption covers goods not connected with trade, manufacture or agriculture. Commercial quantities need an IEC."],
        };
        var nc = document.getElementById("need-check");
        if (nc) {
          var renderNeed = function () {
            var act = nc.querySelector("[name='activity']").value, benefits = nc.querySelector("[name='benefits']").checked;
            var need = ACTS[act][0], verdict = ACTS[act][1], note = ACTS[act][2];
            if (act === "services") {
              need = benefits ? true : "advised";
              verdict = benefits ? "Yes, get an IEC to claim FTP benefits." : "Recommended for service exporters.";
              note = "Service exporters generally need an IEC to claim Foreign Trade Policy benefits, and banks may ask for it on export receipts.";
            } else if (benefits && need) {
              note += " Export benefits under the Foreign Trade Policy are claimed against your IEC.";
            }
            var v = document.getElementById("nc-verdict");
            v.textContent = verdict;
            v.className = "result__verdict " + (need === false ? "is-no" : "is-yes");
            document.getElementById("nc-out").innerHTML = [
              row("IEC required", need === true ? "Yes" : need === false ? "No" : "Advised"),
              row("Issued by", "DGFT"),
              row("Sign with", "DSC or e-sign", true),
            ].join("");
            document.getElementById("nc-note").textContent = note;
          };
          nc.addEventListener("change", function () {
            trackUse("iec_need");
            renderNeed();
          });
          renderNeed();
        }

        /* ---- Annual update checker ---- */
        var uc = document.getElementById("update-check");
        if (uc) {
          var lastIn = uc.querySelector("[name='lastupdate']");
          var t0 = day(new Date());
          lastIn.value = isoDate(new Date(windowYear(t0) - 1, 4, 15));
          var renderUpd = function () {
            var last = parse(lastIn.value), today = day(new Date());
            if (!last) return;
            var y = windowYear(today);
            var open = new Date(y, 3, 1), close = new Date(y, 5, 30), nextOpen = new Date(y + 1, 3, 1);
            var v = document.getElementById("uc-verdict"), rows = [], note = "";
            if (last >= open) {
              v.textContent = "Up to date. Next update from " + dmy(nextOpen) + ".";
              v.className = "result__verdict is-no";
              rows.push(row("Status", "Active"));
              rows.push(row("Next window", MONTHS[3] + "–" + MONTHS[5] + " " + (y + 1), true));
              note = "Update again in the next window even if nothing changes.";
            } else if (today <= close) {
              var left = Math.round((close - today) / 86400000);
              v.textContent = "Update due by " + dmy(close) + ": " + left + (left === 1 ? " day" : " days") + " left.";
              v.className = "result__verdict is-yes";
              rows.push(row("Status", "Update pending"));
              rows.push(row("Window closes", dmy(close), true));
              note = "Confirm or update your details on the DGFT portal before the window closes.";
            } else {
              v.textContent = "The " + y + " update window was missed. Your IEC may be deactivated.";
              v.className = "result__verdict is-yes";
              rows.push(row("Status", "Likely deactivated"));
              rows.push(row("Missed window", "Apr–Jun " + y));
              rows.push(row("What to do", "Update now", true));
              note = "Completing the pending update on the DGFT portal allows the IEC to be reactivated. Check the status before your next shipment.";
            }
            rows.unshift(row("Last updated", dmy(last)));
            document.getElementById("uc-out").innerHTML = rows.join("");
            document.getElementById("uc-note").textContent = note;
          };
          uc.addEventListener("input", function () {
            trackUse("iec_update");
            renderUpd();
          });
          uc.addEventListener("change", renderUpd);
          renderUpd();
        }
      })();
    </script>
