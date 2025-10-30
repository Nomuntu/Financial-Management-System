import React, { useState } from 'react'
import { post } from '../api/client'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState('')

  const onLogin = async ()=>{
    try{
      const res = await post('/auth/login', { email, password })
      localStorage.setItem('token', res.access_token)
      window.location.href = '/dashboard'
    }catch(e){ setErr(String(e)) }
  }

  return (
    <div style={{padding:16}}>
      <h2>Login</h2>
      <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} /><br/>
      <input placeholder='Password' type='password' value={password} onChange={e=>setPassword(e.target.value)} /><br/>
      <button onClick={onLogin}>Login</button>
      {err && <p style={{color:'red'}}>{err}</p>}
    </div>
  )
}
