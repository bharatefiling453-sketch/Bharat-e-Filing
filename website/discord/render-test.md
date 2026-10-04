# Render test for the blog pipeline

Upload this file like a blog post, open the page, and report which numbered lines show their colour:

<div><b>1. RAW HTML:</b> this line is bold. If you see angle brackets like &lt;div&gt; on the page, raw HTML is switched off.</div>

<div style="background:#102161;color:#ffffff;padding:8px;font-weight:700">2. INLINE STYLE: navy box with white text</div>

<style>.bef-test-class{background:#ff8813;color:#102161;padding:8px;font-weight:700}</style>

<div class="bef-test-class">3. STYLE TAG + CLASS: orange box with navy text</div>

<div id="bef-test-script" style="padding:8px;font-weight:700">4. SCRIPT: this text should change to green "SCRIPTS RUN"</div>

<script>var e=document.getElementById("bef-test-script");e.textContent="4. SCRIPT: SCRIPTS RUN";e.style.background="#3c8c31";e.style.color="#fff";</script>

<div style="font-family:Inter,sans-serif;font-size:22px">5. FONT: this line is in the Inter font if fonts load</div>
