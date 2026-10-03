/**
 * Utility helper to download JSON data client-side in the browser.
 * 
 * @param {object} data - The raw JS object/array to download
 * @param {string} filename - The default filename for the download
 */
export function downloadJson(data, filename = "itr_draft_payload.json") {
  if (!data) return;
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
