document.addEventListener("click", async (event) => {
  const copyButton = event.target.closest("[data-copy]");
  if (copyButton) {
    try {
      await navigator.clipboard.writeText(copyButton.dataset.copy || "");
      const previousText = copyButton.textContent;
      copyButton.textContent = "Copied";
      setTimeout(() => { copyButton.textContent = previousText; }, 1200);
    } catch (_error) {
      alert("Copy failed. Select and copy the text manually.");
    }
  }

  const toggleButton = event.target.closest("[data-toggle-secret]");
  if (toggleButton) {
    const secret = document.querySelector("[data-secret]");
    if (!secret) return;
    const original = secret.dataset.originalValue || secret.textContent;
    secret.dataset.originalValue = original;
    const isHidden = secret.dataset.hidden === "true";
    secret.textContent = isHidden ? original : "•".repeat(Math.min(original.length, 24));
    secret.dataset.hidden = isHidden ? "false" : "true";
  }
});

document.addEventListener("submit", (event) => {
  const form = event.target.closest("[data-confirm]");
  if (!form) return;
  if (!confirm(form.dataset.confirm || "Are you sure?")) {
    event.preventDefault();
  }
});

document.querySelectorAll("[data-secret]").forEach((secret) => {
  const original = secret.textContent;
  secret.dataset.originalValue = original;
  secret.textContent = "•".repeat(Math.min(original.length, 24));
  secret.dataset.hidden = "true";
});
