import React, { useState } from 'react';
import { post } from '../api/client';

export default function Register() {
  const [full_name, setFullName] = useState('');
  const [organization_name, setOrg] = useState('My Business');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');
  const [loading, setLoading] = useState(false);

  const onRegister = async (e) => {
    e?.preventDefault();
    setErr('');
    setMsg('');
    setLoading(true);
    try {
      await post('auth/register', {
        full_name,
        organization_name,
        email,
        password,
      });
      setMsg('Registered. You can now log in.');
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 16 }}>
      <h2>Register</h2>
      <form onSubmit={onRegister}>
        <input
          placeholder="Full name"
          value={full_name}
          onChange={(e) => setFullName(e.target.value)}
        /><br/>
        <input
          placeholder="Organization"
          value={organization_name}
          onChange={(e) => setOrg(e.target.value)}
        /><br/>
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /><br/>
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br/>
        <button type="submit" disabled={loading}>
          {loading ? 'Creating…' : 'Create Account'}
        </button>
      </form>

      {msg && <p style={{ color: 'green' }}>{msg}</p>}
      {err && <p style={{ color: 'red' }}>{err}</p>}
    </div>
  );
}
