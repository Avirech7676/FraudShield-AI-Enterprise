# FraudShield React Frontend

React + Vite frontend for FraudShield AI Enterprise.

## Run Locally

```bash
npm install
npm run dev
```

The app opens at `http://localhost:5173` and calls the FastAPI backend at `http://127.0.0.1:8000` by default.

To change the API URL, create `.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Demo Login

If the API login is unavailable, the frontend supports local demo users:

- `admin` / `admin123`
- `analyst` / `analyst123`
- `manager` / `manager123`
- `auditor` / `auditor123`

## Build

```bash
npm run build
```
