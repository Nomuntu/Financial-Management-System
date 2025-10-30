from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

class PayrollSettings(Base):
    __tablename__ = "payroll_settings"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    pay_frequency_default = Column(String(20), default="monthly")
    include_paye = Column(Boolean, default=True)
    include_uif = Column(Boolean, default=True)
    include_pension = Column(Boolean, default=True)
    paye_rate = Column(Numeric(5,2), default=18.00)
    uif_rate = Column(Numeric(5,2), default=1.00)
    pension_rate = Column(Numeric(5,2), default=5.00)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    employee_number = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    position = Column(String(100))
    department = Column(String(100))
    salary = Column(Numeric(12,2))
    bank_name = Column(String(100))
    account_number = Column(String(100))
    pay_frequency = Column(String(20), default="monthly")
    active = Column(Boolean, default=True)

class Payslip(Base):
    __tablename__ = "payslips"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    period_start = Column(Date)
    period_end = Column(Date)
    gross_pay = Column(Numeric(12,2))
    paye = Column(Numeric(12,2))
    uif = Column(Numeric(12,2))
    pension = Column(Numeric(12,2))
    deductions = Column(Numeric(12,2))
    net_pay = Column(Numeric(12,2))
