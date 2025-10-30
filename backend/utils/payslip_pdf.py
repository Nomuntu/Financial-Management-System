from weasyprint import HTML, CSS
from jinja2 import Template
from datetime import datetime

HTML_TEMPLATE = Template("""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    body { font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 24px; color: #222; }
    .title { text-align: center; font-size: 16px; font-weight: bold; }
    .subtitle { text-align: center; font-size: 13px; margin-bottom: 18px; }
    .block { border-top: 2px solid #000; border-bottom: 2px solid #000; padding: 8px 0; margin-top: 8px; }
    .row { display: flex; justify-content: space-between; margin: 2px 0; }
    .label { width: 180px; color: #444; }
    .val { flex: 1; text-align: left; }
    .line { display:flex; justify-content: space-between; margin: 2px 0; }
    .total { border-top: 1px dashed #666; margin-top: 6px; padding-top: 6px; font-weight: bold; }
    .net { border-top: 2px solid #000; margin-top: 10px; padding-top: 8px; font-weight: bold; font-size: 13px; }
    .footer { margin-top: 16px; font-size: 10px; color:#555; display:flex; justify-content: space-between; }
    .mono { font-family: ui-monospace, Menlo, Consolas, 'Courier New', monospace; }
  </style>
</head>
<body>
  <div class="title">{{ company_name }}</div>
  <div class="subtitle">EMPLOYEE PAYSLIP – {{ period_label }}</div>

  <div class="block">
    <div class="row"><div class="label">Employee No</div><div class="val mono">{{ employee_number }}</div></div>
    <div class="row"><div class="label">Employee Name</div><div class="val">{{ employee_name }}</div></div>
    {% if department %}<div class="row"><div class="label">Department</div><div class="val">{{ department }}</div></div>{% endif %}
    {% if position %}<div class="row"><div class="label">Position</div><div class="val">{{ position }}</div></div>{% endif %}
    <div class="row"><div class="label">Pay Frequency</div><div class="val">{{ pay_frequency }}</div></div>
    <div class="row"><div class="label">Period</div><div class="val">{{ period_start }} to {{ period_end }}</div></div>
  </div>

  <div class="block">
    <div class="line"><div>EARNINGS</div><div class="mono">Amount (ZAR)</div></div>
    <div class="line"><div>Basic Salary</div><div class="mono">{{ gross_pay }}</div></div>
  </div>

  <div class="block">
    <div class="line"><div>DEDUCTIONS</div><div class="mono">Amount (ZAR)</div></div>
    {% if include_paye %}<div class="line"><div>PAYE ({{ paye_rate }}%)</div><div class="mono">{{ paye }}</div></div>{% endif %}
    {% if include_uif %}<div class="line"><div>UIF ({{ uif_rate }}%)</div><div class="mono">{{ uif }}</div></div>{% endif %}
    {% if include_pension %}<div class="line"><div>Pension ({{ pension_rate }}%)</div><div class="mono">{{ pension }}</div></div>{% endif %}
    <div class="line total"><div>Total Deductions</div><div class="mono">{{ deductions }}</div></div>
    <div class="line net"><div>NET PAY</div><div class="mono">{{ net_pay }}</div></div>
  </div>

  <div class="footer">
    <div>Generated: {{ generated_at }}</div>
    <div>Company: {{ company_name }}</div>
  </div>
</body>
</html>
""")

def render_payslip_pdf(context: dict) -> bytes:
    html = HTML_TEMPLATE.render(**context)
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(string="")])
    return pdf
