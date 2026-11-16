    <script>
      /* GST revocation (v3): deadline planner and plan pre-selection (no dependencies) */
      (function () {
        "use strict";
        var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        /* Rule 23(1): apply in REG-21 within 90 days of service of the cancellation order, extendable by up to 180 days by the
           Commissioner. Section 107: appeal within 3 months of the order, plus 1 month on sufficient cause. */
        function dmy(d) {
          return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
        }
        function pad(n) {
          return String(n).padStart(2, "0");
        }
        function addDays(from, n) {
          return new Date(from.getFullYear(), from.getMonth(), from.getDate() + n);
        }
        function addMonths(from, n) {
          var d = new Date(from.getFullYear(), from.getMonth() + n, 1);
          var last = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
          d.setDate(Math.min(from.getDate(), last));
          return d;
        }
        function row(label, value, cls) {
          return "<div" + (cls ? ' class="' + cls + '"' : "") + "><dt>" + label + "</dt><dd>" + value + "</dd></div>";
        }
        var used = false;

        /* ---- Deadline planner ---- */
        var rp = document.getElementById("revoke-plan");
        if (rp) {
          var input = rp.querySelector("[name='date']");
          var t = new Date();
          input.value = t.getFullYear() + "-" + pad(t.getMonth() + 1) + "-" + pad(t.getDate());
          var render = function () {
            var p = (input.value || "").split("-");
            if (p.length < 3) return;
            var d = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
            document.getElementById("rp-out").innerHTML = [
              row("Apply in REG-21 by", dmy(addDays(d, 90)), "is-total mark-leaf"),
              row("With an extension, by", dmy(addDays(d, 270)), "mark-saffron"),
              row("Appeal in APL-01 by", dmy(addMonths(d, 3)), "mark-line"),
              row("Late appeal, by", dmy(addMonths(d, 4)), "mark-line"),
            ].join("");
          };
          rp.addEventListener("input", function () {
            if (!used) {
              used = true;
              window.dataLayer = window.dataLayer || [];
              window.dataLayer.push({ event: "calculator_use", service: "gst-revocation", tool: "revocation_deadline_planner" });
            }
            render();
          });
          rp.addEventListener("change", render);
          render();
        }

        /* ---- Floating WhatsApp card: minimise to the round button (remembered for the session) ---- */
        var waFloat = document.querySelector("[data-wa-float]");
        if (waFloat) {
          try {
            if (sessionStorage.getItem("bef_wa_min") === "1") waFloat.classList.add("is-min");
          } catch (err) {
            /* storage blocked: card stays open */
          }
          var minBtn = waFloat.querySelector("[data-wa-min]");
          if (minBtn)
            minBtn.addEventListener("click", function () {
              waFloat.classList.add("is-min");
              try {
                sessionStorage.setItem("bef_wa_min", "1");
              } catch (err) {
                /* ignore */
              }
            });
        }

        /* ---- Pricing buttons pre-select the plan in the contact form ---- */
        var planSelect = document.getElementById("f-plan");
        document.querySelectorAll("a[data-plan]").forEach(function (a) {
          a.addEventListener("click", function () {
            if (planSelect) planSelect.value = a.getAttribute("data-plan");
          });
        });
      })();
    </script>
