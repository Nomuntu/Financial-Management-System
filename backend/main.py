from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import auth
from routers import customers, payroll

app = FastAPI(title="FMS API (with Payroll)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(payroll.router, prefix="/payroll", tags=["Payroll"])

@app.get("/")
def root():
    return {"status": "ok", "service": "FMS API (with Payroll)"}
