import React, { useEffect, useState } from 'react'
import { get, post } from '../api/client'

export default function Employees(){
  const [rows, setRows] = useState([])
  const [employee_number, setEmpNo] = useState('EMP001')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [position, setPosition] = useState('')
  const [department, setDepartment] = useState('')
  const [salary, setSalary] = useState('')
  const [pay_frequency, setFreq] = useState('monthly')
  const [err, setErr] = useState('')

  async function load(){ try{ setRows(await get('/payroll/employees')) }catch(e){ setErr(String(e)) } }
  useEffect(()=>{ load() }, [])

  const add = async ()=>{
    try{
      await post('/payroll/employees', { employee_number, name, email, position, department, salary: parseFloat(salary||0), pay_frequency })
      setEmpNo(''); setName(''); setEmail(''); setPosition(''); setDepartment(''); setSalary(''); setFreq('monthly')
      await load()
    }catch(e){ setErr(String(e)) }
  }

  return (
    <div style={{padding:16}}>
      <h2>Employees</h2>
      <div style={{display:'grid', gridTemplateColumns:'repeat(3, minmax(220px, 1fr))', gap:8}}>
        <input placeholder='Employee Number' value={employee_number} onChange={e=>setEmpNo(e.target.value)} />
        <input placeholder='Full name' value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder='Position' value={position} onChange={e=>setPosition(e.target.value)} />
        <input placeholder='Department' value={department} onChange={e=>setDepartment(e.target.value)} />
        <input placeholder='Salary' value={salary} onChange={e=>setSalary(e.target.value)} />
        <select value={pay_frequency} onChange={e=>setFreq(e.target.value)}>
          <option value="monthly">Monthly</option>
          <option value="weekly">Weekly</option>
          <option value="biweekly">Biweekly</option>
        </select>
        <button onClick={add}>Add Employee</button>
      </div>
      {err && <p style={{color:'red'}}>{err}</p>}
      <table style={{marginTop:12, width:'100%', borderCollapse:'collapse'}}>
        <thead><tr><th align="left">Emp No</th><th align="left">Name</th><th align="left">Dept</th><th align="left">Position</th><th align="right">Salary</th><th>Freq</th></tr></thead>
        <tbody>
          {rows.map(r=>(
            <tr key={r.id} style={{borderTop:'1px solid #eee'}}>
              <td>{r.employee_number}</td><td>{r.name}</td><td>{r.department||'-'}</td><td>{r.position||'-'}</td><td align="right">{Number(r.salary).toFixed(2)}</td><td>{r.pay_frequency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
