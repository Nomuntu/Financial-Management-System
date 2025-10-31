# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# use fully-qualified imports so they work when the app is loaded as "backend.main"
from backend.routers import customers, payroll
from backend.auth import router as auth_router

app = FastAPI(title="Financial Management System API")

# allow your frontend & local dev
origins = [
    "https://financial-management-system-frontend.onrender.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],    # Authorization, Content-Type, etc.
)

@app.get("/")
def health():
    return {"status": "ok"}

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
