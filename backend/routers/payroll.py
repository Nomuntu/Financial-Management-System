from fastapi import APIRouter, Depends, Header, HTTPException, Response
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime
from decimal import Decimal
from database import get_db
import models, schemas
from utils.payroll_calc import calculate_pay
from utils.payslip_pdf import render_payslip_pdf

ALGORITHM = "HS256"
SECRET_KEY = "replace-this-with-a-strong-secret"

router = APIRouter()

def get_token_payload(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Payroll settings
@router.get("/settings", response_model=schemas.PayrollSettingsOut)
def get_settings(db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    s = db.query(models.PayrollSettings).filter(models.PayrollSettings.organization_id == org_id).first()
    if not s:
        # default
        s = models.PayrollSettings(organization_id=org_id)
        db.add(s); db.commit(); db.refresh(s)
    return {
        "pay_frequency_default": s.pay_frequency_default,
        "include_paye": s.include_paye,
        "include_uif": s.include_uif,
        "include_pension": s.include_pension,
        "paye_rate": float(s.paye_rate or 18.0),
        "uif_rate": float(s.uif_rate or 1.0),
        "pension_rate": float(s.pension_rate or 5.0),
    }

@router.put("/settings", response_model=schemas.PayrollSettingsOut)
def update_settings(data: schemas.PayrollSettingsIn, db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    s = db.query(models.PayrollSettings).filter(models.PayrollSettings.organization_id == org_id).first()
    if not s:
        s = models.PayrollSettings(organization_id=org_id)
        db.add(s)
    for k, v in data.dict(exclude_unset=True).items():
        setattr(s, k, v)
    db.commit(); db.refresh(s)
    return {
        "pay_frequency_default": s.pay_frequency_default,
        "include_paye": s.include_paye,
        "include_uif": s.include_uif,
        "include_pension": s.include_pension,
        "paye_rate": float(s.paye_rate or 18.0),
        "uif_rate": float(s.uif_rate or 1.0),
        "pension_rate": float(s.pension_rate or 5.0),
    }

# Employees
@router.get("/employees", response_model=list[schemas.EmployeeOut])
def list_employees(db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    rows = db.query(models.Employee).filter(models.Employee.organization_id == org_id, models.Employee.active == True).all()
    return rows

@router.post("/employees", response_model=schemas.EmployeeOut)
def create_employee(data: schemas.EmployeeIn, db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    # uniqueness on employee_number per organization simulated via global unique for MVP
    exists = db.query(models.Employee).filter(models.Employee.employee_number == data.employee_number).first()
    if exists:
        raise HTTPException(status_code=400, detail="Employee number already exists")
    row = models.Employee(
        organization_id=org_id,
        employee_number=data.employee_number,
        name=data.name,
        email=data.email,
        position=data.position,
        department=data.department,
        salary=data.salary,
        bank_name=data.bank_name,
        account_number=data.account_number,
        pay_frequency=data.pay_frequency or "monthly"
    )
    db.add(row); db.commit(); db.refresh(row)
    return row

# Payslips
@router.post("/payslips/generate", response_model=schemas.PayslipOut)
def generate_payslip(data: schemas.PayslipGenerateIn, db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    emp = db.query(models.Employee).filter(models.Employee.id == data.employee_id, models.Employee.organization_id == org_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    settings = db.query(models.PayrollSettings).filter(models.PayrollSettings.organization_id == org_id).first()
    if not settings:
        settings = models.PayrollSettings(organization_id=org_id)
        db.add(settings); db.commit(); db.refresh(settings)

    calc = calculate_pay(
        gross=emp.salary,
        include_paye=settings.include_paye,
        include_uif=settings.include_uif,
        include_pension=settings.include_pension,
        paye_rate=settings.paye_rate or 18.0,
        uif_rate=settings.uif_rate or 1.0,
        pension_rate=settings.pension_rate or 5.0
    )

    p = models.Payslip(
        organization_id=org_id,
        employee_id=emp.id,
        period_start=data.period_start,
        period_end=data.period_end,
        gross_pay=calc["gross"],
        paye=calc["paye"],
        uif=calc["uif"],
        pension=calc["pension"],
        deductions=calc["deductions"],
        net_pay=calc["net"],
    )
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/payslips", response_model=list[schemas.PayslipOut])
def list_payslips(db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    rows = db.query(models.Payslip).filter(models.Payslip.organization_id == org_id).order_by(models.Payslip.id.desc()).all()
    return rows

@router.get("/payslips/{payslip_id}/pdf")
def payslip_pdf(payslip_id: int, db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    p = db.query(models.Payslip).filter(models.Payslip.id == payslip_id, models.Payslip.organization_id == org_id).first()
    if not p: raise HTTPException(status_code=404, detail="Payslip not found")
    emp = db.query(models.Employee).filter(models.Employee.id == p.employee_id).first()
    settings = db.query(models.PayrollSettings).filter(models.PayrollSettings.organization_id == org_id).first()

    company_name = "Company"  # Replace with organization settings table when available
    period_label = p.period_start.strftime("%b %Y")
    ctx = {
        "company_name": company_name,
        "period_label": period_label,
        "employee_number": emp.employee_number,
        "employee_name": emp.name,
        "department": emp.department or "",
        "position": emp.position or "",
        "pay_frequency": emp.pay_frequency or (settings.pay_frequency_default if settings else "monthly"),
        "period_start": p.period_start.strftime("%Y-%m-%d"),
        "period_end": p.period_end.strftime("%Y-%m-%d"),
        "gross_pay": f"{float(p.gross_pay):,.2f}",
        "include_paye": settings.include_paye if settings else True,
        "include_uif": settings.include_uif if settings else True,
        "include_pension": settings.include_pension if settings else True,
        "paye_rate": f"{float(settings.paye_rate):.2f}" if settings and settings.paye_rate is not None else "18.00",
        "uif_rate": f"{float(settings.uif_rate):.2f}" if settings and settings.uif_rate is not None else "1.00",
        "pension_rate": f"{float(settings.pension_rate):.2f}" if settings and settings.pension_rate is not None else "5.00",
        "paye": f"{float(p.paye):,.2f}",
        "uif": f"{float(p.uif):,.2f}",
        "pension": f"{float(p.pension):,.2f}",
        "deductions": f"{float(p.deductions):,.2f}",
        "net_pay": f"{float(p.net_pay):,.2f}",
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    }
    pdf_bytes = render_payslip_pdf(ctx)
    fname = f"payslip_{emp.employee_number}_{period_label.replace(' ','_')}.pdf"
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f'inline; filename="{fname}"'})
