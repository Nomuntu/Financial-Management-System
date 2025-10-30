// frontend/src/api/client.js

// Normalize base (remove trailing slashes)
const RAW_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_BASE = RAW_BASE.replace(/\/+$/, '');

// Join base + path safely: always exactly one slash
function urlFor(path) {
  const p = String(path || '').replace(/^\/+/, ''); // remove leading slashes
  return `${API_BASE}/${p}`;
}

export const authHeader = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

async function handle(res) {
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(text || res.statusText);
  }
  const ct = res.headers.get('content-type') || '';
  return ct.includes('application/json') ? res.json() : res.text();
}

export async function get(path) {
  const res = await fetch(urlFor(path), {
    headers: { ...authHeader() },
  });
  return handle(res);
}

export async function post(path, body) {
  const res = await fetch(urlFor(path), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeader() },
    body: JSON.stringify(body || {}),
  });
  return handle(res);
}

export async function put(path, body) {
  const res = await fetch(urlFor(path), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeader() },
    body: JSON.stringify(body || {}),
  });
  return handle(res);
}
