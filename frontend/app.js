const out = document.getElementById('out');
const sidesInput = document.getElementById('sides');

function show(obj) {
  out.textContent = typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2);
}

async function roll() {
  const sides = Number(sidesInput.value);
  if (!Number.isFinite(sides) || sides < 2 || sides > 100) {
    show('Sides must be between 2 and 100.');
    return;
  }
  try {
    const res = await fetch(`/api/roll?sides=${encodeURIComponent(sides)}`);
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      show({ error: true, status: res.status, body });
      return;
    }
    show(body);
  } catch (e) {
    show(String(e));
  }
}

async function health() {
  try {
    const res = await fetch('/api/health');
    const body = await res.json().catch(() => ({}));
    show({ status: res.status, body });
  } catch (e) {
    show(String(e));
  }
}

document.getElementById('roll').addEventListener('click', () => void roll());
document.getElementById('health').addEventListener('click', () => void health());
