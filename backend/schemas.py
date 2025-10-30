from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    organization_name: Optional[str] = "My Organization"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class CustomerOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    class Config:
        orm_mode = True

class PayrollSettingsIn(BaseModel):
    pay_frequency_default: Optional[str] = "monthly"
    include_paye: Optional[bool] = True
    include_uif: Optional[bool] = True
    include_pension: Optional[bool] = True
    paye_rate: Optional[float] = 18.0
    uif_rate: Optional[float] = 1.0
    pension_rate: Optional[float] = 5.0

class PayrollSettingsOut(PayrollSettingsIn):
    pass

class EmployeeIn(BaseModel):
    employee_number: str
    name: str
    email: Optional[EmailStr] = None
    position: Optional[str] = None
    department: Optional[str] = None
    salary: float
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    pay_frequency: Optional[str] = "monthly"

class EmployeeOut(BaseModel):
    id: int
    employee_number: str
    name: str
    email: Optional[EmailStr] = None
    position: Optional[str] = None
    department: Optional[str] = None
    salary: float
    pay_frequency: Optional[str] = "monthly"
    class Config:
        orm_mode = True

class PayslipGenerateIn(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    notes: Optional[str] = None

class PayslipOut(BaseModel):
    id: int
    employee_id: int
    period_start: date
    period_end: date
    gross_pay: float
    paye: float
    uif: float
    pension: float
    deductions: float
    net_pay: float
    class Config:
        orm_mode = True
