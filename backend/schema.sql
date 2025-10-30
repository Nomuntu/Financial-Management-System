-- Minimal schema creation for SQLite; for Postgres, use SERIAL/BIGSERIAL as needed
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS payroll_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    pay_frequency_default TEXT DEFAULT 'monthly',
    include_paye BOOLEAN DEFAULT 1,
    include_uif BOOLEAN DEFAULT 1,
    include_pension BOOLEAN DEFAULT 1,
    paye_rate REAL DEFAULT 18.0,
    uif_rate REAL DEFAULT 1.0,
    pension_rate REAL DEFAULT 5.0,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    employee_number TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    position TEXT,
    department TEXT,
    salary REAL,
    bank_name TEXT,
    account_number TEXT,
    pay_frequency TEXT DEFAULT 'monthly',
    active BOOLEAN DEFAULT 1,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS payslips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    employee_id INTEGER,
    period_start DATE,
    period_end DATE,
    gross_pay REAL,
    paye REAL,
    uif REAL,
    pension REAL,
    deductions REAL,
    net_pay REAL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
