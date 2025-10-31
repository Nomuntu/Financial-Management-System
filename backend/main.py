from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import auth
import customers
import payroll

app = FastAPI(title="FMS API (with Payroll)", version="0.1.0")

# ---- CORS ----
# IMPORTANT: list every origin that will host your frontend EXACTLY (no trailing slash)
ALLOWED_ORIGINS = [
    "https://financial-management-system-frontend.onrender.com",  # your Render static site
    "http://localhost:5173",  # vite dev
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,      # allowed because we list explicit origins (not "*")
    allow_methods=["*"],         # allow POST/PUT/GET/OPTIONS etc.
    allow_headers=["*"],         # allow Content-Type, Authorization, etc.
    expose_headers=["*"],
)

# ---- Routers ----
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(customers.router, tags=["Customers"])
app.include_router(payroll.router, prefix="/payroll", tags=["Payroll"])

# ---- Simple health/landing ----
@app.get("/")
def read_root():
    return {"status": "ok", "name": "FMS API"}
