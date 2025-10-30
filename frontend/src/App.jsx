import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Customers from './pages/Customers'
import Employees from './pages/Employees'
import Payroll from './pages/Payroll'
import Payslips from './pages/Payslips'

export default function App(){
  return (
    <BrowserRouter>
      <nav style={{display:'flex', gap:12, padding:12, borderBottom:'1px solid #eee'}}>
        <Link to="/">Login</Link>
        <Link to="/register">Register</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/customers">Customers</Link>
        <Link to="/employees">Employees</Link>
        <Link to="/payroll">Payroll</Link>
        <Link to="/payslips">Payslips</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/dashboard" element={<Dashboard/>} />
        <Route path="/customers" element={<Customers/>} />
        <Route path="/employees" element={<Employees/>} />
        <Route path="/payroll" element={<Payroll/>} />
        <Route path="/payslips" element={<Payslips/>} />
      </Routes>
    </BrowserRouter>
  )
}
