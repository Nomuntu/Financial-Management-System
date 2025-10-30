import React, { useEffect, useState } from 'react'
import { get, post } from '../api/client'

export default function Customers(){
  const [rows, setRows] = useState([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [err, setErr] = useState('')

  async function load(){ try{ setRows(await get('/customers')) }catch(e){ setErr(String(e)) } }
  useEffect(()=>{ load() }, [])

  const add = async ()=>{
    try{
      await post('/customers', { name, email, phone })
      setName(''); setEmail(''); setPhone('')
      await load()
    }catch(e){ setErr(String(e)) }
  }

  return (
    <div style={{padding:16}}>
      <h2>Customers</h2>
      <div>
        <input placeholder='Name' value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder='Phone' value={phone} onChange={e=>setPhone(e.target.value)} />
        <button onClick={add}>Add</button>
      </div>
      {err && <p style={{color:'red'}}>{err}</p>}
      <ul>
        {rows.map(r=>(<li key={r.id}>{r.name} — {r.email || '-'} — {r.phone || '-'}</li>))}
      </ul>
    </div>
  )
}
