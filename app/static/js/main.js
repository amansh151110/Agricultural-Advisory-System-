const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const debounce = (fn, ms = 250) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };

const pages = {
  home() {
    let season = "";
    const apply = () => {
      const q = $("#q").value.trim().toLowerCase();
      let shown = 0;
      document.querySelectorAll(".row.crop").forEach((r) => {
        const ok = (!season || r.dataset.season === season) && (!q || r.dataset.name.includes(q));
        r.hidden = !ok; shown += ok;
      });
      $("#none").hidden = shown > 0;
    };
    $("#chips").addEventListener("click", (e) => {
      if (e.target.tagName !== "BUTTON") return;
      season = e.target.dataset.season;
      document.querySelectorAll("#chips button").forEach((b) => b.classList.toggle("on", b === e.target));
      apply();
    });
    $("#q").addEventListener("input", apply);
  },

  weather() {
    const params = new URLSearchParams(location.search);
    if (params.get("crop")) $("#crop").value = params.get("crop");
    const load = async () => {
      $("#wstatus").textContent = "Loading forecast…";
      try {
        const res = await fetch(`/api/advisory?city=${encodeURIComponent($("#city").value)}&crop=${$("#crop").value}`);
        const d = await res.json();
        if (!res.ok) throw new Error(d.error);
        $("#wstatus").textContent = d.source === "live" ? `Live forecast for ${d.city}.` : `Showing sample data for ${d.city} because the live forecast could not be reached.`;
        $("#advice").innerHTML = d.advice.map((a) => `<div class="tip ${a.level}">${esc(a.text)}</div>`).join("");
        $("#days").innerHTML = d.days.map((x) => `<div class="day ${x.rain >= 10 ? "wet" : ""}">
          <b>${new Date(x.date).toLocaleDateString("en-IN", { weekday: "short", day: "numeric" })}</b>
          <div class="t">${Math.round(x.tmax)}° <small class="muted">${Math.round(x.tmin)}°</small></div>
          <div>Rain ${x.rain} mm</div><div class="muted">Wind ${Math.round(x.wind)} km/h</div></div>`).join("");
      } catch (err) {
        $("#wstatus").textContent = "Could not load advice. Check your connection and try again.";
      }
    };
    $("#wform").addEventListener("submit", (e) => { e.preventDefault(); load(); });
    load();
  },

  doctor() {
    const search = debounce(async () => {
      const q = $("#dq").value.trim();
      if (q.length < 3) { $("#dres").innerHTML = ""; return; }
      const hits = await (await fetch(`/api/diseases?q=${encodeURIComponent(q)}`)).json();
      $("#dres").innerHTML = hits.length ? hits.map((h) => `<details class="prob" open><summary>${esc(h.name)} <small class="muted">on ${esc(h.crop)}</small></summary>
        <p><b>Look for:</b> ${esc(h.symptoms)}</p><p><b>Prevent:</b> ${esc(h.prevention)}</p><p><b>Treat:</b> ${esc(h.cure)}</p>
        <a href="/crop/${esc(h.crop_id)}">See the ${esc(h.crop)} guide</a></details>`).join("")
        : `<p class="muted">No match for "${esc(q)}". Try one or two plain words such as "spots", "holes" or "wilting".</p>`;
    });
    $("#dq").addEventListener("input", search);
  },
};
(pages[document.body.dataset.page] || (() => {}))();
