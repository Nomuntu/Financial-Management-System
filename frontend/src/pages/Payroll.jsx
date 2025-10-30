import React, { useEffect, useState } from 'react'
import { get, post, put } from '../api/client'

export default function Payroll(){
  const [settings, setSettings] = useState(null)
  const [employees, setEmployees] = useState([])
  const [employee_id, setEmployeeId] = useState('')
  const [period_start, setStart] = useState('')
  const [period_end, setEnd] = useState('')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  async function load(){
    try{
      setSettings(await get('/payroll/settings'))
      setEmployees(await get('/payroll/employees'))
    }catch(e){ setErr(String(e)) }
  }
  useEffect(()=>{ load() }, [])

  const saveSettings = async ()=>{
    try{
      const res = await put('/payroll/settings', settings)
      setSettings(res); setMsg('Settings saved')
    }catch(e){ setErr(String(e)) }
  }

  const run = async ()=>{
    try{
      const res = await post('/payroll/payslips/generate', { employee_id: Number(employee_id), period_start, period_end })
      setMsg('Payslip generated')
      setErr('')
    }catch(e){ setErr(String(e)) }
  }

  if(!settings) return <div style={{padding:16}}>Loading...</div>

  return (
    <div style={{padding:16}}>
      <h2>Payroll</h2>

      <h3>Settings</h3>
      <div style={{display:'grid', gridTemplateColumns:'repeat(3, minmax(240px, 1fr))', gap:8}}>
        <label><input type="checkbox" checked={!!settings.include_paye} onChange={e=>setSettings({...settings, include_paye:e.target.checked})}/> Include PAYE</label>
        <label><input type="checkbox" checked={!!settings.include_uif} onChange={e=>setSettings({...settings, include_uif:e.target.checked})}/> Include UIF</label>
        <label><input type="checkbox" checked={!!settings.include_pension} onChange={e=>setSettings({...settings, include_pension:e.target.checked})}/> Include Pension</label>
        <label>PAYE % <input value={settings.paye_rate} onChange={e=>setSettings({...settings, paye_rate:e.target.value})}/></label>
        <label>UIF % <input value={settings.uif_rate} onChange={e=>setSettings({...settings, uif_rate:e.target.value})}/></label>
        <label>Pension % <input value={settings.pension_rate} onChange={e=>setSettings({...settings, pension_rate:e.target.value})}/></label>
        <label>Default Frequency
          <select value={settings.pay_frequency_default} onChange={e=>setSettings({...settings, pay_frequency_default:e.target.value})}>
            <option value="monthly">Monthly</option>
            <option value="weekly">Weekly</option>
            <option value="biweekly">Biweekly</option>
          </select>
        </label>
        <button onClick={saveSettings}>Save Settings</button>
      </div>

      <h3 style={{marginTop:24}}>Generate Payslip</h3>
      <div style={{display:'grid', gridTemplateColumns:'repeat(3, minmax(240px, 1fr))', gap:8}}>
        <select value={employee_id} onChange={e=>setEmployeeId(e.target.value)}>
          <option value="">Select employee</option>
          {employees.map(e=>(<option key={e.id} value={e.id}>{e.employee_number} — {e.name}</option>))}
        </select>
        <input type="date" value={period_start} onChange={e=>setStart(e.target.value)} />
        <input type="date" value={period_end} onChange={e=>setEnd(e.target.value)} />
        <button onClick={run}>Generate</button>
      </div>

      {msg && <p style={{color:'green'}}>{msg}</p>}
      {err && <p style={{color:'red'}}>{err}</p>}
    </div>
  )
}
