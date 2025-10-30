export const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export const authHeader = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

async function handle(res){
  if(!res.ok){
    const t = await res.text();
    throw new Error(t || res.statusText);
  }
  const ct = res.headers.get('content-type') || '';
  return ct.includes('application/json') ? res.json() : res.text();
}

export async function get(path){
  const res = await fetch(`${API_BASE}${path}`, { headers: { ...authHeader() } });
  return handle(res);
}

export async function post(path, body){
  const res = await fetch(`${API_BASE}${path}`, {
    method:'POST',
    headers: { 'Content-Type':'application/json', ...authHeader() },
    body: JSON.stringify(body || {})
  });
  return handle(res);
}
