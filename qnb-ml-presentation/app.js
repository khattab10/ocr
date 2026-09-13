(function () {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const total = slides.length;
  const countEl = document.getElementById("slideCount");
  const barEl = document.getElementById("progressBar");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  let index = 0;
  let locked = false;

  function render() {
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === index);
    });
    countEl.textContent = `${index + 1} / ${total}`;
    barEl.style.width = `${((index + 1) / total) * 100}%`;
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === total - 1;
    history.replaceState(null, "", `#${index + 1}`);
  }

  function go(to) {
    if (locked) return;
    const next = Math.max(0, Math.min(total - 1, to));
    if (next === index) return;
    locked = true;
    index = next;
    render();
    window.setTimeout(() => {
      locked = false;
    }, 420);
  }

  prevBtn.addEventListener("click", () => go(index - 1));
  nextBtn.addEventListener("click", () => go(index + 1));

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
      e.preventDefault();
      go(index + 1);
    } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
      e.preventDefault();
      go(index - 1);
    } else if (e.key === "Home") {
      e.preventDefault();
      go(0);
    } else if (e.key === "End") {
      e.preventDefault();
      go(total - 1);
    }
  });

  let touchX = null;
  document.addEventListener(
    "touchstart",
    (e) => {
      touchX = e.changedTouches[0].screenX;
    },
    { passive: true }
  );
  document.addEventListener(
    "touchend",
    (e) => {
      if (touchX === null) return;
      const dx = e.changedTouches[0].screenX - touchX;
      if (Math.abs(dx) > 50) go(index + (dx < 0 ? 1 : -1));
      touchX = null;
    },
    { passive: true }
  );

  const fromHash = parseInt(location.hash.replace("#", ""), 10);
  if (!Number.isNaN(fromHash) && fromHash >= 1 && fromHash <= total) {
    index = fromHash - 1;
  }

  render();
})();
