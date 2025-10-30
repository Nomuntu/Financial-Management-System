import React, { useState } from 'react'
import { post } from '../api/client'

export default function Register(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [full_name, setFullName] = useState('')
  const [organization_name, setOrg] = useState('My Business')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  const onRegister = async ()=>{
    try{
      await post('/auth/register', { email, password, full_name, organization_name })
      setMsg('Registered. You can now login.')
      setErr('')
    }catch(e){ setErr(String(e)); setMsg('') }
  }

  return (
    <div style={{padding:16}}>
      <h2>Register</h2>
      <input placeholder='Full name' value={full_name} onChange={e=>setFullName(e.target.value)} /><br/>
      <input placeholder='Organization' value={organization_name} onChange={e=>setOrg(e.target.value)} /><br/>
      <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} /><br/>
      <input placeholder='Password' type='password' value={password} onChange={e=>setPassword(e.target.value)} /><br/>
      <button onClick={onRegister}>Create Account</button>
      {msg && <p style={{color:'green'}}>{msg}</p>}
      {err && <p style={{color:'red'}}>{err}</p>}
    </div>
  )
}
