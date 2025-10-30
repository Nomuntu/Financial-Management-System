# FMS — with Payroll (Template-style HTML→PDF payslips)

## Backend
- FastAPI + SQLAlchemy + JWT
- Payroll endpoints under `/payroll`
- HTML→PDF payslips via WeasyPrint (no logo, company name from settings later)

### Run
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

## Deploy
- **Backend (Render)**: Build `pip install -r requirements.txt`; Start `uvicorn main:app --host 0.0.0.0 --port 10000`
- **Frontend (Netlify/Vercel)**: Build `npm run build`; Publish `dist`; Env `VITE_API_URL=https://<backend>.onrender.com`
