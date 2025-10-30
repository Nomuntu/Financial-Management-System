# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from database import Base, engine
import auth
from routers import customers, payroll

app = FastAPI(title="FMS API (with Payroll)")

# ----- CORS (use your frontend URL; credentials allowed) -----
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "https://financial-management-system-frontend.onrender.com",  # change via env var if needed
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # must be a specific origin when allow_credentials=True
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- DB Tables (create on startup for SQLite; safe for Postgres too) -----
Base.metadata.create_all(bind=engine)

# ----- Routers -----
app.include_router(auth.router,      prefix="/auth",    tags=["Auth"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(payroll.router,   prefix="/payroll", tags=["Payroll"])

# ----- Health & Root -----
@app.get("/")
def root():
    return {"status": "ok", "service": "FMS API (with Payroll)"}

@app.get("/healthz")
def healthz():
    return {"ok": True}
