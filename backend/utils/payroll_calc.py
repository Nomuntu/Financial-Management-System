from decimal import Decimal

def calculate_pay(gross, include_paye=True, include_uif=True, include_pension=True,
                  paye_rate=Decimal('18.0'), uif_rate=Decimal('1.0'), pension_rate=Decimal('5.0')):
    gross = Decimal(str(gross))
    paye = gross * (Decimal(paye_rate) / Decimal('100')) if include_paye else Decimal('0')
    uif = gross * (Decimal(uif_rate) / Decimal('100')) if include_uif else Decimal('0')
    pension = gross * (Decimal(pension_rate) / Decimal('100')) if include_pension else Decimal('0')
    deductions = paye + uif + pension
    net = gross - deductions
    return {
        "gross": float(gross),
        "paye": float(paye),
        "uif": float(uif),
        "pension": float(pension),
        "deductions": float(deductions),
        "net": float(net)
    }
