import React, { useEffect, useState } from 'react'
import { get } from '../api/client'

export default function Payslips(){
  const [rows, setRows] = useState([])
  const [err, setErr] = useState('')

  async function load(){ try{ setRows(await get('/payroll/payslips')) }catch(e){ setErr(String(e)) } }
  useEffect(()=>{ load() }, [])

  const openPdf = (id)=>{
    const base = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    window.open(`${base}/payroll/payslips/${id}/pdf`, '_blank')
  }

  return (
    <div style={{padding:16}}>
      <h2>Payslips</h2>
      {err && <p style={{color:'red'}}>{err}</p>}
      <table style={{width:'100%', borderCollapse:'collapse'}}>
        <thead><tr><th align="left">ID</th><th align="left">Employee</th><th>Period</th><th align="right">Gross</th><th align="right">Net</th><th></th></tr></thead>
        <tbody>
          {rows.map(r=>(
            <tr key={r.id} style={{borderTop:'1px solid #eee'}}>
              <td>{r.id}</td>
              <td>{r.employee_id}</td>
              <td>{r.period_start} → {r.period_end}</td>
              <td align="right">{Number(r.gross_pay).toFixed(2)}</td>
              <td align="right">{Number(r.net_pay).toFixed(2)}</td>
              <td><button onClick={()=>openPdf(r.id)}>PDF</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
